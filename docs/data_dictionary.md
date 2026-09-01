# Data dictionary

| Field | Meaning | Grain / source |
|---|---|---|
| `po_id` | Unique purchase-order line identifier | PO line |
| `supplier_id`, `supplier_name`, `supplier_tier` | Approved supplier attributes | Supplier master |
| `promised_date`, `receipt_date` | Supplier commitment and receipt dates | PO / GRN |
| `ordered_qty`, `received_qty`, `defect_qty` | Quantity and quality measures | PO / GRN |
| `contract_unit_price`, `invoice_unit_price` | Agreed and billed price | Contract / invoice |
| `contract_compliant` | Contract-control flag | Sourcing review |
