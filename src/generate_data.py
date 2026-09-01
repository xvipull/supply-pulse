"""Create deterministic synthetic procurement data for the SupplyPulse demo."""
from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
random.seed(42)

SUPPLIERS = [
    ("SUP-001", "Northstar Components", "Strategic", 0.96, 0.02),
    ("SUP-002", "Meridian Industrial", "Strategic", 0.91, 0.04),
    ("SUP-003", "Atlas Materials", "Preferred", 0.87, 0.06),
    ("SUP-004", "Vertex Packaging", "Preferred", 0.94, 0.03),
    ("SUP-005", "Cobalt Supply Co.", "Approved", 0.79, 0.08),
    ("SUP-006", "Pioneer Logistics", "Approved", 0.84, 0.05),
]
CATEGORIES = [("Electronics", 240), ("Mechanical", 165), ("Packaging", 55), ("MRO", 85)]

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    start = date(2025, 1, 1)
    for n in range(1, 241):
        sid, supplier, tier, reliability, defect_probability = random.choice(SUPPLIERS)
        category, base_price = random.choice(CATEGORIES)
        ordered = random.choice([100, 150, 200, 250, 300, 500])
        po_date = start + timedelta(days=random.randrange(240))
        lead_days = random.randint(7, 19)
        promised = po_date + timedelta(days=lead_days)
        late = random.random() > reliability
        received = promised + timedelta(days=random.randint(1, 10) if late else random.randint(-2, 1))
        fill_rate = random.choice([1, 1, 1, 0.95, 0.9, 0.8])
        received_qty = round(ordered * fill_rate)
        contract_price = round(base_price * random.uniform(0.9, 1.1), 2)
        invoice_price = round(contract_price * random.uniform(0.96, 1.12), 2)
        defects = round(received_qty * (random.uniform(0.01, 0.08) if random.random() < defect_probability else 0))
        contract_compliant = random.random() > (0.13 if tier == "Approved" else 0.06)
        rows.append({
            "po_id": f"PO-{n:04d}", "supplier_id": sid, "supplier_name": supplier, "supplier_tier": tier,
            "category": category, "po_date": po_date.isoformat(), "promised_date": promised.isoformat(),
            "receipt_date": received.isoformat(), "ordered_qty": ordered, "received_qty": received_qty,
            "defect_qty": defects, "contract_unit_price": contract_price, "invoice_unit_price": invoice_price,
            "contract_compliant": contract_compliant, "invoice_id": f"INV-{n:04d}",
        })
    with (RAW / "procurement_transactions.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    print(f"Generated {len(rows)} PO / GRN / invoice records.")

if __name__ == "__main__":
    main()
