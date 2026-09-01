# SupplyPulse

**Supplier OTIF, Procurement Risk & Spend Control Tower**

SupplyPulse is a portfolio-grade procurement analytics product for Procurement, Supply Chain and Finance leaders. It turns PO, GRN and invoice records into governed supplier scorecards, a 3-way-match exception queue, and an interactive executive control tower.

## What it answers

- Which suppliers are eroding on-time, in-full (OTIF) performance and why?
- Where do invoice prices diverge from contracted prices?
- Which contract, delivery and quantity mismatches should be worked first?
- How concentrated is spend, and where is supplier risk accumulating?

## Architecture

```text
Synthetic PO / GRN / invoice data
            ↓
validation, type standardisation & reconciliation
            ↓
curated supplier scorecards + exception queue
            ↓
SQL reporting views + risk-priority scoring
            ↓
interactive web control tower / Power BI-ready dataset
```

## Quick start

```bash
python3 src/generate_data.py
python3 src/pipeline.py
python3 -m unittest discover -s tests
cd web && python3 -m http.server 8080
```

Open `http://localhost:8080`. The deployed dashboard is static and contains only synthetic data.

## Data model and controls

The reporting grain is a matched PO-line / goods receipt / invoice record. Raw data is immutable; the pipeline emits a curated `supplier_scorecards.csv`, browser data, and a machine-readable quality report. Controls include required-column validation, duplicate PO detection, valid numeric ranges, controlled synthetic keys, and source-to-reporting spend reconciliation.

See [requirements](docs/requirements.md), [KPI catalog](docs/kpi_catalog.md), [data dictionary](docs/data_dictionary.md), [assumptions](docs/assumptions.md), and [UAT](docs/uat.md).

## Key techniques

- Reproducible deterministic synthetic-data generation
- PO-GRN-invoice three-way reconciliation and exception logic
- Transparent weighted supplier-risk scoring (delivery, fill, defects, compliance, PPV)
- MySQL 8 reporting views for supplier scorecards and control queues
- Responsive executive dashboard with supplier-tier filtering

## Business insights from the demo

Supplier risk is intentionally segmented so that the dashboard surfaces a small priority queue rather than asking leaders to inspect every PO. The score is an explainable triage aid, not an automated supplier decision. Contract and invoice data must be approved by Finance before production use.

## Limitations

This repository uses synthetic transactions and a static Vercel dashboard. A production implementation would connect governed ERP sources, enforce role-based access, retain historical snapshots, and calibrate targets with Procurement and Finance.

## Resume-ready impact

Built SupplyPulse, an end-to-end supplier OTIF, procurement risk and spend control tower using Python, SQL, quality controls, three-way matching, transparent risk scoring and an executive decision dashboard.
