"""Impf-Erinnerung / Vaccination Reminder – Streamlit-Prototyp mit synthetischen Testdaten.

Start:  streamlit run app.py
"""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import core  # noqa: E402
import testdaten  # noqa: E402
from i18n import SPRACHEN, Sprache  # noqa: E402
import charts  # noqa: E402
import ui  # noqa: E402
from vorschau import alle_diagramme  # noqa: E402

st.set_page_config(page_title="Impf-Erinnerung · Vaccination Reminder", page_icon="💉",
                   layout="wide")
st.markdown(ui.CSS, unsafe_allow_html=True)
charts.thema_dunkel()


@st.cache_resource
def verbindung():
    if not core.DB_PFAD.exists():       # auf Streamlit Cloud: beim ersten Start erzeugen
        testdaten.erzeuge()
    return core.verbinde()


conn = verbindung()

# --------------------------------------------------------------------------- Seitenleiste
_, oben = st.columns([5, 1.3])
code = oben.segmented_control("Sprache · Language", list(SPRACHEN), format_func=str.upper,
                              default="de", key="sprache", label_visibility="collapsed") or "de"
L = Sprache(code)

with st.sidebar:
    st.header(L.t("einstellungen"))
    stichtag = st.date_input(L.t("stichtag"), value=date.today(),
                             format="DD.MM.YYYY" if code == "de" else "YYYY-MM-DD")
    vorlauf_wochen = st.slider(L.t("vorlauf"), 2, 16, 8, help=L.t("vorlauf_hilfe"))
    st.caption(L.t("versand_simuliert"))
    if st.button(L.t("testdaten_neu")):
        conn.close()
        st.cache_resource.clear()
        testdaten.erzeuge(stichtag=stichtag)
        for k in [k for k in st.session_state if k != "sprache"]:
            del st.session_state[k]
        st.rerun()

df = core.faelligkeiten(conn, stichtag, vorlauf_wochen * 7)
faellig = df[df["status"].isin(core.STATUS_FAELLIG)]


def pass_zeilen(eintraege: pd.DataFrame) -> list[dict]:
    """Bereitet je Impfung den Zeitstrahl letzte Dosis -> heute -> fällig vor."""
    heute = pd.Timestamp(stichtag)
    reihenfolge = {"überfällig": 0, "bald fällig": 1, "ok": 2, "erledigt": 3}
    zeilen = []
    for r in eintraege.sort_values("status", key=lambda s: s.map(reihenfolge)).itertuples():
        start = pd.Timestamp(r.letzte_dosis) if pd.notna(r.letzte_dosis) else None
        ende = pd.Timestamp(r.faellig_am) if pd.notna(r.faellig_am) else None
        if r.status == "erledigt":
            anteil = 1.0
        elif start is not None and ende is not None and ende > start:
            anteil = (heute - start) / (ende - start)
        elif start is None:
            anteil = None
        else:
            anteil = 1.0
        fmt = L.datumsformat()
        zeilen.append(dict(
            impfung=L.impfung(r.impfung), hinweis=L.hinweis(r.impfung, r.hinweis), status=r.status,
            status_text=L.status(r.status) + (f" · {ende.strftime(fmt)}" if ende is not None and
                                              r.status != "erledigt" else ""),
            anteil=anteil, start_t=start.strftime(fmt) if start is not None else L.t("pass_nie"),
            ende_t=ende.strftime(fmt) if ende is not None else ""))
    return zeilen


def sende_und_melde(eintraege: pd.DataFrame) -> None:
    e = core.versende_erinnerungen(conn, eintraege, stichtag)
    st.session_state["meldung"] = L.t("meldung", gesendet=e.gesendet, ohne=e.ohne_einwilligung,
                                      gesperrt=e.gesperrt, tage=core.SPERRFRIST_TAGE)


# --------------------------------------------------------------------------- Popups
@st.dialog(L.t("popup_tag_titel"), width="large")
def popup_tag():
    st.markdown(ui.box(L.t("demo_hinweis"), "info", "🧪"), unsafe_allow_html=True)
    st.markdown(ui.kpis([
        (L.zahl((faellig["status"] == "überfällig").sum(), 0), L.t("ueberfaellig"), "a"),
        (L.zahl((faellig["status"] == "bald fällig").sum(), 0),
         L.t("faellig_in", wochen=vorlauf_wochen), "b"),
        (L.zahl(faellig["patient_id"].nunique(), 0), L.t("patienten_betroffen"), ""),
    ], kompakt=True), unsafe_allow_html=True)
    naechste = faellig[faellig["status"] == "bald fällig"].sort_values("faellig_am").head(8)
    st.markdown(ui.liste(L.t("als_naechstes").strip("*: "), [
        (r.name, L.impfung(r.impfung), pd.Timestamp(r.faellig_am).strftime(L.datumsformat()),
         L.kanal(r.einwilligung), r.einwilligung != "keine")
        for r in naechste.itertuples()]), unsafe_allow_html=True)
    if st.button(L.t("alle_erinnern"), type="primary"):
        sende_und_melde(faellig)
        st.rerun()


@st.dialog(L.t("popup_patient_titel"), width="large")
def popup_patient(pid: int):
    eintraege = faellig[faellig["patient_id"] == pid]
    p = eintraege.iloc[0]
    st.caption("🧪 " + L.t("demo_kurz"))
    st.markdown(ui.box(L.t("patient_warnung", name=p["name"], alter=p["alter"], anzahl=len(eintraege)),
                       "akzent"), unsafe_allow_html=True)
    st.markdown(ui.impfpass(pass_zeilen(eintraege)), unsafe_allow_html=True)
    if p["einwilligung"] == "keine":
        st.markdown(ui.box(L.t("keine_einwilligung"), "info"), unsafe_allow_html=True)
        return
    erste = eintraege.sort_values("faellig_am").iloc[0]
    vorname, nachname = p["name"].split(" ", 1)
    st.caption(L.t("vorschau", kanal=L.kanal(p["einwilligung"])))
    st.markdown(ui.box(core.nachricht(vorname, nachname, erste["impfung"], erste["faellig_am"], stichtag),
                       "info", "✉️"), unsafe_allow_html=True)
    if L.t("nachricht_sprache"):
        st.caption(L.t("nachricht_sprache"))
    if st.button(L.t("erinnerung_senden"), type="primary"):
        sende_und_melde(eintraege)
        st.rerun()


if "meldung" in st.session_state:
    st.toast(st.session_state.pop("meldung"), icon="✉️")

if not st.session_state.get("tagespopup_gezeigt") and len(faellig):
    st.session_state["tagespopup_gezeigt"] = True
    popup_tag()

# --------------------------------------------------------------------------- Inhalt
st.markdown(ui.hero(L.t("hero_kicker"), L.t("hero_a"), L.t("hero_b"), L.t("hero_lead"),
                    [L.t("pill_stiko"), L.t("pill_dsgvo"), L.datum(stichtag)], L.t("pill_demo")),
            unsafe_allow_html=True)
pat_faellig = faellig.drop_duplicates("patient_id")
n_ueber = int((faellig["status"] == "überfällig").sum())
erreichbar = (pat_faellig["einwilligung"] != "keine").mean() if len(pat_faellig) else 0
st.markdown(ui.kpis([
    (L.zahl(n_ueber, 0), L.t("k_ueber") + " · " + L.t(
        "k_ueber_sub", je=L.zahl(n_ueber / max(faellig.loc[faellig["status"] == "überfällig",
                                                            "patient_id"].nunique(), 1), 1)), "a"),
    (L.zahl((faellig["status"] == "bald fällig").sum(), 0), L.t("k_bald", wochen=vorlauf_wochen), "b"),
    (L.zahl(len(pat_faellig), 0), L.t("k_pat"), ""),
    (L.prozent(erreichbar, 0), L.t("k_erreich"), ""),
]), unsafe_allow_html=True)
st.caption("🧪 " + L.t("demo_hinweis"))

reiter = st.tabs(L.t("reiter").split("|"))

with reiter[0]:
    st.markdown(f'<span class="kicker">{L.t("w_kicker")}</span>', unsafe_allow_html=True)
    st.markdown(f"### {L.t('w_titel')}")
    st.markdown(ui.karten([(L.t("f1_wert"), L.t("f1_text")), (L.t("f2_wert"), L.t("f2_text")),
                           (L.t("f3_wert"), L.t("f3_text"))]), unsafe_allow_html=True)
    st.caption(L.t("quellen"))
    st.markdown(ui.titel(L.t("q_titel")), unsafe_allow_html=True)
    st.write(L.t("q_lead"))
    ab60_df = df[df["alter"] >= 60]
    st.markdown(ui.quoten([
        (L.impfung(i), L.prozent(ab60_df.loc[ab60_df["impfung"] == i, "status"]
                                 .isin(["ok", "erledigt"]).mean(), 0),
         L.t("q_text", rki=L.prozent(q, 0)))
        for i, q in testdaten.RKI.items()]), unsafe_allow_html=True)
    st.markdown(ui.vergleich(L.t("ohne_titel"), L.t("ohne"), L.t("mit_titel"), L.t("mit")),
                unsafe_allow_html=True)
    st.markdown(ui.titel(L.t("ablauf_titel")), unsafe_allow_html=True)
    st.markdown(ui.schritte([(L.t(f"s{i}_t"), L.t(f"s{i}")) for i in range(1, 5)]),
                unsafe_allow_html=True)

    st.markdown(ui.titel(L.t("r_titel")), unsafe_allow_html=True)
    st.write(L.t("r_lead"))
    alter = pd.read_sql("SELECT geburtsdatum FROM patienten", conn, parse_dates=["geburtsdatum"])
    ab60 = int(((pd.Timestamp(stichtag) - alter["geburtsdatum"]).dt.days / 365.25 >= 60).sum())
    r1, r2 = st.columns(2)
    n60 = r1.number_input(L.t("r_pat"), 10, 20000, max(ab60, 10), step=50)
    pp = r1.slider(L.t("r_pp"), 1, 20, 5, help=L.t("r_pp_hilfe"))
    euro = r2.number_input(L.t("r_euro"), 0.0, 100.0, 10.0, step=1.0, help=L.t("r_euro_hilfe"))
    minuten = r2.slider(L.t("r_min"), 1, 15, 3)
    zusaetzlich = round(n60 * pp / 100)   # ganze Patienten, damit € = Patienten × Vergütung aufgeht
    st.markdown(ui.ergebnisse([
        (L.zahl(zusaetzlich, 0), L.t("r_zus")),
        (f"{L.zahl(zusaetzlich * euro, 0)} €", L.t("r_umsatz")),
        (L.zahl(n60 * minuten / 60, 1), L.t("r_zeit")),
    ]), unsafe_allow_html=True)
    st.caption(L.t("r_hinweis"))

with reiter[1]:
    patienten = pd.read_sql("SELECT patient_id, vorname || ' ' || nachname AS name FROM patienten "
                            "ORDER BY nachname, vorname", conn)
    auswahl = st.selectbox(L.t("patient"), patienten["patient_id"],
                           format_func=dict(zip(patienten["patient_id"], patienten["name"])).get,
                           index=None, placeholder=L.t("name_eingeben"))
    if auswahl is not None:
        st.markdown(f'<div class="liste-t">{L.t("pass_titel")}</div>', unsafe_allow_html=True)
        st.markdown(ui.impfpass(pass_zeilen(df[df["patient_id"] == auswahl])),
                    unsafe_allow_html=True)
        if st.session_state.get("aufgerufen") != auswahl:
            st.session_state["aufgerufen"] = auswahl
            if auswahl in set(faellig["patient_id"]):
                popup_patient(auswahl)

with reiter[2]:
    status_filter = st.pills(L.t("status"), list(core.STATUS_FAELLIG), format_func=L.status,
                             selection_mode="multi", key="f_status")
    impf_filter = st.pills(L.t("impfung"), sorted(faellig["impfung"].unique()),
                           format_func=L.impfung, selection_mode="multi", key="f_impf")
    ansicht = faellig
    if impf_filter:
        ansicht = ansicht[ansicht["impfung"].isin(impf_filter)]
    if status_filter:
        ansicht = ansicht[ansicht["status"].isin(status_filter)]
    st.write(L.t("eintraege", n=len(ansicht), p=ansicht["patient_id"].nunique()))
    zeige = ansicht.sort_values("faellig_am").head(25)
    st.markdown(ui.faellig_liste([
        (f"{r.name} ({r.alter})", L.impfung(r.impfung),
         pd.Timestamp(r.faellig_am).strftime(L.datumsformat()), r.status, L.status(r.status),
         L.kanal(r.einwilligung), r.einwilligung != "keine") for r in zeige.itertuples()],
        L.t("mehr", n=L.zahl(len(ansicht) - len(zeige), 0)) if len(ansicht) > len(zeige) else ""),
        unsafe_allow_html=True)
    if st.button(L.t("eintraege_erinnern", n=len(ansicht)), disabled=ansicht.empty):
        sende_und_melde(ansicht)
        st.rerun()

with reiter[3]:
    protokoll = pd.read_sql("SELECT e.gesendet_am, p.vorname || ' ' || p.nachname AS name, "
                            "e.impfung, e.kanal, e.empfaenger, e.status, e.nachricht "
                            "FROM erinnerungen e JOIN patienten p USING (patient_id) "
                            "ORDER BY e.gesendet_am DESC LIMIT 500", conn)
    gesamt = pd.read_sql("SELECT kanal, COUNT(*) AS n FROM erinnerungen GROUP BY kanal", conn)
    je = dict(zip(gesamt["kanal"], gesamt["n"]))
    st.markdown(ui.kpis([(L.zahl(sum(je.values()), 0), L.t("proto_kpi_ges"), "a"),
                         (L.zahl(je.get("sms", 0), 0), L.t("proto_kpi_sms"), "b"),
                         (L.zahl(je.get("email", 0), 0), L.t("proto_kpi_mail"), "")], kompakt=True),
                unsafe_allow_html=True)
    zeige = protokoll.head(40)
    st.markdown(ui.protokoll([
        (pd.Timestamp(r.gesendet_am).strftime(L.datumsformat() + " %H:%M"), r.name,
         L.impfung(r.impfung), L.kanal(r.kanal), r.empfaenger) for r in zeige.itertuples()],
        L.t("mehr", n=L.zahl(len(protokoll) - len(zeige), 0)) if len(protokoll) > len(zeige) else ""),
        unsafe_allow_html=True)

with reiter[4]:
    for fig, satz in alle_diagramme(conn, df, stichtag, L).values():
        st.pyplot(fig)
        st.markdown(f"{L.t('aussage')} {satz}")
        st.divider()

with reiter[5]:
    st.markdown(ui.box(L.t("regeln_info"), "info"), unsafe_allow_html=True)
    regeln = core.lade_regeln()

    def rhythmus(r) -> str:
        a = int(r.mindestalter)
        if r.typ == "intervall":
            j = L.zahl(r.intervall_monate / 12, 0)
            text = (L.t("rh_intervall60", j=j, j60=L.zahl(r.intervall_monate_ab60 / 12, 0))
                    if pd.notna(r.intervall_monate_ab60) else L.t("rh_intervall", j=j, a=a))
        elif r.typ == "serie":
            text = L.t("rh_serie", d=int(r.dosen), a=a)
        else:
            text = L.t(f"rh_{r.typ}", a=a)
        return text + (L.t("rh_indikation") if r.nur_bei_indikation else "")

    st.markdown(ui.regeln([(L.impfung(r.impfung), rhythmus(r), L.hinweis(r.impfung, r.hinweis),
                            f"{r.quelle} · {r.stand}") for r in regeln.itertuples()]),
                unsafe_allow_html=True)

# --------------------------------------------------------------------------- Fußzeile
st.markdown(ui.fusszeile(
    L.t("f_titel"), L.t("f_text"),
    ["Python", "SQL · SQLite", "pandas", "Streamlit", "matplotlib", "STIKO-Regeln", "Wilson-KI", "pytest"],
    [(L.t("f_repo"), "https://github.com/denisetirrel-ops/vaccination-reminder"),
     (L.t("f_linkedin"), "https://www.linkedin.com/in/denise-tirrel/")]), unsafe_allow_html=True)
