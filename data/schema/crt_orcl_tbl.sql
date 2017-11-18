DROP TABLE IF EXISTS stock;

CREATE TABLE stock (
    sdate Date,
    open float,
    high float,
    low float,
    close float, 
    adj_close float,
    vol int,
    sym CHAR(8)
);
    
