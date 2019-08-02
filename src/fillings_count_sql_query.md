```sql

# Query for Edgar data to get companies with multiple (>3) 10K filings

SELECT `CIK`, COUNT(`FORM-TYPE`) AS totCount
FROM `feed_header`
WHERE `feed_header`.`FORM-TYPE` = "10-K"
GROUP BY `feed_header`.`CIK`
HAVING totCount >3
ORDER BY totCount DESC;

```
