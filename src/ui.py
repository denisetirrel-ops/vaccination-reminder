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
div[data-testid="stDialog"] div[role="dialog"]{background:#0A2342;border:1px solid var(--stroke)}
</style>
"""


def hero(kicker: str, a: str, b: str, lead: str, pills: list[str], warn_pill: str) -> str:
    p = "".join(f'<span class="pill">{escape(x)}</span>' for x in pills)
    return (f'<div class="hero"><span class="kicker">{escape(kicker)}</span>'
            f'<h1>{escape(a)} <span class="grad">{escape(b)}</span></h1>'
            f'<p class="lead">{escape(lead)}</p>'
            f'<div class="pills"><span class="pill warn">🧪 {escape(warn_pill)}</span>{p}</div></div>')


def kpis(werte: list[tuple[str, str, str]]) -> str:
    """werte: (Zahl, Beschriftung, Klasse 'a'|'b'|'')"""
    return '<div class="kpis">' + "".join(
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
