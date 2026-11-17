import sys
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import core  # noqa: E402
import testdaten  # noqa: E402

STICHTAG = date(2026, 11, 17)


@pytest.fixture(scope="module")
def regeln():
    return core.lade_regeln().set_index("impfung", drop=False)


def faellig(regeln, impfung, geb, dosen, fsme=False, stichtag=STICHTAG):
    return core.berechne_faelligkeit(regeln.loc[impfung], geb, dosen, fsme, stichtag)


def test_tetanus_10_jahre(regeln):
    assert faellig(regeln, "Tetanus/Diphtherie", date(1980, 1, 1), [date(2017, 3, 5)]) == date(2027, 3, 5)


def test_tetanus_nie_geimpft_ab_18(regeln):
    assert faellig(regeln, "Tetanus/Diphtherie", date(1990, 6, 1), []) == date(2008, 6, 1)


def test_einmalig_erledigt(regeln):
    assert faellig(regeln, "Pneumokokken", date(1950, 1, 1), [date(2022, 1, 1)]) is None


def test_einmalig_erst_ab_mindestalter(regeln):
    assert faellig(regeln, "RSV", date(1955, 2, 1), []) == date(2030, 2, 1)


def test_zoster_zweite_dosis(regeln):
    assert faellig(regeln, "Herpes zoster", date(1950, 1, 1), [date(2026, 9, 1)]) == date(2026, 11, 1)
    assert faellig(regeln, "Herpes zoster", date(1950, 1, 1),
                   [date(2026, 1, 1), date(2026, 4, 1)]) is None


def test_influenza_saison(regeln):
    geb = date(1950, 1, 1)
    assert faellig(regeln, "Influenza", geb, [date(2025, 10, 20)]) == date(2026, 10, 1)   # offen
    assert faellig(regeln, "Influenza", geb, [date(2026, 10, 20)]) == date(2027, 10, 1)   # erledigt
    assert faellig(regeln, "Influenza", geb, [], stichtag=date(2026, 5, 1)) == date(2026, 10, 1)


def test_influenza_wird_erst_mit_60_faellig(regeln):
    assert faellig(regeln, "Influenza", date(1967, 3, 1), []) == date(2027, 3, 1)


def test_fsme_ab_60_kuerzeres_intervall(regeln):
    assert faellig(regeln, "FSME", date(1980, 1, 1), [date(2024, 1, 1)], fsme=True) == date(2029, 1, 1)
    assert faellig(regeln, "FSME", date(1950, 1, 1), [date(2024, 1, 1)], fsme=True) == date(2027, 1, 1)
    assert faellig(regeln, "FSME", date(1950, 1, 1), [date(2024, 1, 1)], fsme=False) is None


@pytest.mark.parametrize("faellig_am,erwartet", [
    (None, "erledigt"), (date(2026, 11, 1), "überfällig"),
    (date(2026, 12, 20), "bald fällig"), (date(2027, 6, 1), "ok")])
def test_status(faellig_am, erwartet):
    assert core.status_von(faellig_am, STICHTAG, 56) == erwartet


def test_wilson_ki():
    lo, hi = core.wilson_ki(44, 100)
    assert lo == pytest.approx(0.347, abs=0.002) and hi == pytest.approx(0.538, abs=0.002)


@pytest.fixture()
def db(tmp_path):
    pfad = testdaten.erzeuge(tmp_path / "test.db", n=150, stichtag=STICHTAG)
    conn = core.verbinde(pfad)
    yield conn
    conn.close()


def test_versand_einwilligung_und_sperrfrist(db):
    df = core.faelligkeiten(db, STICHTAG)
    faellige = df[df["status"].isin(core.STATUS_FAELLIG)]
    vorher = db.execute("SELECT COUNT(*) FROM erinnerungen").fetchone()[0]
    jetzt = datetime(2026, 11, 17, 9, 0)

    e1 = core.versende_erinnerungen(db, faellige, STICHTAG, jetzt=jetzt)
    ohne = (faellige["einwilligung"] == "keine").sum()
    assert e1.ohne_einwilligung == ohne
    assert e1.gesendet + e1.gesperrt == len(faellige) - ohne
    assert db.execute("SELECT COUNT(*) FROM erinnerungen").fetchone()[0] == vorher + e1.gesendet

    e2 = core.versende_erinnerungen(db, faellige, STICHTAG, jetzt=jetzt)  # sofort nochmal
    assert e2.gesendet == 0 and e2.gesperrt == e1.gesendet + e1.gesperrt


def test_keine_nachricht_an_patienten_ohne_einwilligung(db):
    df = core.faelligkeiten(db, STICHTAG)
    core.versende_erinnerungen(db, df, STICHTAG, jetzt=datetime(2026, 11, 17, 9, 0))
    n = db.execute("SELECT COUNT(*) FROM erinnerungen e JOIN patienten p USING (patient_id) "
                   "WHERE p.einwilligung = 'keine'").fetchone()[0]
    assert n == 0


def test_terminquote_ohne_doppelzaehlung(db):
    q = core.terminquote_je_kanal(db)
    assert set(q["kanal"]) == {"sms", "email"}
    assert (q["termine"] <= q["erinnerungen"]).all()
    assert q["erinnerungen"].sum() == db.execute("SELECT COUNT(*) FROM erinnerungen").fetchone()[0]


def test_nachricht_ohne_diagnose():
    text = core.nachricht("Anna", "Müller", "Tetanus/Diphtherie", date(2027, 1, 5), STICHTAG)
    assert "05.01.2027" in text and "Termin" in text
    assert len(text) < 200
