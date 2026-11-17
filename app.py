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
with st.sidebar:
    code = st.radio("Sprache · Language", list(SPRACHEN), format_func=SPRACHEN.get,
                    horizontal=True, key="sprache")
    L = Sprache(code)
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


def anzeige(tab: pd.DataFrame) -> pd.DataFrame:
    """Für die Anzeige übersetzen und Datumsspalten formatieren (Daten bleiben unverändert)."""
    t = tab.copy()
    for spalte in ("letzte_dosis", "faellig_am"):
        t[spalte] = pd.to_datetime(t[spalte]).dt.strftime(L.datumsformat()).fillna("–")
    t["hinweis"] = [L.hinweis(i, h) for i, h in zip(t["impfung"], t["hinweis"])]
    t["impfung"] = t["impfung"].map(L.impfung)
    t["status"] = t["status"].map(L.status)
    t["einwilligung"] = t["einwilligung"].map(L.kanal)
    return t.rename(columns={"patient_id": L.t("sp_id"), "name": L.t("sp_name"),
                             "alter": L.t("sp_alter"), "impfung": L.t("impfung"),
                             "letzte_dosis": L.t("sp_letzte"), "faellig_am": L.t("sp_faellig"),
                             "status": L.t("status"), "einwilligung": L.t("sp_einwilligung"),
                             "hinweis": L.t("sp_hinweis")})


def spalten(*schluessel: str) -> list[str]:
    return [L.t(s) for s in schluessel]


def sende_und_melde(eintraege: pd.DataFrame) -> None:
    e = core.versende_erinnerungen(conn, eintraege, stichtag)
    st.session_state["meldung"] = L.t("meldung", gesendet=e.gesendet, ohne=e.ohne_einwilligung,
                                      gesperrt=e.gesperrt, tage=core.SPERRFRIST_TAGE)


# --------------------------------------------------------------------------- Popups
@st.dialog(L.t("popup_tag_titel"), width="large")
def popup_tag():
    st.warning(L.t("demo_hinweis"), icon="🧪")
    c1, c2, c3 = st.columns(3)
    c1.metric(L.t("ueberfaellig"), int((faellig["status"] == "überfällig").sum()))
    c2.metric(L.t("faellig_in", wochen=vorlauf_wochen), int((faellig["status"] == "bald fällig").sum()))
    c3.metric(L.t("patienten_betroffen"), faellig["patient_id"].nunique())
    st.write(L.t("als_naechstes"))
    naechste = faellig[faellig["status"] == "bald fällig"].sort_values("faellig_am").head(8)
    st.dataframe(anzeige(naechste)[spalten("sp_name", "impfung", "sp_faellig", "sp_einwilligung")],
                 hide_index=True, use_container_width=True)
    if st.button(L.t("alle_erinnern"), type="primary"):
        sende_und_melde(faellig)
        st.rerun()


@st.dialog(L.t("popup_patient_titel"), width="large")
def popup_patient(pid: int):
    eintraege = faellig[faellig["patient_id"] == pid]
    p = eintraege.iloc[0]
    st.caption("🧪 " + L.t("demo_kurz"))
    st.warning(L.t("patient_warnung", name=p["name"], alter=p["alter"], anzahl=len(eintraege)))
    st.dataframe(anzeige(eintraege)[spalten("impfung", "sp_letzte", "sp_faellig", "status",
                                            "sp_hinweis")],
                 hide_index=True, use_container_width=True)
    if p["einwilligung"] == "keine":
        st.info(L.t("keine_einwilligung"))
        return
    erste = eintraege.sort_values("faellig_am").iloc[0]
    vorname, nachname = p["name"].split(" ", 1)
    st.caption(L.t("vorschau", kanal=L.kanal(p["einwilligung"])))
    st.info(core.nachricht(vorname, nachname, erste["impfung"], erste["faellig_am"], stichtag))
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
erreichbar = (pat_faellig["einwilligung"] != "keine").mean() if len(pat_faellig) else 0
st.markdown(ui.kpis([
    (L.zahl((faellig["status"] == "überfällig").sum(), 0), L.t("k_ueber"), "a"),
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
        st.dataframe(anzeige(df[df["patient_id"] == auswahl])
                     [spalten("impfung", "sp_letzte", "sp_faellig", "status", "sp_hinweis")],
                     hide_index=True, use_container_width=True)
        if st.session_state.get("aufgerufen") != auswahl:
            st.session_state["aufgerufen"] = auswahl
            if auswahl in set(faellig["patient_id"]):
                popup_patient(auswahl)

with reiter[2]:
    c1, c2 = st.columns(2)
    impf_filter = c1.multiselect(L.t("impfung"), sorted(faellig["impfung"].unique()),
                                 format_func=L.impfung)
    status_filter = c2.multiselect(L.t("status"), list(core.STATUS_FAELLIG), format_func=L.status)
    ansicht = faellig
    if impf_filter:
        ansicht = ansicht[ansicht["impfung"].isin(impf_filter)]
    if status_filter:
        ansicht = ansicht[ansicht["status"].isin(status_filter)]
    st.write(L.t("eintraege", n=len(ansicht), p=ansicht["patient_id"].nunique()))
    st.dataframe(anzeige(ansicht.sort_values("faellig_am")), hide_index=True,
                 use_container_width=True)
    if st.button(L.t("eintraege_erinnern", n=len(ansicht)), disabled=ansicht.empty):
        sende_und_melde(ansicht)
        st.rerun()

with reiter[3]:
    protokoll = pd.read_sql("SELECT e.gesendet_am, p.vorname || ' ' || p.nachname AS name, "
                            "e.impfung, e.kanal, e.empfaenger, e.status, e.nachricht "
                            "FROM erinnerungen e JOIN patienten p USING (patient_id) "
                            "ORDER BY e.gesendet_am DESC LIMIT 500", conn)
    protokoll["gesendet_am"] = (pd.to_datetime(protokoll["gesendet_am"])
                                .dt.strftime(L.datumsformat() + " %H:%M"))
    protokoll["impfung"] = protokoll["impfung"].map(L.impfung)
    protokoll["kanal"] = protokoll["kanal"].map(L.kanal)
    st.dataframe(protokoll.rename(columns={
        "gesendet_am": L.t("sp_gesendet"), "name": L.t("sp_name"), "impfung": L.t("impfung"),
        "kanal": L.t("sp_kanal"), "empfaenger": L.t("sp_empfaenger"), "status": L.t("status"),
        "nachricht": L.t("sp_nachricht")}), hide_index=True, use_container_width=True)

with reiter[4]:
    for fig, satz in alle_diagramme(conn, df, stichtag, L).values():
        st.pyplot(fig)
        st.markdown(f"{L.t('aussage')} {satz}")
        st.divider()

with reiter[5]:
    st.info(L.t("regeln_info"))
    regeln = core.lade_regeln()
    regeln["hinweis"] = [L.hinweis(i, h) for i, h in zip(regeln["impfung"], regeln["hinweis"])]
    regeln["impfung"] = regeln["impfung"].map(L.impfung)
    st.dataframe(regeln[["impfung", "mindestalter", "typ", "intervall_monate",
                         "intervall_monate_ab60", "dosen", "hinweis", "quelle", "stand"]],
                 hide_index=True, use_container_width=True)
