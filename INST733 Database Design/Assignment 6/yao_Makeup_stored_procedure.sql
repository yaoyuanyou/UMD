USE ap;

DROP PROCEDURE IF EXISTS owed_to_state_vendors;

DELIMITER //
CREATE PROCEDURE owed_to_state_vendors (
    vendor_state_param VARCHAR(50)
)
BEGIN
    WITH Vendor AS (
        SELECT vendor_state,
			vendor_name,
            (SUM(invoice_total) - SUM(payment_total) - SUM(credit_total)) AS total_amt
        FROM vendors
        LEFT OUTER JOIN invoices USING(vendor_id)
        WHERE vendor_state = vendor_state_param
        GROUP BY vendor_state, vendor_name
        HAVING total_amt > 0
    ), 
		MaxAmt AS (
			SELECT vendor_state,
				MAX(total_amt) AS max_total_amt
			FROM Vendor
			GROUP BY vendor_state
    )
    SELECT a.vendor_state,
        a.vendor_name,
        a.total_amt AS highest_total
    FROM Vendor a
    LEFT OUTER JOIN MaxAmt b 
    ON a.vendor_state = b.vendor_state AND a.total_amt = b.max_total_amt;
END //
DELIMITER ;

CALL owed_to_state_vendors('CA');

