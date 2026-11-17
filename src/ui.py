"""Optik im Stil der Portfolio-Homepage: dunkler Grund, Glas-Karten, Blau/Pfirsich-Akzente.

Nur HTML/CSS-Bausteine; die Logik bleibt in app.py und core.py.
"""
from __future__ import annotations

from html import escape

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600&display=swap');
:root{--bg:#06182F;--bg2:#0A2342;--surface:#0B2444;--ink:#F4F7FB;--muted:#A9B8CC;--dim:#7489A6;
  --lav:#8DBEF2;--peach:#F6A15E;--acc:#2F7BD6;--stroke:rgba(255,255,255,.09);
  --glass:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.015) 45%),#0B2444;
  --grad:linear-gradient(95deg,#F6A15E 0%,#F8BC86 100%)}
html,body,.stMarkdown,p,li,label,input,textarea{font-family:Geist,Inter,"Segoe UI",system-ui,sans-serif}
[data-testid="stIconMaterial"],.material-symbols-rounded{font-family:"Material Symbols Rounded"!important}
.stApp{background:#06182F;
  background-image:radial-gradient(1000px 520px at 50% -180px,rgba(26,100,184,.28),transparent 70%),
                   radial-gradient(720px circle at 15% 10%,rgba(47,123,214,.16),transparent 62%),
                   linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);
  background-size:auto,auto,56px 56px,56px 56px}
[data-testid="stSidebar"]{background:#0A2342;border-right:1px solid var(--stroke)}
[data-testid="stHeader"]{background:transparent}
h1,h2,h3{font-family:Geist,Inter,sans-serif!important;letter-spacing:-.02em}
.block-container{padding-top:2.2rem;max-width:1180px}
.kicker{display:inline-flex;align-items:center;font:600 12px/1 "Geist Mono",monospace;
  letter-spacing:.16em;text-transform:uppercase;color:var(--lav);padding:8px 14px;
  border:1px solid rgba(141,190,242,.3);background:rgba(141,190,242,.08);border-radius:999px;margin-bottom:16px}
.hero h1{font-size:clamp(36px,5vw,62px);line-height:1.04;margin:0 0 14px;font-weight:700;color:var(--ink)}
.grad{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.lead{font-size:17px;color:var(--muted);max-width:760px;margin:0 0 16px;line-height:1.6}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}
.pill{font:600 12px "Geist Mono",monospace;letter-spacing:.06em;color:var(--muted);
  padding:6px 12px;border:1px solid var(--stroke);border-radius:999px;background:var(--glass)}
.pill.warn{color:var(--peach);border-color:rgba(246,161,94,.4);background:rgba(246,161,94,.08)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:4px 0 18px}
@media(max-width:820px){.kpis{grid-template-columns:repeat(2,1fr)}}
.kpi,.card{background:var(--glass);border:1px solid var(--stroke);border-radius:18px;
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
.kpi{padding:16px 18px}
.kpi .v{font:700 32px Geist,sans-serif;color:var(--ink);line-height:1.1}
.kpi .l{font-size:13px;color:var(--muted);margin-top:4px}
.kpi.a .v{color:var(--peach)} .kpi.b .v{color:var(--lav)}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:8px 0 10px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:8px 0 10px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:8px 0 10px}
@media(max-width:820px){.grid3,.grid2,.grid4{grid-template-columns:1fr}}
.card{padding:18px 20px}
.card .big{font:700 34px Geist,sans-serif;line-height:1.1;margin-bottom:6px}
.card p{color:#D5DFEC;font-size:14.5px;margin:0;line-height:1.55}
.card h4{font:600 13px "Geist Mono",monospace;letter-spacing:.12em;text-transform:uppercase;
  margin:0 0 8px;color:var(--muted)}
.card.minus{border-color:rgba(169,184,204,.25)} .card.minus h4{color:var(--muted)}
.card.plus{border-color:rgba(246,161,94,.45);background:linear-gradient(120deg,rgba(246,161,94,.10),rgba(47,123,214,.10)),#0B2444}
.card.plus h4{color:var(--peach)}
.step .n{display:inline-flex;width:30px;height:30px;border-radius:50%;align-items:center;justify-content:center;
  font:700 14px Geist,sans-serif;background:var(--peach);color:#0A2342;margin-bottom:10px}
.step b{display:block;color:var(--ink);font-size:16px;margin-bottom:4px}
.section-t{font:700 26px Geist,sans-serif;color:var(--ink);margin:26px 0 6px}
.result .v{font:700 30px Geist,sans-serif;color:var(--peach)}
.stTabs [data-baseweb="tab-list"]{gap:6px;flex-wrap:wrap}
.stTabs [data-baseweb="tab"]{background:var(--glass);border:1px solid var(--stroke);border-radius:999px;
  padding:6px 14px;height:auto}
.stTabs [aria-selected="true"]{background:var(--ink)!important;color:#0A2342!important}
.stTabs [aria-selected="true"] p{color:#0A2342!important}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none}
[data-testid="stImage"] img,[data-testid="stPyplot"] img{border-radius:16px;border:1px solid var(--stroke)}
.box{border-radius:14px;padding:12px 16px;margin:6px 0 12px;font-size:14.5px;line-height:1.55;color:#E6EDF6;
  background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.015)),#0B2444;border:1px solid var(--stroke)}
.box b{color:var(--ink)}
.box.akzent{border-left:3px solid var(--peach);background:linear-gradient(90deg,rgba(246,161,94,.10),rgba(246,161,94,0) 60%),#0B2444}
.box.info{border-left:3px solid var(--lav)}
.kpis.k3{grid-template-columns:repeat(3,1fr);gap:10px}
.kpis.k3 .kpi{padding:14px 14px}.kpis.k3 .kpi .v{font-size:28px}
.liste{display:flex;flex-direction:column;gap:8px;margin:6px 0 14px}
.zeile{display:grid;grid-template-columns:1fr auto;gap:4px 12px;align-items:center;padding:12px 16px;border-radius:14px;
  background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.015)),#0B2444;border:1px solid var(--stroke)}
.zeile .n{font-weight:600;color:var(--ink)} .zeile .i{font-size:13.5px;color:var(--muted)}
.zeile .d{font:600 13px "Geist Mono",monospace;color:var(--peach);text-align:right}
.zeile .k{justify-self:end;font:600 11px "Geist Mono",monospace;letter-spacing:.06em;padding:3px 9px;border-radius:999px;
  border:1px solid rgba(141,190,242,.35);color:var(--lav);background:rgba(141,190,242,.08)}
.zeile .k.aus{border-color:var(--stroke);color:var(--dim);background:none}
.liste-t{font:600 12px "Geist Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--lav);margin:6px 0 8px}
div[data-testid="stDialog"] div[role="dialog"]{background:#0A2342;border:1px solid var(--stroke)}
.pass{display:flex;flex-direction:column;gap:10px;margin:6px 0 14px}
.pz{display:grid;grid-template-columns:minmax(150px,1.1fr) 2fr 210px;gap:6px 18px;align-items:center;padding:14px 18px;
  border-radius:16px;background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.015)),#0B2444;border:1px solid var(--stroke)}
@media(max-width:820px){.pz{grid-template-columns:1fr}}
.pz .t{font-weight:600;color:var(--ink)} .pz .h{font-size:12.5px;color:var(--dim);margin-top:2px}
.bahn{position:relative;height:8px;border-radius:99px;background:rgba(255,255,255,.07);margin:16px 0 18px}
.bahn .f{position:absolute;left:0;top:0;bottom:0;border-radius:99px}
.bahn .m{position:absolute;top:-5px;width:2px;height:18px;background:var(--ink);border-radius:2px}
.bahn .a,.bahn .e{position:absolute;top:14px;font:500 11px "Geist Mono",monospace;color:var(--dim);white-space:nowrap}
.bahn .a{left:0}.bahn .e{right:0}
.chip{justify-self:end;font:600 11px "Geist Mono",monospace;letter-spacing:.06em;padding:4px 10px;border-radius:999px;white-space:nowrap}
.chip.ueber{color:var(--peach);border:1px solid rgba(246,161,94,.45);background:rgba(246,161,94,.10)}
.chip.bald{color:var(--lav);border:1px solid rgba(141,190,242,.4);background:rgba(141,190,242,.08)}
.chip.ok{color:#9FDCC0;border:1px solid rgba(159,220,192,.35);background:rgba(159,220,192,.07)}
.chip.fertig{color:var(--muted);border:1px solid var(--stroke)}
.zeile.v{grid-template-columns:110px 1fr auto auto}
@media(max-width:820px){.zeile.v{grid-template-columns:1fr auto}}
.zeile .s{font:500 12.5px "Geist Mono",monospace;color:var(--dim)}
.mehr{font-size:13px;color:var(--dim);margin:-4px 0 12px}
.regel .big{font-size:22px!important;color:var(--ink)} .regel .rh{font:600 12px "Geist Mono",monospace;color:var(--peach);margin-bottom:8px}
.regel small{display:block;color:var(--dim);font-size:12px;margin-top:8px}
.foot{margin-top:40px;padding-top:22px;border-top:1px solid var(--stroke)}
.stack{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 14px}
.links a{display:inline-block;margin:0 8px 8px 0;padding:8px 14px;border-radius:999px;border:1px solid var(--stroke);
  background:var(--glass);color:var(--ink)!important;text-decoration:none;font-weight:600;font-size:14px}
.links a:hover{border-color:var(--peach);color:var(--peach)!important}
.quote{font:700 26px Geist,sans-serif;color:var(--lav)} .quote span{font-size:14px;color:var(--dim);font-weight:500}
</style>
"""


def hero(kicker: str, a: str, b: str, lead: str, pills: list[str], warn_pill: str) -> str:
    p = "".join(f'<span class="pill">{escape(x)}</span>' for x in pills)
    return (f'<div class="hero"><span class="kicker">{escape(kicker)}</span>'
            f'<h1>{escape(a)} <span class="grad">{escape(b)}</span></h1>'
            f'<p class="lead">{escape(lead)}</p>'
            f'<div class="pills"><span class="pill warn">🧪 {escape(warn_pill)}</span>{p}</div></div>')


def kpis(werte: list[tuple[str, str, str]], kompakt: bool = False) -> str:
    """werte: (Zahl, Beschriftung, Klasse 'a'|'b'|''); kompakt = eine Reihe, z. B. im Pop-up."""
    return f'<div class="kpis{" k3" if kompakt else ""}">' + "".join(
        f'<div class="kpi {k}"><div class="v">{escape(v)}</div><div class="l">{escape(l)}</div></div>'
        for v, l, k in werte) + "</div>"


def karten(eintraege: list[tuple[str, str]], spalten: int = 3, gross: bool = True) -> str:
    farben = ["var(--peach)", "var(--lav)", "var(--ink)"]
    innen = "".join(
        f'<div class="card"><div class="big" style="color:{farben[i % 3]}">{escape(t)}</div>'
        f'<p>{escape(x)}</p></div>' if gross else
        f'<div class="card"><h4>{escape(t)}</h4><p>{escape(x)}</p></div>'
        for i, (t, x) in enumerate(eintraege))
    return f'<div class="grid{spalten}">{innen}</div>'


def vergleich(ohne_t: str, ohne: str, mit_t: str, mit: str) -> str:
    return (f'<div class="grid2"><div class="card minus"><h4>{escape(ohne_t)}</h4><p>{escape(ohne)}</p></div>'
            f'<div class="card plus"><h4>{escape(mit_t)}</h4><p>{escape(mit)}</p></div></div>')


def schritte(eintraege: list[tuple[str, str]]) -> str:
    return '<div class="grid4">' + "".join(
        f'<div class="card step"><span class="n">{i}</span><b>{escape(t)}</b><p>{escape(x)}</p></div>'
        for i, (t, x) in enumerate(eintraege, 1)) + "</div>"


def titel(text: str) -> str:
    return f'<div class="section-t">{escape(text)}</div>'


def ergebnisse(werte: list[tuple[str, str]]) -> str:
    return '<div class="grid3">' + "".join(
        f'<div class="card result"><div class="v">{escape(v)}</div><p>{escape(l)}</p></div>'
        for v, l in werte) + "</div>"


def box(text: str, art: str = "info", icon: str = "") -> str:
    """Hinweiskasten in Homepage-Farben statt st.warning/st.info (gelb/blau passten nicht).
    art: 'akzent' (Pfirsich-Rand) oder 'info' (Blau-Rand). **fett** wird übernommen."""
    import re
    inhalt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escape(text)).replace("\n", "<br>")
    return f'<div class="box {art}">{icon + " " if icon else ""}{inhalt}</div>'


def liste(titel: str, zeilen: list[tuple[str, str, str, str, bool]]) -> str:
    """zeilen: (Name, Impfung, Datum, Kanal, erreichbar)"""
    innen = "".join(
        f'<div class="zeile"><span class="n">{escape(n)}</span><span class="d">{escape(d)}</span>'
        f'<span class="i">{escape(i)}</span><span class="k{"" if ok else " aus"}">{escape(k)}</span></div>'
        for n, i, d, k, ok in zeilen)
    return f'<div class="liste-t">{escape(titel)}</div><div class="liste">{innen}</div>'


STATUS_KLASSE = {"überfällig": "ueber", "bald fällig": "bald", "ok": "ok", "erledigt": "fertig"}


def impfpass(zeilen: list[dict]) -> str:
    """Digitaler Impfpass: je Impfung eine Karte mit Zeitstrahl letzte Dosis -> heute -> fällig.
    zeilen: dict(impfung, hinweis, status, status_text, start, ende, anteil, start_t, ende_t)
    anteil: Position von 'heute' zwischen letzter Dosis und Fälligkeit (0..1, None = keine Dosis)."""
    karten = []
    for z in zeilen:
        k = STATUS_KLASSE.get(z["status"], "fertig")
        farbe = {"ueber": "var(--peach)", "bald": "var(--lav)", "ok": "#9FDCC0", "fertig": "var(--muted)"}[k]
        anteil = z["anteil"]
        if anteil is None:
            bahn = (f'<div class="bahn" style="background:repeating-linear-gradient(90deg,rgba(246,161,94,.25) 0 6px,transparent 6px 12px)">'
                    f'<span class="a">{escape(z["start_t"])}</span></div>')
        else:
            breite = max(min(anteil, 1.0), 0.02) * 100
            marke = "" if k == "fertig" else f'<span class="m" style="left:{min(breite, 99.5):.1f}%"></span>'
            bahn = (f'<div class="bahn"><span class="f" style="width:{breite:.1f}%;background:{farbe};opacity:.75"></span>'
                    f'{marke}<span class="a">{escape(z["start_t"])}</span><span class="e">{escape(z["ende_t"])}</span></div>')
        karten.append(f'<div class="pz"><div><div class="t">{escape(z["impfung"])}</div>'
                      f'<div class="h">{escape(z["hinweis"])}</div></div>{bahn}'
                      f'<span class="chip {k}">{escape(z["status_text"])}</span></div>')
    return '<div class="pass">' + "".join(karten) + "</div>"


def faellig_liste(zeilen: list[tuple[str, str, str, str, str, str, bool]], mehr: str = "") -> str:
    """zeilen: (Name + Alter, Impfung, Datum, Status, Status-Text, Kanal, erreichbar)"""
    innen = "".join(
        f'<div class="zeile"><span class="n">{escape(n)}</span><span class="d">{escape(d)}</span>'
        f'<span class="i">{escape(i)} · <span class="chip {STATUS_KLASSE.get(s, "fertig")}" '
        f'style="padding:2px 8px">{escape(st)}</span></span>'
        f'<span class="k{"" if ok else " aus"}">{escape(k)}</span></div>'
        for n, i, d, s, st, k, ok in zeilen)
    return (f'<div class="liste">{innen}</div>' + (f'<div class="mehr">{escape(mehr)}</div>' if mehr else ""))


def protokoll(zeilen: list[tuple[str, str, str, str, str]], mehr: str = "") -> str:
    """zeilen: (Zeitpunkt, Name, Impfung, Kanal, Empfänger)"""
    innen = "".join(
        f'<div class="zeile v"><span class="s">{escape(t)}</span><span><span class="n">{escape(n)}</span> '
        f'<span class="i">· {escape(i)}</span></span><span class="s">{escape(e)}</span>'
        f'<span class="k">{escape(k)}</span></div>' for t, n, i, k, e in zeilen)
    return (f'<div class="liste">{innen}</div>' + (f'<div class="mehr">{escape(mehr)}</div>' if mehr else ""))


def regeln(eintraege: list[tuple[str, str, str, str]]) -> str:
    """eintraege: (Impfung, Rhythmus, Hinweis, Quelle)"""
    return '<div class="grid3">' + "".join(
        f'<div class="card regel"><div class="big">{escape(i)}</div><div class="rh">{escape(r)}</div>'
        f'<p>{escape(h)}</p><small>{escape(q)}</small></div>' for i, r, h, q in eintraege) + "</div>"


def quoten(eintraege: list[tuple[str, str, str]]) -> str:
    """eintraege: (Impfung, Quote Testdaten, Text mit RKI-Wert)"""
    return '<div class="grid4">' + "".join(
        f'<div class="card"><h4>{escape(i)}</h4><div class="quote">{escape(q)}</div><p>{escape(t)}</p></div>'
        for i, q, t in eintraege) + "</div>"


def fusszeile(titel_: str, text: str, stack: list[str], links: list[tuple[str, str]]) -> str:
    s = "".join(f'<span class="pill">{escape(x)}</span>' for x in stack)
    l = "".join(f'<a href="{escape(u)}" target="_blank" rel="noopener">{escape(t)}</a>' for t, u in links)
    return (f'<div class="foot"><span class="kicker">{escape(titel_)}</span>'
            f'<p class="lead">{escape(text)}</p><div class="stack">{s}</div><div class="links">{l}</div></div>')
