-- Beispielabfragen für die Praxis-Datenbank (data/praxis.db)
-- Ausführbar z. B. in Beekeeper Studio oder mit: sqlite3 data/praxis.db < sql/beispielabfragen.sql

-- 1) Letzte Dosis je Patient und Impfung
WITH letzte_dosis AS (
    SELECT patient_id, impfung, MAX(datum) AS letzte_dosis, COUNT(*) AS dosen
    FROM impfungen
    GROUP BY patient_id, impfung
)
SELECT p.patient_id, p.vorname, p.nachname, l.impfung, l.letzte_dosis, l.dosen
FROM letzte_dosis AS l
JOIN patienten   AS p USING (patient_id)
ORDER BY p.nachname, l.impfung
LIMIT 20;

-- 2) Tetanus/Diphtherie älter als 10 Jahre (überfällig) – inkl. Patienten ganz ohne Dosis
WITH td AS (
    SELECT patient_id, MAX(datum) AS letzte_dosis
    FROM impfungen
    WHERE impfung = 'Tetanus/Diphtherie'
    GROUP BY patient_id
)
SELECT p.patient_id, p.vorname, p.nachname, td.letzte_dosis
FROM patienten AS p
LEFT JOIN td USING (patient_id)
WHERE td.letzte_dosis IS NULL
   OR td.letzte_dosis < date('now', '-10 years')
ORDER BY td.letzte_dosis
LIMIT 20;

-- 3) Einwilligungen nach Kanal
SELECT einwilligung, COUNT(*) AS patienten
FROM patienten
GROUP BY einwilligung
ORDER BY patienten DESC;

-- 4) Versandprotokoll der letzten 30 Tage
SELECT gesendet_am, kanal, impfung, status
FROM erinnerungen
WHERE gesendet_am >= date('now', '-30 days')
ORDER BY gesendet_am DESC
LIMIT 20;
