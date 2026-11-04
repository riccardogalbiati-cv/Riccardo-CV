#!/usr/bin/env python3
"""Build Riccardo Galbiati's CV website from cv.json.

    python3 build.py   # writes index.html and Riccardo-Galbiati-CV.pdf
"""
import json
import subprocess
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
PDF_NAME = "Riccardo-Galbiati-CV.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

FONTS = "https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800&family=Nunito+Sans:ital,opsz,wght@0,6..12,400;0,6..12,600;0,6..12,700;1,6..12,400&display=swap"

CSS = """
/* Layout: banner with name and downloads, quick-facts strip, then a tabbed timeline beside a side column */
:root{
  --bg:#eceff2; --surface:#ffffff; --ink:#1f2933; --muted:#5f6b78; --line:#e1e6eb;
  --hero:#0e2235; --hero-2:#1a3650; --on-hero:#ffffff; --accent:#1d6b84; --accent-soft:#e3f0f4;
  --display:'Nunito',system-ui,-apple-system,sans-serif; --body:'Nunito Sans',system-ui,-apple-system,sans-serif;
}
@media screen and (prefers-color-scheme:dark){:root{
  --bg:#10161c; --surface:#18212a; --ink:#e8eef3; --muted:#a2afbc; --line:#2a3642;
  --hero:#0e2235; --hero-2:#1a3650; --accent:#7cc4da; --accent-soft:#1b3340; color-scheme:dark}}
*{margin:0;padding:0;box-sizing:border-box}
a{color:inherit}
ul,ol{list-style:none}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.6}

/* Banner */
.hero{background:var(--hero);color:var(--on-hero);position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;right:-120px;top:-120px;width:420px;height:420px;border-radius:50%;border:60px solid var(--hero-2);opacity:.7}
.hero-in{position:relative;z-index:1;max-width:1040px;margin:0 auto;padding:72px 16px 96px}
.eyebrow{font-family:var(--display);font-weight:700;font-size:.8rem;letter-spacing:.22em;text-transform:uppercase;opacity:.75}
h1{font-family:Georgia,'Times New Roman',serif;font-weight:400;font-size:clamp(2.6rem,8vw,4.8rem);line-height:1.05;letter-spacing:-.01em;margin:8px 0 18px}
.sub{font-family:var(--display);font-weight:700;font-size:clamp(1.1rem,2.4vw,1.35rem)}
.sub2{opacity:.8;margin-top:2px}
.btns{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.btn{font-family:var(--display);font-weight:700;font-size:.95rem;padding:10px 20px;border-radius:999px;text-decoration:none;border:1.5px solid rgba(255,255,255,.5);transition:transform .15s,background .2s}
.btn:hover{transform:translateY(-2px);background:rgba(255,255,255,.12)}
.btn.solid{background:#fff;color:var(--hero);border-color:#fff}
.btn.solid:hover{background:#e8f1f5}

/* Quick facts */
.stats{max-width:1040px;margin:-48px auto 0;padding:0 16px;position:relative;z-index:2}
.stats-in{background:var(--surface);border:1px solid var(--line);border-radius:18px;display:grid;grid-template-columns:repeat(4,1fr);box-shadow:0 10px 30px rgba(14,34,53,.08)}
.stat{padding:20px 22px;border-right:1px solid var(--line)}
.stat:last-child{border:0}
.stat b{display:block;font-family:var(--display);font-weight:800;font-size:1.7rem;color:var(--accent);line-height:1.1}
.stat span{font-size:.88rem;color:var(--muted)}

/* Body */
.wrap{max-width:1040px;margin:0 auto;padding:56px 16px 72px;display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:40px}
h2{font-family:var(--display);font-weight:800;font-size:1.05rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:14px}
.about{font-size:1.08rem;margin-bottom:40px;max-width:65ch}
.tabs{display:flex;gap:6px;border-bottom:1px solid var(--line);margin-bottom:24px;overflow-x:auto}
.tab{font-family:var(--display);font-weight:700;font-size:1rem;padding:10px 16px;border:0;background:none;color:var(--muted);cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-1px;white-space:nowrap}
.tab:hover{color:var(--ink)}
.tab[aria-selected="true"]{color:var(--ink);border-color:var(--accent)}
.panel-title,.print-only{display:none}
.mini{display:flex;flex-direction:column;padding:1.2mm 0;border-bottom:1px solid var(--line)}
.mini:last-child{border:0}
.mini b{font-family:var(--display);font-weight:800;line-height:1.25}
.mini span{color:var(--muted)}
.mini .mini-date{color:var(--accent);font-weight:700}

.tl{position:relative;padding-left:28px}
.tl::before{content:"";position:absolute;left:6px;top:8px;bottom:8px;width:2px;background:var(--line)}
.tl li{position:relative;margin-bottom:18px}
.dot{position:absolute;left:-28px;top:20px;width:14px;height:14px;border-radius:50%;background:var(--surface);border:3px solid var(--accent)}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:18px 20px;transition:border-color .2s,box-shadow .2s}
.card:hover{border-color:var(--accent);box-shadow:0 6px 18px rgba(14,34,53,.08)}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
h3{font-family:var(--display);font-weight:800;font-size:1.06rem;line-height:1.35}
.org{color:var(--muted);font-style:italic}
.date{font-size:.88rem;color:var(--accent);font-weight:700;margin:4px 0 6px}
.pill{font-family:var(--display);font-size:.72rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:4px 10px;border-radius:999px;background:var(--accent-soft);color:var(--accent);white-space:nowrap}
.pill.full{background:var(--accent);color:var(--surface)}
.card p{color:var(--muted);margin-top:6px}

/* Side column */
.box{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;margin-bottom:20px}
.box h2{font-size:.88rem;margin-bottom:10px}
.contact a,.contact span{display:block;padding:5px 0;overflow-wrap:anywhere}
.contact a{text-decoration:none;color:var(--accent)}
.contact a:hover{text-decoration:underline}
.contact span{color:var(--muted)}
.group{padding:10px 0;border-bottom:1px solid var(--line)}
.group:first-of-type{padding-top:0}
.group:last-child{border:0;padding-bottom:0}
.group b{display:block;font-family:var(--display);font-weight:800;font-size:.9rem;margin-bottom:8px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips li{font-size:.84rem;padding:3px 10px;border-radius:999px;background:var(--accent-soft);color:var(--ink);transition:background .15s,color .15s}
.chips li:hover{background:var(--accent);color:var(--surface)}
.lang{display:flex;justify-content:space-between;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);flex-wrap:wrap}
.lang:last-child{border:0}
.lang-name{font-weight:700}
.lang-level{color:var(--muted);font-size:.9rem}
footer{text-align:center;color:var(--muted);font-size:.85rem;padding:0 16px 40px}

@media screen and (max-width:860px){
  .wrap{grid-template-columns:minmax(0,1fr)}
  .stats-in{grid-template-columns:repeat(2,1fr)}
  .stat:nth-child(2){border-right:0}
  .stat:nth-child(-n+2){border-bottom:1px solid var(--line)}
  .hero-in{padding:56px 16px 88px}
}

/* One A4 page for the PDF: every tab's content shown, interactive parts hidden */
@page{size:A4;margin:0}
@media print{
  html{font-size:10.6px}
  body{background:var(--bg);font-size:8.2pt;line-height:1.32;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  .hero::after,.btns,.stats,.tabs,footer{display:none}
  .hero-in{max-width:none;padding:7mm 13mm 5mm}
  h1{font-size:30pt;margin:1mm 0 2mm}
  .eyebrow{font-size:7.5pt}
  .sub{font-size:12pt}
  .wrap{max-width:none;padding:5mm 13mm 0;grid-template-columns:minmax(0,1fr) 64mm;gap:7mm}
  .about{font-size:8.5pt;margin-bottom:3mm;max-width:none}
  h2{font-size:9.5pt;margin-bottom:2.5mm}
  #p-edu{display:none!important}
  #p-work{display:block!important;margin-top:3mm}
  .print-only,.panel-title{display:block}
  .tl li{margin-bottom:1.5mm}
  .dot{top:3.4mm;width:10px;height:10px;border-width:2.5px;left:-26px}
  .card{padding:1.8mm 3.5mm;border-radius:8px;box-shadow:none!important}
  .tl::before{top:3mm;bottom:3mm}
  h3{font-size:9.5pt}
  .date{margin:.5mm 0 0;font-size:8.5pt}
  .card p{margin-top:1mm}
  .box{font-size:8pt;line-height:1.3;padding:3mm 4mm;margin-bottom:2.5mm;border-radius:8px}
  aside .box:last-child{margin-bottom:0}
  .box h2{font-size:8.5pt;margin-bottom:2mm}
  .contact a,.contact span{padding:.4mm 0}
  .group{padding:1.4mm 0}
  .group b{font-size:8pt;margin-bottom:1mm}
  .chips{gap:.8mm}
  .chips li{font-size:7.2pt;padding:0 1.8mm}
  .lang{padding:.6mm 0}
  .mini{padding:.9mm 0}
  .card,.box{break-inside:avoid}
}
"""


def e(s):
    return escape(s or "")


def timeline(items):
    return '<ol class="tl">' + "".join(f'<li><div class="dot"></div><div class="card">{x}</div></li>' for x in items) + "</ol>"


def project(x):
    return f'<h3>{e(x["title"])}</h3><div class="org">{e(x["focus"])}</div><p>{e(x["summary"])}</p>'


def job(x):
    return (f'<div class="card-head"><div><h3>{e(x["role"])}</h3><div class="org">{e(x["organisation"])}</div></div>'
            f'<span class="pill{" full" if x["type"] == "Work" else ""}">{e(x["type"])}</span></div>'
            f'<div class="date">{e(x["dates"])}</div>'
            + (f'<p>{e(x["summary"])}</p>' if x.get("summary") else ""))


def render(cv):
    c = cv["contact"]
    projects = timeline(project(x) for x in cv["projects"])
    edu = timeline(f'<h3>{e(x["degree"])}</h3><div class="org">{e(x["institution"])}</div><div class="date">{e(x["dates"])}</div>'
                   for x in cv["education"])
    edu_print = "".join(f'<div class="mini"><b>{e(x["degree"])}</b><span>{e(x["institution"])}</span><span class="mini-date">{e(x["dates"])}</span></div>'
                        for x in cv["education"])
    work = timeline(job(x) for x in cv["experience"])
    skills = "".join(f'<div class="group"><b>{e(g["group"])}</b><ul class="chips">'
                     + "".join(f"<li>{e(s)}</li>" for s in g["items"]) + "</ul></div>"
                     for g in cv["skills"])
    langs = "".join(f'<div class="lang"><div class="lang-name">{e(l["language"])}</div><div class="lang-level">{e(l["level"])}</div></div>'
                    for l in cv["languages"])
    msc_year = cv["education"][0]["dates"].split()[-1]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(cv["name"])} — CV</title>
<meta name="description" content="{e(cv["name"])} — {e(cv["focus"])}. {e(cv["headline"])}, {e(cv["school"])}.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="hero"><div class="hero-in">
  <div class="eyebrow">Curriculum Vitae</div>
  <h1>{e(cv["name"])}</h1>
  <p class="sub">{e(cv["focus"])}</p>
  <p class="sub2">{e(cv["headline"])} · {e(cv["school"])}</p>
  <div class="btns"><a class="btn solid" href="{PDF_NAME}">Download PDF</a><a class="btn" href="{e(c["linkedin_url"])}">LinkedIn</a><a class="btn" href="mailto:{e(c["email"])}">Email me</a></div>
</div></header>
<div class="stats"><div class="stats-in">
  <div class="stat"><b>{len(cv["projects"])}</b><span>research projects</span></div>
  <div class="stat"><b>MSc</b><span>Erasmus, {msc_year}</span></div>
  <div class="stat"><b>{len(cv["languages"])}</b><span>languages</span></div>
  <div class="stat"><b>3</b><span>countries studied in</span></div>
</div></div>
<div class="wrap">
<main>
  <h2>About me</h2><p class="about">{e(cv["profile"])}</p>
  <div class="tabs" role="tablist" aria-label="Background">
    <button class="tab" role="tab" id="tab-proj" aria-selected="true" aria-controls="p-proj">Research projects</button>
    <button class="tab" role="tab" id="tab-edu" aria-selected="false" aria-controls="p-edu">Education</button>
    <button class="tab" role="tab" id="tab-work" aria-selected="false" aria-controls="p-work">Work &amp; volunteering</button>
  </div>
  <div role="tabpanel" id="p-proj" aria-labelledby="tab-proj"><h2 class="panel-title">Research projects</h2>{projects}</div>
  <div role="tabpanel" id="p-edu" aria-labelledby="tab-edu" hidden>{edu}</div>
  <div role="tabpanel" id="p-work" aria-labelledby="tab-work" hidden><h2 class="panel-title">Work &amp; volunteering</h2>{work}</div>
</main>
<aside>
  <div class="box contact"><h2>Contact</h2><span>{e(c["location"])}</span><a href="mailto:{e(c["email"])}">{e(c["email"])}</a><a href="tel:{e(c["phone"].replace(" ", ""))}">{e(c["phone"])}</a><a href="{e(c["linkedin_url"])}">LinkedIn: {e(c["linkedin_label"])}</a></div>
  <div class="box"><h2>Skills</h2>{skills}</div>
  <div class="box"><h2>Languages</h2>{langs}</div>
  <div class="box print-only"><h2>Education</h2>{edu_print}</div>
</aside>
</div>
<footer>© 2026 {e(cv["name"])}</footer>
<script>
const tabs=[...document.querySelectorAll('[role=tab]')];
tabs.forEach(t=>t.addEventListener('click',()=>tabs.forEach(x=>{{const on=x===t;x.setAttribute('aria-selected',on);document.getElementById(x.getAttribute('aria-controls')).hidden=!on;}})));
</script>
</body>
</html>
"""


def build_pdf():
    """Print index.html to PDF with headless Chrome (uses the page's print styles)."""
    if not Path(CHROME).exists():
        print(f"skipped {PDF_NAME}: Google Chrome not found")
        return
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={ROOT / PDF_NAME}",
                    (ROOT / "index.html").as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(PDF_NAME)


def main():
    cv = json.loads((ROOT / "cv.json").read_text(encoding="utf-8"))
    (ROOT / "index.html").write_text(render(cv), encoding="utf-8")
    print("index.html")
    build_pdf()


if __name__ == "__main__":
    main()
