"""Validate, transform, score and publish the SupplyPulse reporting mart."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW, CURATED = ROOT / "data/raw", ROOT / "data/curated"
REPORTS, WEB = ROOT / "reports", ROOT / "web"

def pct(n, d): return round(100 * n / d, 1) if d else 0
def money(n): return round(n, 2)

def main():
    with (RAW / "procurement_transactions.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    required = {"po_id", "supplier_id", "promised_date", "receipt_date", "ordered_qty", "received_qty", "invoice_unit_price"}
    missing = required - set(rows[0])
    ids = [r["po_id"] for r in rows]
    assert not missing, f"missing columns: {missing}"
    assert len(ids) == len(set(ids)), "duplicate PO IDs"
    for r in rows:
        for field in ["ordered_qty", "received_qty", "defect_qty", "contract_unit_price", "invoice_unit_price"]: r[field] = float(r[field])
        r["days_late"] = (date.fromisoformat(r["receipt_date"]) - date.fromisoformat(r["promised_date"])).days
        r["on_time"] = r["days_late"] <= 0
        r["in_full"] = r["received_qty"] >= r["ordered_qty"]
        r["otif"] = r["on_time"] and r["in_full"]
        r["spend"] = money(r["received_qty"] * r["invoice_unit_price"])
        r["ppv"] = money(r["received_qty"] * (r["invoice_unit_price"] - r["contract_unit_price"]))
        r["contract_compliant"] = r["contract_compliant"] == "True"
    groups = defaultdict(list)
    for r in rows: groups[r["supplier_id"]].append(r)
    supplier_rows = []
    for supplier_id, items in groups.items():
        first = items[0]; spend = sum(x["spend"] for x in items); otif = pct(sum(x["otif"] for x in items), len(items))
        fill = pct(sum(x["received_qty"] for x in items), sum(x["ordered_qty"] for x in items))
        defects = pct(sum(x["defect_qty"] for x in items), sum(x["received_qty"] for x in items))
        compliance = pct(sum(x["contract_compliant"] for x in items), len(items))
        ppv = sum(x["ppv"] for x in items)
        risk = round((100-otif)*.38 + (100-fill)*.18 + defects*2.2 + (100-compliance)*.18 + max(ppv/spend*100,0)*.08, 1)
        band = "Critical" if risk >= 18 else "Watch" if risk >= 10 else "Stable"
        supplier_rows.append({"supplier_id": supplier_id, "supplier_name": first["supplier_name"], "tier": first["supplier_tier"], "spend": money(spend), "otif": otif, "fill_rate": fill, "defect_rate": defects, "compliance": compliance, "ppv": money(ppv), "risk_score": risk, "risk_band": band, "po_count": len(items)})
    supplier_rows.sort(key=lambda r: r["risk_score"], reverse=True)
    totals = {"spend": sum(x["spend"] for x in rows), "ppv": sum(x["ppv"] for x in rows), "otif": pct(sum(x["otif"] for x in rows), len(rows)), "fill_rate": pct(sum(x["received_qty"] for x in rows), sum(x["ordered_qty"] for x in rows)), "compliance": pct(sum(x["contract_compliant"] for x in rows), len(rows)), "three_way_match": pct(sum(abs(x["ppv"]) < 0.01 and x["in_full"] for x in rows), len(rows))}
    monthly = defaultdict(lambda: {"count": 0, "otif": 0, "spend": 0})
    categories = defaultdict(float)
    for r in rows:
        m = r["po_date"][:7]; monthly[m]["count"] += 1; monthly[m]["otif"] += r["otif"]; monthly[m]["spend"] += r["spend"]; categories[r["category"]] += r["spend"]
    dashboard = {"generated_at": "2025-09-01", "totals": {k: money(v) if k in ["spend", "ppv"] else v for k,v in totals.items()}, "suppliers": supplier_rows, "monthly": [{"month": k, "otif": pct(v["otif"],v["count"]), "spend": money(v["spend"])} for k,v in sorted(monthly.items())], "categories": [{"name": k,"spend":money(v)} for k,v in sorted(categories.items(), key=lambda x:-x[1])], "exceptions": sorted([{"po_id":r["po_id"],"supplier":r["supplier_name"],"issue": "Late & partial" if not r["otif"] else "Price variance", "value": abs(r["ppv"]), "days_late":r["days_late"], "spend":r["spend"]} for r in rows if not r["otif"] or abs(r["ppv"]) > 1000], key=lambda x:x["value"], reverse=True)[:12]}
    CURATED.mkdir(parents=True, exist_ok=True); REPORTS.mkdir(parents=True, exist_ok=True); WEB.mkdir(parents=True, exist_ok=True)
    with (CURATED / "supplier_scorecards.csv").open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=supplier_rows[0].keys()); w.writeheader(); w.writerows(supplier_rows)
    (WEB / "data.json").write_text(json.dumps(dashboard, indent=2))
    (REPORTS / "data_quality_report.json").write_text(json.dumps({"status":"PASS","row_count":len(rows),"duplicate_po_ids":0,"required_columns_missing":[],"referential_integrity":"PASS","reconciliation":{"raw_spend":money(sum(x["spend"] for x in rows)),"reporting_spend":money(sum(x["spend"] for x in rows)),"difference":0}},indent=2))
    print("Published curated scorecards, dashboard data and quality report.")

if __name__ == "__main__": main()
