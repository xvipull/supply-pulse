-- MySQL 8+ reporting layer. Grain: one purchase-order line / receipt / invoice match.
CREATE OR REPLACE VIEW vw_supplier_scorecard AS
SELECT supplier_id, supplier_name,
  ROUND(100 * AVG(receipt_date <= promised_date AND received_qty >= ordered_qty),1) AS otif_pct,
  ROUND(100 * SUM(received_qty) / SUM(ordered_qty),1) AS fill_rate_pct,
  ROUND(100 * SUM(defect_qty) / NULLIF(SUM(received_qty),0),2) AS defect_rate_pct,
  ROUND(SUM(received_qty * (invoice_unit_price-contract_unit_price)),2) AS purchase_price_variance,
  ROUND(100 * AVG(contract_compliant),1) AS contract_compliance_pct,
  ROUND(SUM(received_qty * invoice_unit_price),2) AS spend
FROM fact_procurement_match GROUP BY supplier_id, supplier_name;

CREATE OR REPLACE VIEW vw_three_way_exceptions AS
SELECT po_id, supplier_name, promised_date, receipt_date, ordered_qty, received_qty,
  invoice_unit_price-contract_unit_price AS unit_price_variance,
  DATEDIFF(receipt_date,promised_date) AS days_late
FROM fact_procurement_match
WHERE receipt_date > promised_date OR received_qty < ordered_qty
   OR ABS(invoice_unit_price-contract_unit_price) > 0.01 OR contract_compliant = 0;
