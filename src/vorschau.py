"""Rendert alle Diagramme in beiden Sprachen als PNG nach vorschau/<sprache>/."""
import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import charts  # noqa: E402
import core  # noqa: E402
from i18n import SPRACHEN, Sprache  # noqa: E402


def alter_in_jahren(conn, stichtag: date) -> pd.Series:
    geb = pd.read_sql("SELECT geburtsdatum FROM patienten", conn, parse_dates=["geburtsdatum"])
    return ((pd.Timestamp(stichtag) - geb["geburtsdatum"]).dt.days / 365.25).astype(int)


def alle_diagramme(conn, df: pd.DataFrame, stichtag: date, L: Sprache) -> dict:
    return {
        "1_faellig_nach_monat": charts.faellig_nach_monat(df, stichtag, L),
        "2_status_je_impfung": charts.status_je_impfung(df, L),
        "3_terminquote": charts.terminquote(core.terminquote_je_kanal(conn), L),
        "4_altersverteilung": charts.altersverteilung(alter_in_jahren(conn, stichtag), L),
    }


def main(stichtag: date = date(2026, 11, 17)) -> None:
    conn = core.verbinde()
    df = core.faelligkeiten(conn, stichtag)
    for code in SPRACHEN:
        ziel = core.BASIS / "vorschau" / code
        ziel.mkdir(parents=True, exist_ok=True)
        for name, (fig, satz) in alle_diagramme(conn, df, stichtag, Sprache(code)).items():
            fig.savefig(ziel / f"{name}.png", dpi=110)
            print(f"[{code}] {name}: {satz}")


if __name__ == "__main__":
    main()
