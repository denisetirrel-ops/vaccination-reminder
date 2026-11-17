"""Kernlogik: Impfregeln, Fälligkeitsberechnung, Datenbank und (simulierter) Versand.

Alles hier ist ohne Streamlit testbar. Das Stichtag-Argument macht die Logik
reproduzierbar (Tests und Demo nutzen ein festes Datum).
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Protocol

import pandas as pd
from dateutil.relativedelta import relativedelta

BASIS = Path(__file__).resolve().parent.parent
REGELN_CSV = BASIS / "data" / "impfregeln.csv"
DB_PFAD = BASIS / "data" / "praxis.db"

SAISONSTART_MONAT = 10      # Influenza/COVID: ab 1. Oktober ("im Herbst")
SAISON_VORLAUF_MONATE = 2   # Impfung ab 1. August zählt schon für die neue Saison
SPERRFRIST_TAGE = 90        # keine zweite Erinnerung zur selben Impfung innerhalb dieser Frist
STATUS_FAELLIG = ("überfällig", "bald fällig")

SCHEMA = """
CREATE TABLE IF NOT EXISTS patienten (
    patient_id      INTEGER PRIMARY KEY,
    vorname         TEXT NOT NULL,
    nachname        TEXT NOT NULL,
    geburtsdatum    TEXT NOT NULL,              -- ISO-Datum
    telefon         TEXT,
    email           TEXT,
    einwilligung    TEXT NOT NULL CHECK (einwilligung IN ('sms', 'email', 'keine')),
    fsme_indikation INTEGER NOT NULL DEFAULT 0 CHECK (fsme_indikation IN (0, 1))
);
CREATE TABLE IF NOT EXISTS impfungen (
    impfung_id  INTEGER PRIMARY KEY,
    patient_id  INTEGER NOT NULL REFERENCES patienten(patient_id),
    impfung     TEXT NOT NULL,
    datum       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_impfungen_patient ON impfungen(patient_id);
CREATE TABLE IF NOT EXISTS erinnerungen (
    erinnerung_id INTEGER PRIMARY KEY,
    patient_id    INTEGER NOT NULL REFERENCES patienten(patient_id),
    impfung       TEXT NOT NULL,
    faellig_am    TEXT NOT NULL,
    kanal         TEXT NOT NULL CHECK (kanal IN ('sms', 'email')),
    empfaenger    TEXT NOT NULL,
    nachricht     TEXT NOT NULL,
    gesendet_am   TEXT NOT NULL,
    status        TEXT NOT NULL                 -- 'simuliert' oder Status eines echten Anbieters
);
CREATE INDEX IF NOT EXISTS ix_erinnerungen_patient ON erinnerungen(patient_id, impfung);
CREATE TABLE IF NOT EXISTS termine (
    termin_id     INTEGER PRIMARY KEY,
    patient_id    INTEGER NOT NULL REFERENCES patienten(patient_id),
    impfung       TEXT NOT NULL,
    vereinbart_am TEXT NOT NULL,
    erinnerung_id INTEGER REFERENCES erinnerungen(erinnerung_id)
);
"""


# --------------------------------------------------------------------------- Regeln
def lade_regeln(pfad: Path = REGELN_CSV) -> pd.DataFrame:
    regeln = pd.read_csv(pfad)
    regeln["nur_bei_indikation"] = regeln["nur_bei_indikation"].astype(bool)
    return regeln


def _alter(geburtsdatum: date, stichtag: date) -> int:
    return relativedelta(stichtag, geburtsdatum).years


def _saisonstart(stichtag: date) -> date:
    """1. Oktober der laufenden Saison (Okt–März) bzw. der nächsten (ab April)."""
    jahr = stichtag.year - 1 if stichtag.month <= 3 else stichtag.year
    return date(jahr, SAISONSTART_MONAT, 1)


def berechne_faelligkeit(regel: pd.Series, geburtsdatum: date, dosen: list[date],
                         fsme_indikation: bool, stichtag: date) -> date | None:
    """Datum, ab dem die nächste Dosis fällig ist; None = erledigt oder nicht relevant."""
    if regel["nur_bei_indikation"] and not fsme_indikation:
        return None
    ab_alter = geburtsdatum + relativedelta(years=int(regel["mindestalter"]))
    dosen = sorted(dosen)
    typ = regel["typ"]

    if typ == "intervall":
        if not dosen:
            return ab_alter
        letzte = dosen[-1]
        monate = regel["intervall_monate"]
        if pd.notna(regel["intervall_monate_ab60"]) and _alter(geburtsdatum, letzte) >= 60:
            monate = regel["intervall_monate_ab60"]
        return letzte + relativedelta(months=int(monate))

    if typ == "einmalig":
        return None if dosen else ab_alter

    if typ == "serie":
        if len(dosen) >= int(regel["dosen"]):
            return None
        if not dosen:
            return ab_alter
        return dosen[-1] + relativedelta(months=int(regel["dosisabstand_monate"]))

    if typ == "saisonal":
        saison = _saisonstart(stichtag)
        gilt_ab = saison - relativedelta(months=SAISON_VORLAUF_MONATE)
        if any(d >= gilt_ab for d in dosen):
            return saison + relativedelta(years=1)  # diese Saison erledigt
        return max(saison, ab_alter)                # erst ab Mindestalter relevant

    raise ValueError(f"Unbekannter Regeltyp: {typ}")


def status_von(faellig_am: date | None, stichtag: date, vorlauf_tage: int) -> str:
    if faellig_am is None:
        return "erledigt"
    if faellig_am < stichtag:
        return "überfällig"
    if faellig_am <= stichtag + timedelta(days=vorlauf_tage):
        return "bald fällig"
    return "ok"


# --------------------------------------------------------------------------- Datenbank
def verbinde(pfad: Path | str = DB_PFAD) -> sqlite3.Connection:
    conn = sqlite3.connect(pfad, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def faelligkeiten(conn: sqlite3.Connection, stichtag: date, vorlauf_tage: int = 56,
                  regeln: pd.DataFrame | None = None) -> pd.DataFrame:
    """Eine Zeile je Patient und relevanter Impfung mit Fälligkeitsdatum und Status."""
    regeln = lade_regeln() if regeln is None else regeln
    patienten = pd.read_sql("SELECT * FROM patienten", conn, parse_dates=["geburtsdatum"])
    impfungen = pd.read_sql("SELECT patient_id, impfung, datum FROM impfungen", conn,
                            parse_dates=["datum"])
    dosen_je = (impfungen.groupby(["patient_id", "impfung"])["datum"]
                .apply(lambda s: [d.date() for d in s]).to_dict())

    zeilen = []
    for p in patienten.itertuples(index=False):
        geb = p.geburtsdatum.date()
        for _, r in regeln.iterrows():
            if r["nur_bei_indikation"] and not p.fsme_indikation:
                continue
            dosen = dosen_je.get((p.patient_id, r["impfung"]), [])
            faellig = berechne_faelligkeit(r, geb, dosen, bool(p.fsme_indikation), stichtag)
            zeilen.append({
                "patient_id": p.patient_id,
                "name": f"{p.vorname} {p.nachname}",
                "alter": _alter(geb, stichtag),
                "impfung": r["impfung"],
                "letzte_dosis": max(dosen) if dosen else None,
                "faellig_am": faellig,
                "status": status_von(faellig, stichtag, vorlauf_tage),
                "einwilligung": p.einwilligung,
                "hinweis": r["hinweis"],
            })
    df = pd.DataFrame(zeilen)
    # noch nicht im relevanten Alter und nicht im Vorlauf -> ausblenden
    zu_jung = (df["status"] == "ok") & df["letzte_dosis"].isna()
    return df.loc[~zu_jung].reset_index(drop=True)


# --------------------------------------------------------------------------- Versand
def nachricht(vorname: str, nachname: str, impfung: str, faellig_am: date,
              stichtag: date) -> str:
    datum = faellig_am.strftime("%d.%m.%Y")
    if faellig_am < stichtag:
        kern = f"ist Ihre Impfung gegen {impfung} seit {datum} fällig"
    else:
        kern = f"läuft Ihr Impfschutz gegen {impfung} am {datum} ab"
    return (f"Guten Tag {vorname} {nachname}, laut unseren Unterlagen {kern}. "
            "Bitte vereinbaren Sie einen Termin in unserer Praxis. Ihre Hausarztpraxis")


class Versand(Protocol):
    """Schnittstelle: ein echter SMS-/E-Mail-Anbieter muss nur diese Methode liefern."""
    def senden(self, kanal: str, empfaenger: str, text: str) -> str: ...


class SimulierterVersand:
    """Verschickt nichts, sondern meldet nur 'simuliert' zurück."""
    def senden(self, kanal: str, empfaenger: str, text: str) -> str:
        return "simuliert"


@dataclass
class VersandErgebnis:
    gesendet: int
    ohne_einwilligung: int
    gesperrt: int


def versende_erinnerungen(conn: sqlite3.Connection, faellige: pd.DataFrame, stichtag: date,
                          versand: Versand | None = None,
                          jetzt: datetime | None = None) -> VersandErgebnis:
    """Erinnert alle übergebenen fälligen Einträge – nur mit Einwilligung, ohne Doppelversand."""
    versand = versand or SimulierterVersand()
    jetzt = jetzt or datetime.combine(stichtag, datetime.now().time())
    grenze = (jetzt - timedelta(days=SPERRFRIST_TAGE)).isoformat(timespec="seconds")
    gesendet = ohne = gesperrt = 0

    for z in faellige.itertuples(index=False):
        if z.status not in STATUS_FAELLIG:
            continue
        p = conn.execute("SELECT vorname, nachname, telefon, email, einwilligung "
                         "FROM patienten WHERE patient_id = ?", (z.patient_id,)).fetchone()
        vorname, nachname, telefon, email, kanal = p
        if kanal == "keine":
            ohne += 1
            continue
        schon = conn.execute("SELECT 1 FROM erinnerungen WHERE patient_id = ? AND impfung = ? "
                             "AND gesendet_am >= ?", (z.patient_id, z.impfung, grenze)).fetchone()
        if schon:
            gesperrt += 1
            continue
        empfaenger = telefon if kanal == "sms" else email
        text = nachricht(vorname, nachname, z.impfung, z.faellig_am, stichtag)
        status = versand.senden(kanal, empfaenger, text)
        conn.execute("INSERT INTO erinnerungen (patient_id, impfung, faellig_am, kanal, "
                     "empfaenger, nachricht, gesendet_am, status) VALUES (?,?,?,?,?,?,?,?)",
                     (z.patient_id, z.impfung, z.faellig_am.isoformat(), kanal, empfaenger,
                      text, jetzt.isoformat(timespec="seconds"), status))
        gesendet += 1
    conn.commit()
    return VersandErgebnis(gesendet, ohne, gesperrt)


# --------------------------------------------------------------------------- Analyse
def terminquote_je_kanal(conn: sqlite3.Connection, tage: int = 30) -> pd.DataFrame:
    """Anteil der Erinnerungen, nach denen innerhalb von `tage` Tagen ein Termin vereinbart wurde."""
    sql = (BASIS / "sql" / "terminquote_je_kanal.sql").read_text(encoding="utf-8")
    return pd.read_sql(sql, conn, params={"tage": tage})


def wilson_ki(treffer: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95-%-Konfidenzintervall für einen Anteil (Wilson-Methode)."""
    if n == 0:
        return (0.0, 0.0)
    p = treffer / n
    nenner = 1 + z**2 / n
    mitte = (p + z**2 / (2 * n)) / nenner
    breite = z * ((p * (1 - p) / n + z**2 / (4 * n**2)) ** 0.5) / nenner
    return (mitte - breite, mitte + breite)
