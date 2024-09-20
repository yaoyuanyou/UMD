USE ap;
DROP VIEW IF EXISTS late_invoices;
CREATE VIEW late_invoices AS
SELECT vendor_name,
	a.invoice_number,
    DATE_FORMAT(a.invoice_due_date, "%M %D") AS due_date,
	DATE_FORMAT(a.payment_date, "%M %D") AS payment_date,
	DATEDIFF(a.payment_date, a.invoice_due_date) AS days_late, 
	CONCAT("$", a.invoice_total) AS invoice_total
FROM invoices a 
LEFT OUTER JOIN vendors USING(vendor_id)
LEFT OUTER JOIN invoice_archive USING(invoice_id)
WHERE (a.payment_date > a.invoice_due_date) OR a.payment_date IS NULL
ORDER BY days_late DESC, invoice_total DESC;

SELECT COUNT(*) FROM late_invoices;