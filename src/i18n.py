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
        # Kopf
        "titel": "💉 Impf-Erinnerung",
        "untertitel": "Stichtag {datum} · Regeln nach STIKO-Empfehlungen (vereinfacht, "
                      "ärztlich zu prüfen) · **synthetische Testdaten**",
        "reiter": "Patient aufrufen|Fällige Impfungen|Versandprotokoll|Analyse|Regeln",
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
        "titel": "💉 Vaccination Reminder",
        "untertitel": "Reference date {datum} · Rules based on STIKO recommendations (German "
                      "Standing Committee on Vaccination; simplified, to be reviewed by a "
                      "physician) · **synthetic test data**",
        "reiter": "Open patient|Due vaccinations|Sending log|Analysis|Rules",
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
