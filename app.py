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
from vorschau import alle_diagramme  # noqa: E402

st.set_page_config(page_title="Impf-Erinnerung · Vaccination Reminder", page_icon="💉",
                   layout="wide")


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
st.title(L.t("titel"))
st.caption(L.t("untertitel", datum=L.datum(stichtag)))

reiter = st.tabs(L.t("reiter").split("|"))

with reiter[0]:
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

with reiter[1]:
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

with reiter[2]:
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

with reiter[3]:
    for fig, satz in alle_diagramme(conn, df, stichtag, L).values():
        st.pyplot(fig)
        st.markdown(f"{L.t('aussage')} {satz}")
        st.divider()

with reiter[4]:
    st.info(L.t("regeln_info"))
    regeln = core.lade_regeln()
    regeln["hinweis"] = [L.hinweis(i, h) for i, h in zip(regeln["impfung"], regeln["hinweis"])]
    regeln["impfung"] = regeln["impfung"].map(L.impfung)
    st.dataframe(regeln[["impfung", "mindestalter", "typ", "intervall_monate",
                         "intervall_monate_ab60", "dosen", "hinweis", "quelle", "stand"]],
                 hide_index=True, use_container_width=True)
