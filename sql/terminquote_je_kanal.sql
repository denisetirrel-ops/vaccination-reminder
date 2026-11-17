-- Terminquote je Kanal: Anteil der Erinnerungen, nach denen innerhalb von :tage Tagen
-- ein Termin zur selben Impfung vereinbart wurde.
WITH erinnerung_mit_termin AS (
    SELECT
        e.erinnerung_id,
        e.kanal,
        MAX(CASE
                WHEN t.termin_id IS NOT NULL
                 AND julianday(t.vereinbart_am) - julianday(e.gesendet_am) BETWEEN 0 AND :tage
                THEN 1 ELSE 0
            END) AS termin_vereinbart          -- MAX verhindert Doppelzählung bei mehreren Terminen
    FROM erinnerungen AS e
    LEFT JOIN termine AS t
           ON t.patient_id = e.patient_id
          AND t.impfung    = e.impfung
    GROUP BY e.erinnerung_id, e.kanal
)
SELECT
    kanal,
    COUNT(*)               AS erinnerungen,
    SUM(termin_vereinbart) AS termine
FROM erinnerung_mit_termin
GROUP BY kanal
ORDER BY kanal;
