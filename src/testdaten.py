"""Erzeugt synthetische Testdaten (keine echten Personen) und schreibt sie in SQLite.

Aufruf:  python src/testdaten.py            -> data/praxis.db mit 400 Patienten
"""
from __future__ import annotations

import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path

import numpy as np
from dateutil.relativedelta import relativedelta

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import DB_PFAD, _saisonstart, verbinde  # noqa: E402

VORNAMEN = ["Anna", "Ben", "Clara", "David", "Elif", "Finn", "Greta", "Hannes", "Ida", "Jonas",
            "Karin", "Lukas", "Maria", "Niklas", "Olga", "Paul", "Rita", "Sven", "Tanja", "Uwe",
            "Vera", "Wolfgang", "Yasemin", "Zoe", "Heike", "Jürgen", "Monika", "Peter", "Sabine",
            "Thomas"]
NACHNAMEN = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker",
             "Hoffmann", "Schulz", "Koch", "Richter", "Klein", "Wolf", "Neumann", "Schröder",
             "Braun", "Zimmermann", "Krüger", "Hartmann", "Lange", "Werner", "Krause", "Peters",
             "Janssen", "Hinrichs", "Ahrens", "Gerdes", "Behrens", "Oltmanns"]


def _tag(rng: np.random.Generator, von: date, bis: date) -> date:
    return von + timedelta(days=int(rng.integers(0, max((bis - von).days, 1))))


def erzeuge(pfad: Path = DB_PFAD, n: int = 400, stichtag: date | None = None,
            seed: int = 42) -> Path:
    stichtag = stichtag or date.today()
    rng = np.random.default_rng(seed)
    pfad.unlink(missing_ok=True)
    conn = verbinde(pfad)

    patienten, impfungen = [], []
    for pid in range(1, n + 1):
        # Hausarztpraxis: eher ältere Patienten -> Alter aus einer Beta-Verteilung, 18–95 Jahre
        alter = 18 + rng.beta(2.2, 1.8) * 77
        geb = stichtag - timedelta(days=int(alter * 365.25))
        einw = rng.choice(["sms", "email", "keine"], p=[0.6, 0.28, 0.12])
        fsme = int(rng.random() < 0.18)
        patienten.append((pid, rng.choice(VORNAMEN), rng.choice(NACHNAMEN), geb.isoformat(),
                          f"+49 151 0000{pid:04d}", f"patient{pid:04d}@example.org", einw, fsme))

        def impf(name: str, d: date) -> None:
            if geb + relativedelta(years=18) <= d <= stichtag:
                impfungen.append((pid, name, d.isoformat()))

        alt = int(alter)
        # Tetanus/Diphtherie: letzte Dosis 0–16 Jahre her, 7 % ohne Dokumentation
        if rng.random() > 0.07:
            impf("Tetanus/Diphtherie", stichtag - timedelta(days=int(rng.uniform(30, 16 * 365))))
        if alt >= 60:
            saison = _saisonstart(stichtag)
            if rng.random() < 0.5:   # Grippe in dieser Saison
                impf("Influenza", _tag(rng, saison - timedelta(days=30), stichtag))
            elif rng.random() < 0.7:  # nur letzte Saison
                impf("Influenza", _tag(rng, saison - relativedelta(years=1), saison - timedelta(days=270)))
            if rng.random() < 0.3:
                impf("COVID-19", _tag(rng, saison - timedelta(days=30), stichtag))
            if rng.random() < 0.45:
                impf("Pneumokokken", _tag(rng, stichtag - relativedelta(years=6), stichtag))
            r = rng.random()
            if r < 0.4:
                d1 = _tag(rng, stichtag - relativedelta(years=5), stichtag - timedelta(days=200))
                impf("Herpes zoster", d1)
                impf("Herpes zoster", d1 + timedelta(days=int(rng.integers(60, 180))))
            elif r < 0.55:            # nur 1. Dosis -> 2. Dosis fällig
                impf("Herpes zoster", _tag(rng, stichtag - timedelta(days=150), stichtag - timedelta(days=20)))
        if alt >= 75 and rng.random() < 0.3:
            impf("RSV", _tag(rng, stichtag - relativedelta(years=2), stichtag))
        if fsme and rng.random() < 0.85:
            impf("FSME", stichtag - timedelta(days=int(rng.uniform(60, 7 * 365))))

    conn.executemany("INSERT INTO patienten VALUES (?,?,?,?,?,?,?,?)", patienten)
    conn.executemany("INSERT INTO impfungen (patient_id, impfung, datum) VALUES (?,?,?)", impfungen)

    # Historie der letzten 12 Monate: Erinnerungen und ob danach ein Termin vereinbart wurde.
    # Rein synthetisch – die Quoten sind gesetzt, nicht gemessen.
    quote = {"sms": 0.44, "email": 0.31}
    mit_einw = [p for p in patienten if p[6] != "keine"]
    impfarten = ["Tetanus/Diphtherie", "Influenza", "COVID-19", "Pneumokokken", "Herpes zoster"]
    for _ in range(420):
        p = mit_einw[int(rng.integers(len(mit_einw)))]
        kanal, impfung = p[6], str(rng.choice(impfarten))
        gesendet = datetime.combine(_tag(rng, stichtag - relativedelta(months=12),
                                         stichtag - timedelta(days=35)), time(8, 0))
        empf = p[4] if kanal == "sms" else p[5]
        cur = conn.execute(
            "INSERT INTO erinnerungen (patient_id, impfung, faellig_am, kanal, empfaenger, "
            "nachricht, gesendet_am, status) VALUES (?,?,?,?,?,?,?,?)",
            (p[0], impfung, (gesendet.date() + timedelta(days=30)).isoformat(), kanal, empf,
             "(historische Testnachricht)", gesendet.isoformat(timespec="seconds"), "simuliert"))
        if rng.random() < quote[kanal]:
            termin = gesendet + timedelta(days=int(rng.gamma(2.0, 4.0)) % 30)
            conn.execute("INSERT INTO termine (patient_id, impfung, vereinbart_am, erinnerung_id) "
                         "VALUES (?,?,?,?)", (p[0], impfung, termin.isoformat(timespec="seconds"),
                                              cur.lastrowid))
    conn.commit()
    conn.close()
    return pfad


if __name__ == "__main__":
    print(f"Testdaten geschrieben: {erzeuge()}")
