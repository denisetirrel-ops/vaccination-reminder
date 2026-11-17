"""Diagramme im einheitlichen Stil: Pastellfarben, Werte direkt beschriftet, Zahlenformat je Sprache.

Jede Funktion bekommt ein `Sprache`-Objekt und gibt (Figure, Aussagesatz) zurück, damit App
und README denselben Satz zeigen.
"""
from __future__ import annotations

from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from scipy.stats import gaussian_kde  # noqa: E402

from core import wilson_ki  # noqa: E402
from i18n import Sprache  # noqa: E402

PASTELL = {"blau": "#A7C7E7", "rosa": "#F4B6C2", "gruen": "#B5E3C1", "gelb": "#FBE3A1",
           "lila": "#CDB4DB", "grau": "#D9D9D9", "pfirsich": "#FFD1B3"}
DUNKEL = {"blau": "#3D6C99", "rosa": "#B5536A", "text": "#333333", "grau": "#777777",
          "kante": "white", "box": "white", "dichte": "#3D6C99"}
INNEN = "#1E1B2E"   # Beschriftung auf Pastellflächen – in beiden Themen dunkel
STATUS_FARBE = {"überfällig": PASTELL["rosa"], "bald fällig": PASTELL["gelb"],
                "ok": PASTELL["gruen"], "erledigt": PASTELL["blau"]}

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#BBBBBB", "axes.titleweight": "bold",
                     "axes.titlesize": 12, "figure.dpi": 110})


def thema_dunkel() -> None:
    """Dunkles Thema passend zur Portfolio-Homepage (für die App; README-Vorschau bleibt hell)."""
    DUNKEL.update({"blau": "#8DBEF2", "rosa": "#F6A15E", "text": "#E8ECF4", "grau": "#A9A5BD",
                   "kante": "#16152A", "box": "#16152A", "dichte": "#E2C4F2"})
    plt.rcParams.update({"figure.facecolor": "#16152A", "axes.facecolor": "#16152A",
                         "savefig.facecolor": "#16152A", "text.color": "#E8ECF4",
                         "axes.labelcolor": "#C9CFDB", "axes.titlecolor": "#F4F7FB",
                         "xtick.color": "#A9A5BD", "ytick.color": "#A9A5BD",
                         "axes.edgecolor": "#3A3850", "legend.labelcolor": "#E8ECF4"})


def _zahl_achse(ax, L: Sprache, nachkomma: int = 0) -> None:
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: L.zahl(v, nachkomma)))


def _testdaten_hinweis(fig, L: Sprache) -> None:
    fig.text(0.99, 0.01, L.t("testdaten"), ha="right", va="bottom",
             fontsize=8, color=DUNKEL["grau"], style="italic")


# --------------------------------------------------------------------------- 1
def faellig_nach_monat(df: pd.DataFrame, stichtag: date, L: Sprache, monate: int = 12):
    """Anzahl Fälligkeiten: bereits überfällig + je Monat der nächsten `monate` Monate."""
    offen = df[df["status"] != "erledigt"].copy()
    offen["faellig_am"] = pd.to_datetime(offen["faellig_am"])
    start = pd.Timestamp(stichtag)
    ueber = int((offen["faellig_am"] < start).sum())
    perioden = pd.period_range(start, periods=monate, freq="M")
    zukunft = offen[offen["faellig_am"] >= start]["faellig_am"].dt.to_period("M")
    je_monat = zukunft.value_counts().reindex(perioden, fill_value=0)
    labels = [f"{L.monat_kurz(p.month)}\n{str(p.year)[2:]}" for p in perioden]

    # Zwei Felder mit eigener Skala: der Rückstand würde die Monatswerte sonst plattdrücken
    fig, (ax0, ax) = plt.subplots(1, 2, figsize=(10.5, 4.6),
                                  gridspec_kw={"width_ratios": [1, 7]})
    for achse, xs, werte, farbe in [(ax0, [0], [ueber], PASTELL["rosa"]),
                                    (ax, range(monate), je_monat.tolist(), PASTELL["blau"])]:
        balken = achse.bar(xs, werte, color=farbe, edgecolor=DUNKEL["kante"], width=0.7)
        oben = max(werte) or 1
        for b, w in zip(balken, werte):
            achse.text(b.get_x() + b.get_width() / 2, b.get_height() + oben * 0.015,
                       L.zahl(w, 0), ha="center", va="bottom", fontsize=9, color=DUNKEL["text"])
        achse.set_ylim(0, oben * 1.15)
        _zahl_achse(achse, L)
    ax0.set_xticks([0], [L.t("d1_bereits")], fontsize=8.5)
    ax0.set_xlim(-0.6, 0.6)
    ax0.set_ylabel(L.t("d1_y"))
    ax.set_xticks(range(monate), labels, fontsize=8.5)
    ax.set_title(L.t("d1_naechste", n=monate), fontsize=10, fontweight="normal")
    ax0.set_title(L.t("d1_rueckstand"), fontsize=10, fontweight="normal")
    fig.suptitle(L.t("d1_titel", datum=L.datum(stichtag)), fontweight="bold", fontsize=12)
    _testdaten_hinweis(fig, L)
    fig.tight_layout()

    spitze = je_monat.idxmax()
    satz = L.t("d1_satz", ueber=L.zahl(ueber, 0), mittel=L.zahl(float(np.mean(je_monat))),
               monat=L.monat(spitze.month, spitze.year), spitze=L.zahl(je_monat.max(), 0),
               saison=L.t("d1_saison") if spitze.month == 10 else "")
    return fig, satz


# --------------------------------------------------------------------------- 2
def status_je_impfung(df: pd.DataFrame, L: Sprache):
    """Anteile je Status pro Impfung, mit Fallzahl."""
    reihenfolge = ["überfällig", "bald fällig", "ok", "erledigt"]
    tab = df.groupby(["impfung", "status"]).size().unstack(fill_value=0)
    tab = tab.reindex(columns=reihenfolge, fill_value=0)
    n = tab.sum(axis=1)
    anteil = tab.div(n, axis=0).sort_values("überfällig")
    tab, n = tab.loc[anteil.index], n.loc[anteil.index]

    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    links = np.zeros(len(anteil))
    namen = [L.impfung(i) for i in anteil.index]
    for status in reihenfolge:
        breite = anteil[status].to_numpy()
        ax.barh(namen, breite, left=links, color=STATUS_FARBE[status],
                edgecolor=DUNKEL["kante"], label=L.status(status))
        for i, (b, l) in enumerate(zip(breite, links)):
            if b >= 0.10:   # nur Segmente beschriften, die breit genug sind (keine Überlappung)
                ax.text(l + b / 2, i, f"{L.prozent(b, 0)}\n(n={tab[status].iloc[i]})",
                        ha="center", va="center", fontsize=8, color=INNEN)
        links += breite
    for i, gesamt in enumerate(n):
        bald = tab["bald fällig"].iloc[i]
        zusatz = (f"\n{L.t('d2_bald')}: {bald}"
                  if 0 < anteil["bald fällig"].iloc[i] < 0.10 else "")
        ax.text(1.01, i, f"n={gesamt}{zusatz}", va="center", fontsize=8, color=DUNKEL["grau"])
    ax.set_xlim(0, 1.13)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], [L.prozent(v, 0) for v in (0, 0.25, 0.5, 0.75, 1)])
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.1), frameon=False)
    ax.set_title(L.t("d2_titel"))
    _testdaten_hinweis(fig, L)
    fig.tight_layout()
    top = anteil["überfällig"].idxmax()
    satz = L.t("d2_satz", impfung=L.impfung(top), anteil=L.prozent(anteil.loc[top, "überfällig"], 0),
               n=tab.loc[top, "überfällig"], gesamt=n.loc[top])
    return fig, satz


# --------------------------------------------------------------------------- 3
def terminquote(quote: pd.DataFrame, L: Sprache, tage: int = 30):
    """Terminquote je Kanal mit 95-%-Konfidenzintervall (Wilson)."""
    q = quote.copy()
    q["anteil"] = q["termine"] / q["erinnerungen"]
    q[["ki_u", "ki_o"]] = [wilson_ki(t, n) for t, n in zip(q["termine"], q["erinnerungen"])]
    q["label"] = q["kanal"].map(L.kanal)

    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    x = np.arange(len(q))
    farben = [PASTELL["lila"], PASTELL["pfirsich"]][:len(q)]
    ax.bar(x, q["anteil"], color=farben, width=0.55, edgecolor=DUNKEL["kante"])
    ax.errorbar(x, q["anteil"], yerr=[q["anteil"] - q["ki_u"], q["ki_o"] - q["anteil"]],
                fmt="none", ecolor=DUNKEL["text"], capsize=6, lw=1.2)
    for xi, r in zip(x, q.itertuples()):
        ax.text(xi + 0.08, r.ki_o + 0.015,
                f"{L.prozent(r.anteil)}\n{L.t('d3_ki')} [{L.prozent(r.ki_u)}; {L.prozent(r.ki_o)}]",
                ha="left", va="bottom", fontsize=8.5, color=DUNKEL["text"])
        ax.text(xi, 0.02, L.t("d3_von", t=r.termine, n=r.erinnerungen),
                ha="center", va="bottom", fontsize=8.5, color=INNEN)
    ax.set_xticks(x, q["label"])
    ax.set_xlim(-0.5, len(q) - 0.5 + 0.35)
    ax.set_ylim(0, min(1, q["ki_o"].max() + 0.15))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: L.prozent(v, 0)))
    ax.set_ylabel(L.t("d3_y", tage=tage))
    ax.set_title(L.t("d3_titel"))
    _testdaten_hinweis(fig, L)
    fig.tight_layout()

    a, b = list(q.sort_values("anteil", ascending=False).itertuples())[:2]   # erwartet SMS + E-Mail
    satz = (L.t("d3_satz", a=a.label, pa=L.prozent(a.anteil), b=b.label, pb=L.prozent(b.anteil),
                tage=tage)
            + L.t("d3_ueberlapp" if a.ki_u <= b.ki_o else "d3_getrennt"))
    return fig, satz


# --------------------------------------------------------------------------- 4
def altersverteilung(alter: pd.Series, L: Sprache):
    """Histogramm plus Dichte der Patientenalter, Mittelwert und Median beschriftet."""
    werte = alter.to_numpy(dtype=float)
    mittel, median = werte.mean(), np.median(werte)
    fig, ax = plt.subplots(figsize=(9, 4.6))
    zaehl, _, balken = ax.hist(werte, bins=np.arange(15, 100, 5), color=PASTELL["blau"],
                               edgecolor=DUNKEL["kante"])
    for b, z in zip(balken, zaehl):
        if z:
            ax.text(b.get_x() + b.get_width() / 2, z + 0.5, L.zahl(z, 0), ha="center",
                    va="bottom", fontsize=8, color=DUNKEL["text"],
                    bbox=dict(boxstyle="round,pad=0.15", fc=DUNKEL["box"], ec="none", alpha=0.85))
    xs = np.linspace(15, 100, 300)
    dichte = gaussian_kde(werte)(xs) * len(werte) * 5   # auf Histogramm-Skala (Klassenbreite 5)
    ax.plot(xs, dichte, color=DUNKEL["dichte"], lw=2)
    hoehe = max(zaehl.max(), dichte.max())
    for wert, name, farbe, ha in [(mittel, L.t("d4_mittel"), DUNKEL["rosa"], "right"),
                                  (median, L.t("d4_median"), DUNKEL["text"], "left")]:
        ax.axvline(wert, color=farbe, ls="--", lw=1.2)
        ax.text(wert + (-0.6 if ha == "right" else 0.6), hoehe * 1.08,
                f"{name}\n{L.zahl(wert)} {L.t('d4_jahre')}",
                ha=ha, va="bottom", fontsize=8.5, color=farbe)
    anteil60 = (werte >= 60).mean()
    ax.text(99, hoehe * 1.2, L.t("d4_ab60", anteil=L.prozent(anteil60, 0), n=(werte >= 60).sum()),
            ha="right", va="bottom", fontsize=9, color=DUNKEL["text"])
    ax.text(97, dichte[-60] + hoehe * 0.06, L.t("d4_dichte"), ha="right", fontsize=8.5,
            color=DUNKEL["dichte"])
    ax.set_ylim(0, hoehe * 1.3)
    ax.set_xlabel(L.t("d4_x"))
    ax.set_ylabel(L.t("d4_y"))
    _zahl_achse(ax, L)
    ax.set_title(L.t("d4_titel", n=len(werte)))
    _testdaten_hinweis(fig, L)
    fig.tight_layout()
    satz = L.t("d4_satz", anteil=L.prozent(anteil60, 0), median=L.zahl(median))
    return fig, satz
