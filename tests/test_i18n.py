import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import core  # noqa: E402
from i18n import HINWEIS_EN, IMPFUNG_EN, STATUS_EN, TEXTE, Sprache  # noqa: E402


def test_beide_sprachen_haben_dieselben_schluessel():
    assert set(TEXTE["de"]) == set(TEXTE["en"])


def test_alle_impfungen_und_status_uebersetzt():
    impfungen = set(core.lade_regeln()["impfung"])
    assert impfungen == set(IMPFUNG_EN) == set(HINWEIS_EN)
    assert set(STATUS_EN) == {"überfällig", "bald fällig", "ok", "erledigt"}


def test_zahlenformat_je_sprache():
    assert Sprache("de").zahl(1234.5) == "1.234,5"
    assert Sprache("en").zahl(1234.5) == "1,234.5"
    assert Sprache("de").prozent(0.475) == "47,5 %"
    assert Sprache("en").prozent(0.475) == "47.5%"


def test_platzhalter_in_beiden_sprachen_gleich():
    import string
    felder = lambda s: {f for _, f, _, _ in string.Formatter().parse(s) if f}
    for k in TEXTE["de"]:
        assert felder(TEXTE["de"][k]) == felder(TEXTE["en"][k]), k


def test_datum():
    assert Sprache("de").datum(date(2026, 11, 17)) == "17.11.2026"
    assert Sprache("en").datum(date(2026, 11, 17)) == "17 Nov 2026"
