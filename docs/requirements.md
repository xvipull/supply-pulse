# Product charter

## Purpose

Give Procurement Head, Supply Chain Manager and Finance a shared daily view of supplier reliability, price variance, fulfillment and contract controls.

## Decisions supported

1. Prioritize the highest-value PO-GRN-invoice exceptions.
2. Escalate suppliers with deteriorating OTIF, fill rate or quality.
3. Focus sourcing reviews where spend is concentrated and risk is high.

## Scope

In scope: supplier master, purchase orders, goods receipts, invoices, contract pricing and a monthly performance view. Out of scope: supplier onboarding, payment execution, purchase approval workflows and autonomous supplier decisions.

## Operating model

Data owners: Procurement Operations (POs), Warehouse (GRNs), Accounts Payable (invoices), Strategic Sourcing (contracts). Planned refresh: daily at 06:00 local time. The demo contains no personal or commercially sensitive data.

## Acceptance criteria

- Every reporting record has a unique PO ID and required matching fields.
- Reporting spend reconciles to validated source spend with zero tolerance in the demo.
- OTIF, fill, PPV, compliance and risk definitions are documented.
- A user can filter supplier scorecards by tier and inspect priority exceptions.
