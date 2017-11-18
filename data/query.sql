SELECT 
	s1.sdate,
	s1.sym,
	s1.open,
	s2.sym,
	s2.open
FROM stock s1
JOIN stock s2 
	ON s1.sdate = s2.sdate
WHERE 1=1
	AND s1.sym = "ORCL"
	AND s2.sym = "GTIM"
	AND s1.open != "null"
	AND s2.open != "null"
	AND s1.sdate BETWEEN '2017-06' AND '2017-09-14'
LIMIT 100;
