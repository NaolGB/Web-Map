CREATE SCHEMA MapTheInternet;

-- DROP TABLE IF EXISTS domains;

CREATE TABLE IF NOT EXISTS domains(
		id BIGINT NOT NULL AUTO_INCREMENT, 
		domain VARCHAR(300) UNIQUE,
        numIncomingLinks INT,
        numInternalLinks INT,
        connectionStatus VARCHAR(64),
        PRIMARY KEY (id)
);

SELECT *
FROM domains
WHERE domain = 'http://Unraveling the Mystery of “Visit Eroda,” The Tourism Campaign For An Island That Doesn’t Exist.'
ORDER BY numIncomingLinks DESC;

SELECT COUNT(*)
FROM domains;