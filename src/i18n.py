"""Zweisprachigkeit DE/EN.

Die Sprache wird als Objekt weitergereicht (nicht global gespeichert), damit sich
mehrere Besucher auf Streamlit Cloud nicht gegenseitig die Sprache umstellen.
Daten bleiben intern deutsch (z. B. Impfnamen); übersetzt wird nur die Anzeige.
"""
from __future__ import annotations

from datetime import date

SPRACHEN = {"de": "Deutsch", "en": "English"}

TEXTE: dict[str, dict[str, str]] = {
    "de": {
        # Seitenleiste
        "einstellungen": "Einstellungen",
        "sprache": "Sprache",
        "stichtag": "Stichtag",
        "vorlauf": "Vorlaufzeit (Wochen)",
        "vorlauf_hilfe": "So früh vor Ablauf gilt eine Impfung als „bald fällig“.",
        "versand_simuliert": "Versand ist **simuliert** – es werden keine SMS oder E-Mails verschickt.",
        "testdaten_neu": "Testdaten neu erzeugen",
        "demo_hinweis": "**Demo mit fiktiven Daten:** Alle Patientinnen, Patienten, Impfungen und "
                        "Kontaktdaten sind frei erfunden. Es werden keine echten Gesundheitsdaten "
                        "verarbeitet und keine Nachrichten verschickt.",
        "demo_kurz": "Fiktive Person – keine echten Daten.",
        # Startbereich
        "hero_kicker": "Portfolio-Prototyp · Hausarztpraxis",
        "hero_a": "Keine Auffrischung",
        "hero_b": "mehr verpassen.",
        "hero_lead": "Das Tool prüft jeden Patienten gegen die STIKO-Regeln, meldet fällige Impfungen "
                     "per Pop-up und erinnert Patienten mit Einwilligung per SMS oder E-Mail – "
                     "und misst, wie viele danach einen Termin machen.",
        "k_bald": "fällig in ≤ {wochen} Wochen",
        "k_pat": "Patienten betroffen",
        "k_erreich": "per SMS/E-Mail erreichbar",
        "pill_demo": "Fiktive Daten",
        "pill_stiko": "STIKO-Regeln",
        "pill_dsgvo": "nur mit Einwilligung",
        # Warum
        "w_kicker": "Warum Praxen das brauchen",
        "w_titel": "Impflücken sind Alltag – und kosten Gesundheit und Umsatz.",
        "f1_wert": "34 %",
        "f1_text": "der Menschen ab 60 waren 2024/25 gegen Grippe geimpft – der niedrigste Wert seit "
                   "Beginn der Erfassung. Das Ziel von WHO und EU liegt bei 75 %.",
        "f2_wert": "21 %",
        "f2_text": "Impfquote gegen Pneumokokken ab 60 (2024/25). Gürtelrose: 24 %, COVID-19: rund 14 %.",
        "f3_wert": "außerbudgetär",
        "f3_text": "Impfungen werden außerhalb des Praxisbudgets vergütet. Jede nachgeholte Impfung "
                   "ist bessere Versorgung und zusätzlicher Umsatz zugleich.",
        "quellen": "Quellen: [RKI VacMap](https://www.rki.de/vacmap) · "
                   "[PTAheute, 17.12.2025 (RKI-Impfquoten)](https://www.ptaheute.de/aktuelles/2025/12/17/impfquoten-wie-immun-ist-deutschland) · "
                   "[Ärzte Zeitung: Recall statt Impfpflicht](https://www.aerztezeitung.de/Wirtschaft/Recall-statt-Impfpflicht-267668.html)",
        "ohne_titel": "Ohne Tool",
        "ohne": "Recall-Listen von Hand ziehen · Patienten einzeln anrufen · Briefe drucken · "
                "niemand weiß, ob es etwas gebracht hat",
        "mit_titel": "Mit Impf-Erinnerung",
        "mit": "Fälligkeiten täglich automatisch · Pop-up beim Aufruf des Patienten · Versand nur mit "
               "Einwilligung, nie doppelt · Wirkung je Kanal messbar",
        "ablauf_titel": "So funktioniert es",
        "s1_t": "Erkennen", "s1": "Regeln nach STIKO prüfen jeden Patienten: Intervall, Saison, Alter, Serie.",
        "s2_t": "Anzeigen", "s2": "Pop-up mit Tagesübersicht und beim Aufruf eines Patienten.",
        "s3_t": "Erinnern", "s3": "SMS oder E-Mail – nur mit Einwilligung, keine Diagnosen, 90 Tage Sperrfrist.",
        "s4_t": "Messen", "s4": "Terminquote je Kanal mit Konfidenzintervall statt Bauchgefühl.",
        "r_titel": "Was bringt das Ihrer Praxis?",
        "r_lead": "Beispielrechnung für die jährliche Grippeimpfung – stellen Sie Ihre eigenen Werte ein.",
        "r_pat": "Patienten ab 60 in Ihrer Praxis",
        "r_pp": "Mehr Geimpfte durch Erinnerung (Prozentpunkte)",
        "r_pp_hilfe": "Annahme – keine Studienzahl. Prüfen Sie den Wert später im Reiter „Analyse“.",
        "r_euro": "Vergütung je Impfung in €",
        "r_euro_hilfe": "Annahme – je nach KV-Region und Impfvereinbarung verschieden.",
        "r_min": "Minuten je Erinnerung von Hand (Anruf, Brief)",
        "r_zus": "zusätzlich geimpfte Patienten pro Saison",
        "r_umsatz": "zusätzliche Vergütung pro Saison",
        "r_zeit": "Stunden MFA-Zeit gespart",
        "r_hinweis": "Beispielrechnung mit Ihren Annahmen, keine Prognose.",
        "q_titel": "Testdaten wie die Realität",
        "q_lead": "Die fiktiven Patientendaten sind so erzeugt, dass ihre Impfquoten (ab 60 Jahren) den RKI-Werten 2024/25 entsprechen. Darum wirken die vielen Lücken oben so groß: Sie sind in deutschen Praxen normal. Kleine Abweichungen entstehen durch Zufall bei rund 200 Patienten ab 60.",
        "q_text": "in den Testdaten · RKI: {rki}",
        "k_ueber": "Impflücken überfällig",
        "k_ueber_sub": "Ø {je} je betroffenem Patient",
        "pass_titel": "Digitaler Impfpass",
        "pass_nie": "nicht dokumentiert",
        "pass_heute": "heute",
        "alle": "Alle",
        "mehr": "+ {n} weitere Einträge (Filter nutzen)",
        "proto_kpi_ges": "Erinnerungen gesamt",
        "proto_kpi_sms": "per SMS",
        "proto_kpi_mail": "per E-Mail",
        "rh_intervall": "alle {j} Jahre ab {a}",
        "rh_intervall60": "alle {j} Jahre, ab 60 alle {j60} Jahre",
        "rh_saisonal": "jährlich im Herbst ab {a}",
        "rh_einmalig": "einmalig ab {a}",
        "rh_serie": "{d} Dosen ab {a}",
        "rh_indikation": " · nur bei Indikation",
        "f_titel": "So ist es gebaut",
        "f_text": "Portfolio-Projekt von Denise Tirrel (Data Analytics). Fälligkeiten per Python-Regelwerk aus SQLite, Versand über eine austauschbare Schnittstelle (hier simuliert), Wirkung als Terminquote je Kanal mit Wilson-Konfidenzintervall.",
        "f_repo": "Code auf GitHub",
        "f_linkedin": "LinkedIn",
        "demo_knopf": "▶ Demo in 30 Sekunden",
        "demo_titel": "Demo in 30 Sekunden",
        "demo_schritt": "Schritt {i} von {n}",
        "demo_weiter": "Weiter →",
        "demo_zurueck": "← Zurück",
        "demo_ende": "Selbst ausprobieren",
        "d1_t": "1 · Erkennen",
        "d1": "Jeden Morgen prüft das Tool alle {n} Patienten gegen die STIKO-Regeln: Alter, Intervall, Saison und Impfserien.",
        "d1_a": "Impflücken überfällig",
        "d1_b": "Patienten betroffen",
        "d1_c": "davon per SMS/E-Mail erreichbar",
        "d2_t": "2 · Anzeigen",
        "d2": "Ruft die MFA {name} ({alter}) auf, erscheint sofort ein Pop-up mit dem digitalen Impfpass:",
        "d3_t": "3 · Erinnern",
        "d3": "Mit Einwilligung geht automatisch eine Erinnerung raus, hier per {kanal}. Ohne Einwilligung keine Nachricht, und dieselbe Impfung frühestens nach {tage} Tagen erneut.",
        "d4_t": "4 · Messen",
        "d4": "Wirkt das? Die App misst, wie viele Patienten danach innerhalb von 30 Tagen einen Termin machen, mit 95-%-Konfidenzintervall statt Bauchgefühl.",
        "d4_ki": "Termin nach {kanal} · KI [{u}; {o}]",
        "d4_fazit": "Fazit: Die Konfidenzintervalle überlappen, also ist noch kein Kanal klar besser. Genau so ehrlich soll ein Dashboard sein.",
        # Kopf
        "titel": "💉 Impf-Erinnerung",
        "untertitel": "Stichtag {datum} · Regeln nach STIKO-Empfehlungen (vereinfacht, "
                      "ärztlich zu prüfen) · **synthetische Testdaten**",
        "reiter": "Warum?|Patient aufrufen|Fällige Impfungen|Versandprotokoll|Analyse|Regeln",
        # Popups
        "popup_tag_titel": "Tagesübersicht Impfungen",
        "ueberfaellig": "Überfällig",
        "faellig_in": "Fällig in ≤ {wochen} Wochen",
        "patienten_betroffen": "Patienten betroffen",
        "als_naechstes": "**Als Nächstes fällig:**",
        "alle_erinnern": "Alle Fälligen erinnern (simuliert)",
        "popup_patient_titel": "Impfung fällig",
        "patient_warnung": "**{name}** ({alter} Jahre) – {anzahl} Impfung(en) überfällig oder bald fällig.",
        "keine_einwilligung": "Keine Einwilligung für SMS/E-Mail – bitte im Gespräch ansprechen.",
        "vorschau": "Vorschau ({kanal}):",
        "nachricht_sprache": "",
        "erinnerung_senden": "Erinnerung senden (simuliert)",
        "meldung": "{gesendet} Erinnerung(en) simuliert versendet · {ohne} ohne Einwilligung "
                   "übersprungen · {gesperrt} bereits in den letzten {tage} Tagen erinnert",
        # Reiter
        "patient": "Patient",
        "name_eingeben": "Name eingeben …",
        "impfung": "Impfung",
        "status": "Status",
        "eintraege": "**{n}** Einträge bei **{p}** Patienten",
        "eintraege_erinnern": "Diese {n} Einträge erinnern (simuliert)",
        "aussage": "**Aussage:**",
        "regeln_info": "Die Regeln sind eine vereinfachte Umsetzung der STIKO-Empfehlungen für "
                       "Erwachsene und vor einem echten Einsatz ärztlich zu prüfen. Sie lassen "
                       "sich in `data/impfregeln.csv` pflegen.",
        # Spalten
        "sp_id": "ID", "sp_name": "Name", "sp_alter": "Alter", "sp_letzte": "Letzte Dosis",
        "sp_faellig": "Fällig am", "sp_einwilligung": "Einwilligung", "sp_hinweis": "Hinweis",
        "sp_gesendet": "Gesendet am", "sp_kanal": "Kanal", "sp_empfaenger": "Empfänger",
        "sp_nachricht": "Nachricht", "sp_quelle": "Quelle", "sp_regel": "Regel",
        "sp_ab_alter": "ab Alter",
        # Diagramme
        "testdaten": "Synthetische Testdaten",
        "d1_titel": "Fällige Impfungen ab {datum}",
        "d1_rueckstand": "Rückstand",
        "d1_bereits": "bereits\nüberfällig",
        "d1_naechste": "in den nächsten {n} Monaten",
        "d1_y": "Fällige Impfungen",
        "d1_saison": " – dann beginnt die neue Grippe- und COVID-Saison",
        "d1_satz": "Der Rückstand ist das Hauptproblem: {ueber} Impfungen sind bereits überfällig. "
                   "Neu fällig werden im Schnitt {mittel} je Monat, mit einer Spitze im "
                   "{monat} ({spitze}){saison}.",
        "d2_titel": "Impfstatus je Impfung (Anteil der relevanten Patienten)",
        "d2_bald": "bald fällig",
        "d2_satz": "Am größten ist die Lücke bei {impfung}: {anteil} der relevanten Patienten "
                   "(n={n} von {gesamt}) sind überfällig.",
        "d3_titel": "Terminquote nach Erinnerung je Kanal",
        "d3_y": "Termin innerhalb von {tage} Tagen",
        "d3_von": "{t} von {n}\nErinnerungen",
        "d3_ki": "95-%-KI",
        "d3_satz": "Nach einer {a} vereinbaren {pa} der Patienten innerhalb von {tage} Tagen einen "
                   "Termin, nach einer {b} {pb}. ",
        "d3_ueberlapp": "Die Konfidenzintervalle überlappen, der Unterschied ist also noch nicht belastbar.",
        "d3_getrennt": "Die Konfidenzintervalle überlappen nicht – der Unterschied ist deutlich.",
        "d4_titel": "Altersverteilung der Patienten (n={n})",
        "d4_x": "Alter in Jahren",
        "d4_y": "Patienten",
        "d4_mittel": "Mittelwert",
        "d4_median": "Median",
        "d4_jahre": "J.",
        "d4_dichte": "Dichte",
        "d4_ab60": "ab 60 Jahren: {anteil} (n={n})",
        "d4_satz": "{anteil} der Patienten sind 60 oder älter (Median {median} Jahre) – für sie "
                   "kommen Grippe, COVID-19, Pneumokokken und Gürtelrose hinzu, deshalb fallen "
                   "die meisten Fälligkeiten in dieser Gruppe an.",
    },
    "en": {
        "einstellungen": "Settings",
        "sprache": "Language",
        "stichtag": "Reference date",
        "vorlauf": "Lead time (weeks)",
        "vorlauf_hilfe": "How early before expiry a vaccination counts as “due soon”.",
        "versand_simuliert": "Sending is **simulated** – no text messages or emails are sent.",
        "testdaten_neu": "Regenerate test data",
        "demo_hinweis": "**Demo with fictitious data:** All patients, vaccinations and contact "
                        "details are made up. No real health data is processed and no messages "
                        "are sent.",
        "demo_kurz": "Fictitious person – no real data.",
        "hero_kicker": "Portfolio prototype · GP practice",
        "hero_a": "Never miss",
        "hero_b": "a booster again.",
        "hero_lead": "The tool checks every patient against the STIKO rules, flags due vaccinations in "
                     "a pop-up, reminds consenting patients by text message or email – and measures "
                     "how many book an appointment afterwards.",
        "k_bald": "due within {wochen} weeks",
        "k_pat": "patients affected",
        "k_erreich": "reachable by text/email",
        "pill_demo": "Fictitious data",
        "pill_stiko": "STIKO rules",
        "pill_dsgvo": "consent only",
        "w_kicker": "Why practices need this",
        "w_titel": "Vaccination gaps are everyday reality – costing health and revenue.",
        "f1_wert": "34%",
        "f1_text": "of people aged 60+ in Germany got a flu shot in 2024/25 – the lowest value since "
                   "records began. The WHO and EU target is 75%.",
        "f2_wert": "21%",
        "f2_text": "pneumococcal vaccination rate at 60+ (2024/25). Shingles: 24%, COVID-19: about 14%.",
        "f3_wert": "outside budget",
        "f3_text": "In Germany, vaccinations are paid outside the practice budget. Every catch-up "
                   "vaccination means better care and extra revenue.",
        "quellen": "Sources: [RKI VacMap](https://www.rki.de/vacmap) · "
                   "[PTAheute, 17 Dec 2025 (RKI vaccination rates)](https://www.ptaheute.de/aktuelles/2025/12/17/impfquoten-wie-immun-ist-deutschland) · "
                   "[Ärzte Zeitung: recall instead of mandates](https://www.aerztezeitung.de/Wirtschaft/Recall-statt-Impfpflicht-267668.html)",
        "ohne_titel": "Without the tool",
        "ohne": "Pull recall lists by hand · call patients one by one · print letters · "
                "nobody knows whether it worked",
        "mit_titel": "With Vaccination Reminder",
        "mit": "Due dates found automatically every day · pop-up when a patient is opened · sent only "
               "with consent, never twice · impact measurable per channel",
        "ablauf_titel": "How it works",
        "s1_t": "Detect", "s1": "STIKO-based rules check every patient: interval, season, age, series.",
        "s2_t": "Show", "s2": "Pop-up with the daily overview and whenever a patient is opened.",
        "s3_t": "Remind", "s3": "Text or email – consent only, no diagnoses, 90-day block on repeats.",
        "s4_t": "Measure", "s4": "Booking rate per channel with confidence interval instead of gut feeling.",
        "r_titel": "What does it bring your practice?",
        "r_lead": "Example calculation for the yearly flu shot – set your own values.",
        "r_pat": "Patients aged 60+ in your practice",
        "r_pp": "More vaccinated thanks to reminders (percentage points)",
        "r_pp_hilfe": "Assumption, not a study figure. Check it later in the Analysis tab.",
        "r_euro": "Fee per vaccination in €",
        "r_euro_hilfe": "Assumption – differs by region and vaccination agreement.",
        "r_min": "Minutes per manual reminder (call, letter)",
        "r_zus": "additional patients vaccinated per season",
        "r_umsatz": "additional fees per season",
        "r_zeit": "hours of staff time saved",
        "r_hinweis": "Example calculation based on your assumptions, not a forecast.",
        "q_titel": "Test data that mirrors reality",
        "q_lead": "The fictitious patient data is generated so that its vaccination rates (age 60+) match the German RKI figures for 2024/25. That is why the gaps above look so large: they are normal in German practices. Small deviations are random noise with about 200 patients aged 60+.",
        "q_text": "in the test data · RKI: {rki}",
        "k_ueber": "vaccination gaps overdue",
        "k_ueber_sub": "avg. {je} per affected patient",
        "pass_titel": "Digital vaccination record",
        "pass_nie": "not documented",
        "pass_heute": "today",
        "alle": "All",
        "mehr": "+ {n} more entries (use the filters)",
        "proto_kpi_ges": "reminders in total",
        "proto_kpi_sms": "by text message",
        "proto_kpi_mail": "by email",
        "rh_intervall": "every {j} years from {a}",
        "rh_intervall60": "every {j} years, from 60 every {j60} years",
        "rh_saisonal": "yearly in autumn from {a}",
        "rh_einmalig": "once from {a}",
        "rh_serie": "{d} doses from {a}",
        "rh_indikation": " · only if indicated",
        "f_titel": "How it is built",
        "f_text": "Portfolio project by Denise Tirrel (data analytics). Due dates from a Python rule set over SQLite, sending through a swappable interface (simulated here), impact measured as appointment rate per channel with a Wilson confidence interval.",
        "f_repo": "Code on GitHub",
        "f_linkedin": "LinkedIn",
        "demo_knopf": "▶ 30-second demo",
        "demo_titel": "30-second demo",
        "demo_schritt": "Step {i} of {n}",
        "demo_weiter": "Next →",
        "demo_zurueck": "← Back",
        "demo_ende": "Try it yourself",
        "d1_t": "1 · Detect",
        "d1": "Every morning the tool checks all {n} patients against the STIKO rules: age, interval, season and vaccine series.",
        "d1_a": "vaccination gaps overdue",
        "d1_b": "patients affected",
        "d1_c": "of them reachable by text/email",
        "d2_t": "2 · Show",
        "d2": "When staff open {name} ({alter}), a pop-up immediately shows the digital vaccination record:",
        "d3_t": "3 · Remind",
        "d3": "With consent, a reminder goes out automatically, here by {kanal}. No consent, no message, and the same vaccine at most once every {tage} days.",
        "d4_t": "4 · Measure",
        "d4": "Does it work? The app measures how many patients book an appointment within 30 days, with a 95% confidence interval instead of gut feeling.",
        "d4_ki": "appointment after {kanal} · CI [{u}; {o}]",
        "d4_fazit": "Bottom line: the confidence intervals overlap, so no channel is clearly better yet. That is how honest a dashboard should be.",
        "titel": "💉 Vaccination Reminder",
        "untertitel": "Reference date {datum} · Rules based on STIKO recommendations (German "
                      "Standing Committee on Vaccination; simplified, to be reviewed by a "
                      "physician) · **synthetic test data**",
        "reiter": "Why?|Open patient|Due vaccinations|Sending log|Analysis|Rules",
        "popup_tag_titel": "Daily vaccination overview",
        "ueberfaellig": "Overdue",
        "faellig_in": "Due within ≤ {wochen} weeks",
        "patienten_betroffen": "Patients affected",
        "als_naechstes": "**Due next:**",
        "alle_erinnern": "Remind all due patients (simulated)",
        "popup_patient_titel": "Vaccination due",
        "patient_warnung": "**{name}** ({alter} years) – {anzahl} vaccination(s) overdue or due soon.",
        "keine_einwilligung": "No consent for text/email – please mention it during the visit.",
        "vorschau": "Preview ({kanal}):",
        "nachricht_sprache": "The message is sent in German, as the practice is located in Germany.",
        "erinnerung_senden": "Send reminder (simulated)",
        "meldung": "{gesendet} reminder(s) sent (simulated) · {ohne} skipped without consent · "
                   "{gesperrt} already reminded within the last {tage} days",
        "patient": "Patient",
        "name_eingeben": "Type a name …",
        "impfung": "Vaccination",
        "status": "Status",
        "eintraege": "**{n}** entries for **{p}** patients",
        "eintraege_erinnern": "Remind these {n} entries (simulated)",
        "aussage": "**Key finding:**",
        "regeln_info": "The rules are a simplified implementation of the STIKO recommendations "
                       "for adults and must be reviewed by a physician before real use. They are "
                       "maintained in `data/impfregeln.csv`.",
        "sp_id": "ID", "sp_name": "Name", "sp_alter": "Age", "sp_letzte": "Last dose",
        "sp_faellig": "Due on", "sp_einwilligung": "Consent", "sp_hinweis": "Note",
        "sp_gesendet": "Sent at", "sp_kanal": "Channel", "sp_empfaenger": "Recipient",
        "sp_nachricht": "Message", "sp_quelle": "Source", "sp_regel": "Rule",
        "sp_ab_alter": "from age",
        "testdaten": "Synthetic test data",
        "d1_titel": "Vaccinations due from {datum}",
        "d1_rueckstand": "Backlog",
        "d1_bereits": "already\noverdue",
        "d1_naechste": "in the next {n} months",
        "d1_y": "Vaccinations due",
        "d1_saison": " – when the new flu and COVID season starts",
        "d1_satz": "The backlog is the main issue: {ueber} vaccinations are already overdue. "
                   "On average {mittel} new ones fall due per month, peaking in {monat} "
                   "({spitze}){saison}.",
        "d2_titel": "Vaccination status by vaccine (share of eligible patients)",
        "d2_bald": "due soon",
        "d2_satz": "The largest gap is for {impfung}: {anteil} of eligible patients "
                   "(n={n} of {gesamt}) are overdue.",
        "d3_titel": "Appointment rate after reminder by channel",
        "d3_y": "Appointment within {tage} days",
        "d3_von": "{t} of {n}\nreminders",
        "d3_ki": "95% CI",
        "d3_satz": "After a {a}, {pa} of patients book an appointment within {tage} days; "
                   "after an {b}, {pb}. ",
        "d3_ueberlapp": "The confidence intervals overlap, so the difference is not yet conclusive.",
        "d3_getrennt": "The confidence intervals do not overlap – the difference is clear.",
        "d4_titel": "Age distribution of patients (n={n})",
        "d4_x": "Age in years",
        "d4_y": "Patients",
        "d4_mittel": "Mean",
        "d4_median": "Median",
        "d4_jahre": "yrs",
        "d4_dichte": "Density",
        "d4_ab60": "aged 60+: {anteil} (n={n})",
        "d4_satz": "{anteil} of patients are 60 or older (median {median} years) – flu, COVID-19, "
                   "pneumococcal and shingles vaccines are added for them, so most due "
                   "vaccinations fall in this group.",
    },
}

IMPFUNG_EN = {
    "Tetanus/Diphtherie": "Tetanus/diphtheria",
    "Influenza": "Influenza",
    "COVID-19": "COVID-19",
    "Pneumokokken": "Pneumococcal",
    "Herpes zoster": "Herpes zoster (shingles)",
    "RSV": "RSV",
    "FSME": "TBE (tick-borne encephalitis)",
}
STATUS_EN = {"überfällig": "overdue", "bald fällig": "due soon", "ok": "ok", "erledigt": "completed"}
KANAL = {"de": {"sms": "SMS", "email": "E-Mail", "keine": "keine"},
         "en": {"sms": "text message", "email": "email", "keine": "none"}}
HINWEIS_EN = {
    "Tetanus/Diphtherie": "Next booster once as Tdap (with pertussis)",
    "Influenza": "Yearly in autumn",
    "COVID-19": "Yearly in autumn",
    "Pneumokokken": "Once; risk groups may need further doses",
    "Herpes zoster": "2 doses 2–6 months apart",
    "RSV": "Once from age 75",
    "FSME": "Simplified – interval depends on vaccine, to be reviewed by a physician",
}
MONATE = {"de": ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"],
          "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}


class Sprache:
    """Übersetzer und Zahlenformat für eine Sprache (de: 1.234,5 · en: 1,234.5)."""

    def __init__(self, code: str = "de"):
        if code not in TEXTE:
            raise ValueError(f"Unbekannte Sprache: {code}")
        self.code = code

    def t(self, schluessel: str, **werte) -> str:
        return TEXTE[self.code][schluessel].format(**werte)

    def zahl(self, x: float, nachkomma: int = 1) -> str:
        s = f"{x:,.{nachkomma}f}"
        if self.code == "de":
            s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return s

    def prozent(self, anteil: float, nachkomma: int = 1) -> str:
        wert = self.zahl(anteil * 100, nachkomma)
        return f"{wert} %" if self.code == "de" else f"{wert}%"

    def datum(self, d: date) -> str:
        return d.strftime("%d.%m.%Y") if self.code == "de" else d.strftime("%d %b %Y")

    def datumsformat(self) -> str:
        """strftime-Format für Tabellen."""
        return "%d.%m.%Y" if self.code == "de" else "%Y-%m-%d"

    def monat(self, m: int, jahr: int) -> str:
        return f"{MONATE[self.code][m - 1]} {jahr}"

    def monat_kurz(self, m: int) -> str:
        return MONATE[self.code][m - 1]

    def impfung(self, name: str) -> str:
        return name if self.code == "de" else IMPFUNG_EN.get(name, name)

    def status(self, s: str) -> str:
        return s if self.code == "de" else STATUS_EN.get(s, s)

    def kanal(self, k: str) -> str:
        return KANAL[self.code].get(k, k)

    def hinweis(self, impfung: str, text: str) -> str:
        return text if self.code == "de" else HINWEIS_EN.get(impfung, text)
