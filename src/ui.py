"""Optik im Stil der Portfolio-Homepage: dunkler Grund, Glas-Karten, Blau/Pfirsich-Akzente.

Nur HTML/CSS-Bausteine; die Logik bleibt in app.py und core.py.
"""
from __future__ import annotations

from html import escape

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap');
:root{--ink:#F4F7FB;--muted:#A9A5BD;--dim:#7489A6;--lav:#8DBEF2;--peach:#F6A15E;
  --glass:rgba(255,255,255,.045);--stroke:rgba(255,255,255,.09);
  --grad:linear-gradient(100deg,#8DBEF2 0%,#F6A15E 100%)}
html,body,[class*="st-"],.stMarkdown,p,li,label{font-family:Inter,"Segoe UI",system-ui,sans-serif}
.stApp{background:#0E0D16;
  background-image:radial-gradient(600px 420px at 8% -5%,rgba(141,190,242,.20),transparent 70%),
                   radial-gradient(520px 380px at 95% 0%,rgba(246,161,94,.14),transparent 70%),
                   linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);
  background-size:auto,auto,56px 56px,56px 56px}
[data-testid="stSidebar"]{background:#14131F;border-right:1px solid var(--stroke)}
[data-testid="stHeader"]{background:transparent}
h1,h2,h3{font-family:"Space Grotesk",Inter,sans-serif!important;letter-spacing:-.02em}
.block-container{padding-top:2.2rem;max-width:1180px}
.kicker{display:inline-flex;align-items:center;font:600 12px/1 "JetBrains Mono",monospace;
  letter-spacing:.16em;text-transform:uppercase;color:var(--lav);padding:8px 14px;
  border:1px solid rgba(141,190,242,.3);background:rgba(141,190,242,.08);border-radius:999px;margin-bottom:16px}
.hero h1{font-size:clamp(36px,5vw,62px);line-height:1.04;margin:0 0 14px;font-weight:700;color:var(--ink)}
.grad{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.lead{font-size:17px;color:var(--muted);max-width:760px;margin:0 0 16px;line-height:1.6}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}
.pill{font:600 12px "JetBrains Mono",monospace;letter-spacing:.06em;color:var(--muted);
  padding:6px 12px;border:1px solid var(--stroke);border-radius:999px;background:var(--glass)}
.pill.warn{color:var(--peach);border-color:rgba(246,161,94,.4);background:rgba(246,161,94,.08)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:4px 0 18px}
@media(max-width:820px){.kpis{grid-template-columns:repeat(2,1fr)}}
.kpi,.card{background:var(--glass);border:1px solid var(--stroke);border-radius:18px;
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
.kpi{padding:16px 18px}
.kpi .v{font:700 32px "Space Grotesk",sans-serif;color:var(--ink);line-height:1.1}
.kpi .l{font-size:13px;color:var(--muted);margin-top:4px}
.kpi.a .v{color:var(--peach)} .kpi.b .v{color:var(--lav)}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:8px 0 10px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:8px 0 10px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:8px 0 10px}
@media(max-width:820px){.grid3,.grid2,.grid4{grid-template-columns:1fr}}
.card{padding:18px 20px}
.card .big{font:700 34px "Space Grotesk",sans-serif;line-height:1.1;margin-bottom:6px}
.card p{color:#D5DFEC;font-size:14.5px;margin:0;line-height:1.55}
.card h4{font:600 13px "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;
  margin:0 0 8px;color:var(--muted)}
.card.minus{border-color:rgba(246,161,94,.35)} .card.minus h4{color:var(--peach)}
.card.plus{border-color:rgba(141,190,242,.4);background:linear-gradient(120deg,rgba(141,190,242,.12),rgba(246,161,94,.06))}
.card.plus h4{color:var(--lav)}
.step .n{display:inline-flex;width:30px;height:30px;border-radius:50%;align-items:center;justify-content:center;
  font:700 14px "Space Grotesk",sans-serif;background:var(--ink);color:#0E0D16;margin-bottom:10px}
.step b{display:block;color:var(--ink);font-size:16px;margin-bottom:4px}
.section-t{font:700 26px "Space Grotesk",sans-serif;color:var(--ink);margin:26px 0 6px}
.result .v{font:700 30px "Space Grotesk",sans-serif;color:var(--peach)}
.stTabs [data-baseweb="tab-list"]{gap:6px;flex-wrap:wrap}
.stTabs [data-baseweb="tab"]{background:var(--glass);border:1px solid var(--stroke);border-radius:999px;
  padding:6px 14px;height:auto}
.stTabs [aria-selected="true"]{background:var(--ink)!important;color:#0E0D16!important}
.stTabs [aria-selected="true"] p{color:#0E0D16!important}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none}
[data-testid="stImage"] img,[data-testid="stPyplot"] img{border-radius:16px;border:1px solid var(--stroke)}
div[data-testid="stDialog"] div[role="dialog"]{background:#14131F;border:1px solid var(--stroke)}
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
