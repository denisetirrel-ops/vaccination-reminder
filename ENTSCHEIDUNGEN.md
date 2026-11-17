# Entscheidungen – Impf-Erinnerungstool (Portfolio-Prototyp)

Stand: 17.11.2026 · Methode: Rat aus drei Sitzen + Urteil (llm-council)

> **Art des Rats:** Ein Modell in einem Gespräch mit drei festen Haltungen.
> Die drei Sitze teilen sich die blinden Flecken dieses Modells; ihre Einigkeit
> zählt deshalb weniger als die Einigkeit unabhängiger Modelle.

## Die Frage an alle Sitze

Portfolio-Prototyp mit Testdaten: Ein Tool für eine Hausarztpraxis zeigt ein Popup,
sobald Auffrischimpfungen fällig werden, und schickt Patienten eine Erinnerung per SMS
oder E-Mail. Zu entscheiden:
(1) Popup-Technik, (2) Datenhaltung, (3) Impfregeln und Vorlaufzeit,
(4) echter oder simulierter Versand, (5) Umfang für ein überzeugendes Data-Analyst-Portfolio.

---

## Sitz A – Skeptiker (sucht, was bricht)

1. **Popup:** Eine Desktop-Tray-App ist für ein Portfolio eine Falle. Recruiter können sie
   nicht per Link öffnen, sie braucht eine Installation und je nach Betriebssystem andere
   Bibliotheken. Streamlit mit `st.dialog` (modales Fenster) plus `st.toast` simuliert das
   Popup ausreichend und läuft im Browser. → **Streamlit**
2. **Daten:** CSV bricht, sobald das Tool *schreiben* muss (Versandprotokoll, keine
   Doppelversände). → **SQLite**; CSV nur als Import-Format.
3. **Regeln:** Keine Regeln im Code verstecken. Jede Regel braucht Quelle und Stand, sonst
   wirkt das Tool medizinisch verbindlich. Ein Hinweis „ärztlich prüfen“ muss sichtbar sein.
4. **Versand:** Kein echter Gateway. Das kostet Geld, braucht Zugangsdaten, und ein Versehen
   mit echten Nummern wäre peinlich. → **Simulation mit Protokoll**, aber hinter einer
   Schnittstelle, damit ein echter Anbieter austauschbar bleibt.
5. **Umfang:** Nicht überbauen. Lieber 4 saubere Funktionen als 10 halbe. Synthetische
   „Erfolgsquoten“ müssen klar als Testdaten gekennzeichnet sein.

Konfidenz: 0,8

## Sitz B – Fachexpertin (achtet auf fachliche Korrektheit)

1. **Popup:** Fachlich zählt der Moment: beim *Aufruf eines Patienten* und als
   *Tagesliste* morgens. Technik ist zweitrangig; Streamlit-Dialog reicht für die Demo.
2. **Daten:** SQLite mit getrennten Tabellen für Patienten, Impfungen, Erinnerungen und
   Termine. Einwilligung und Kanal gehören zum Patienten – ohne Einwilligung kein Versand.
3. **Regeln (STIKO, Erwachsene):**
   - Tetanus/Diphtherie: alle 10 Jahre; die nächste einmalig mit Pertussis (Tdap)
   - Influenza ab 60: jährlich im Herbst
   - COVID-19 ab 60: jährlich im Herbst
   - Pneumokokken ab 60: einmalig
   - Herpes zoster ab 60: 2 Dosen
   - RSV ab 75: einmalig
   - FSME nur bei Indikation (Risikogebiet): Auffrischung je nach Alter alle 3–5 Jahre

   Saisonale Impfungen „laufen nicht ab“, sie sind ab Saisonbeginn fällig – das muss die
   Logik getrennt behandeln. **Vorlaufzeit konfigurierbar, Standard 8 Wochen.**
4. **Versand:** Simuliert. Nachricht ohne Diagnosen, nur „Impfschutz gegen … läuft ab“.
5. **Umfang:** Lieber alle sieben Regeln in einer Tabelle (kostet kaum Code) als nur Tetanus.

Konfidenz: 0,75

## Sitz C – die Person, die damit lebt (Denise / Recruiter)

1. **Popup:** Ich will einen Link ins Portfolio stellen können → **Streamlit** (lässt sich
   später auf Streamlit Community Cloud stellen). Desktop-Benachrichtigung höchstens als
   spätere Erweiterung.
2. **Daten:** SQLite, weil ich dann echte **SQL-Abfragen** zeigen kann – das ist mein Profil.
3. **Regeln:** Als CSV-Tabelle, die man in Google Sheets pflegen könnte.
4. **Versand:** Simuliert, mit sichtbarem Protokoll und Vorschau der Nachricht.
5. **Umfang:** Der Unterschied zu „noch einem Dashboard“ ist der Prozess:
   *fällig → erinnert → Termin*. Ein Analyse-Teil mit Terminquote je Kanal und
   Konfidenzintervall zeigt Data-Analyst-Können. Diagramme im eigenen Stil (Pastell,
   Werte beschriftet, Dezimalkomma).

Konfidenz: 0,85

---

## Urteil (anonymisiert: A, B, C)

**Einig:**
- Streamlit statt Desktop-Tray-App; Popup über `st.dialog` + `st.toast`
- SQLite als Datenbank, CSV nur für Regeln und Import
- Versand simuliert, mit Protokoll und Schnittstelle für einen echten Anbieter
- Regeln als Tabelle mit Quelle und Stand, Hinweis „ärztlich prüfen“

**Uneinig und Entscheidung:**
- *Wie viele Impfungen?* A will schmal bleiben, B will alle sieben. Stärkstes Argument für B:
  die Regeltabelle macht weitere Zeilen fast kostenlos. → **Alle sieben**, aber eine
  gemeinsame, einfache Logik (Intervall / einmalig / saisonal / Dosenserie).
- *Analyse mit Erfolgsquoten?* C will sie, A warnt vor erfundenen Ergebnissen.
  → **Ja**, mit deutlichem Label „synthetische Testdaten“ im Diagramm.

**Geprüfte Fakten (gegen Quellen):**
- Td alle 10 Jahre, nächste einmalig als Tdap – BMG, Impfkalender ✔
- Influenza, COVID-19 (jährlich Herbst), Pneumokokken (einmalig) ab 60 – BMG ✔
- Herpes zoster ab 60 mit 2 Dosen, RSV ab 75 einmalig – STIKO-Kalender (AMBOSS-Wiedergabe) ✔
- FSME ab 60 alle 3 Jahre – Landkreis Passau / schutz-impfung-jetzt.de ✔
- FSME unter 60 alle 5 Jahre – **nicht geprüft** (hängt vom Impfstoff ab) → im Tool als
  „vereinfacht, ärztlich prüfen“ markiert

**Endergebnis:** Streamlit + SQLite + Regeltabelle (7 Impfungen) + simulierter Versand mit
Einwilligungsprüfung + Analyse-Seite. Konfidenz **0,8**.

| Sitz | Position | Konfidenz |
|---|---|---|
| A – Skeptiker | Streamlit, SQLite, simuliert, schmal halten | 0,8 |
| B – Fachexpertin | alle STIKO-Regeln, saisonal getrennt, Einwilligung | 0,75 |
| C – Nutzerin | Link fürs Portfolio, SQL zeigen, Analyse fällig→Termin | 0,85 |

**Braucht noch einen Menschen:** fachliche Abnahme der Regeln durch eine Ärztin/einen Arzt,
falls das Tool je echte Daten sieht.

---

# Runde 2 – Zweisprachigkeit (DE/EN) und Online-Gang

Stand: 17.11.2026 · gleiche Methode (ein Modell, drei Haltungen – Einigkeit zählt weniger
als bei unabhängigen Modellen)

**Frage:** (1) Wie wird übersetzt? (2) Welches Zahlenformat im Englischen? (3) In welcher
Sprache gehen Patientennachrichten raus? (4) Wie kommt die App online (Repo, Datenbank)?

## Sitz A – Skeptiker
1. Kein gettext, kein Framework: ein Python-Wörterbuch je Sprache reicht. Was bricht, sind
   fehlende Schlüssel → ein Test muss prüfen, dass DE und EN dieselben Schlüssel haben.
   Die Sprache **nicht** als globale Variable speichern: Auf Streamlit Cloud teilen sich alle
   Besucher denselben Prozess, eine globale Sprache würde zwischen Nutzern „überspringen“.
2. Englisch mit Punkt. „47,5 %“ liest ein internationaler Recruiter als Tippfehler.
3. –
4. Die Datenbank nicht ins Repo legen (Binärdatei, ändert sich bei jedem Klick). Die App
   erzeugt sie beim ersten Start selbst. Die Diagramm-PNGs für das README dürfen rein.

Konfidenz: 0,8

## Sitz B – Fachexpertin
1. Fachbegriffe korrekt übersetzen: Tetanus/diphtheria, Influenza, COVID-19, Pneumococcal,
   Herpes zoster (shingles), RSV, TBE (tick-borne encephalitis) statt FSME. STIKO bleibt
   STIKO, mit Erklärung „German Standing Committee on Vaccination“.
2. Englisch mit Punkt, Deutsch mit Komma – Zahlenformat gehört zur Sprache.
3. **Patientennachrichten bleiben deutsch**: Die Praxis steht in Deutschland, die
   Oberflächensprache ist die der Nutzerin, nicht die der Patienten. In der EN-Ansicht ein
   Hinweis „message is sent in German“.
4. –

Konfidenz: 0,75

## Sitz C – die Person, die damit lebt (Denise / Recruiter)
1. Umschalter oben in der Seitenleiste, Standard Deutsch. Diagramme inkl. Aussagesatz
   und README in beiden Sprachen – sonst wirkt die EN-Version halbfertig.
2. Meine Regel ist Dezimalkomma; für die EN-Version wäre Punkt aber professioneller.
   → **Nutzerin gefragt**
3. Einverstanden mit deutschen Nachrichten.
4. Öffentliches Repo auf meinem Account wie meine anderen Projekte, englischer Name.
   → **Nutzerin gefragt** (Veröffentlichung ist ihre Entscheidung)

Konfidenz: 0,85

## Urteil
**Einig:** Wörterbuch-Übersetzung mit Schlüssel-Test · Sprache pro Sitzung, nicht global ·
deutsche Fachbegriffe sauber ins Englische · DB wird beim Start erzeugt, nicht eingecheckt ·
Patientennachrichten auf Deutsch.

**Von Denise entschieden:** Deutsch mit Komma, Englisch mit Punkt · öffentliches Repo
`denisetirrel-ops/vaccination-reminder`.

**Geprüft:** Streamlit Community Cloud braucht ein GitHub-Repo und eine Anmeldung der
Kontoinhaberin – das Deploy-Klicken bleibt bei Denise.

| Sitz | Position | Konfidenz |
|---|---|---|
| A – Skeptiker | Wörterbuch + Test, keine globale Sprache, DB nicht ins Repo | 0,8 |
| B – Fachexpertin | korrekte EN-Fachbegriffe, Nachrichten deutsch | 0,75 |
| C – Nutzerin | Umschalter, alles zweisprachig, Repo auf eigenem Account | 0,85 |

Endergebnis Konfidenz **0,8**.

## Runde 3 – Optik, Interaktivität, Nutzen für Praxen (17.11.2026)

Rat aus drei Haltungen eines Modells (Skeptiker, Fachperson Praxis/Daten, spätere Nutzerin bzw. Recruiter). Gleiches Modell, gleiche blinde Flecken – Einigkeit zählt daher nur eingeschränkt.

| Sitz | Position | Konfidenz |
|---|---|---|
| A Skeptiker | Dunkles Thema per config.toml und wenig CSS; Nutzen nur mit belegten Zahlen; Rechner mit sichtbar markierten Annahmen; keine Plotly-Umstellung, keine Animationen | 0,70 |
| B Fachperson | Impflücke je Impfung und Erreichbarkeit (Einwilligung) als Kernzahlen; Vergütung nie als Fakt nennen, sondern als Eingabe | 0,75 |
| C Nutzerin | In 5 Sekunden verstehen: Startbereich mit Satz, 4 Kennzahlen, „Warum?“ als erster Reiter, Ablauf in 4 Schritten | 0,70 |

**Ergebnis (Konfidenz 0,75):** Look der Homepage (dunkel, Glas-Karten, Blau/Pfirsich, Space Grotesk/Inter/JetBrains Mono), Startbereich mit Kennzahlen inkl. Anteil erreichbarer Patienten, neuer Reiter „Warum?“ mit drei belegten Fakten (RKI-Impfquoten 2024/25, außerbudgetäre Vergütung), Vergleich ohne/mit Tool, Ablauf in 4 Schritten und interaktivem Nutzenrechner mit markierten Annahmen. Diagramme im dunklen Thema, README-Vorschau bleibt hell.

**Bewusst gelassen:** Plotly-Umstellung, Animationen, erfundene Erfolgsquoten oder EBM-Beträge als Fakten.

**Geprüft:** Impfquoten 60+ 2024/25 (Influenza 34 %, Pneumokokken 21 %, Gürtelrose 24 %, COVID-19 ~14 %, WHO/EU-Ziel 75 %) laut RKI, berichtet von PTAheute (17.12.2025) und web.de; außerbudgetäre Vergütung laut Ärzte Zeitung. **Offen für Menschen:** reale Vergütungshöhe je KV-Region.
