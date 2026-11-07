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
/* Layout: sticky top nav, centred intro, then full-width sections that the nav links scroll to */
:root{
  --bg:#eceff2; --surface:#ffffff; --ink:#1f2933; --muted:#5f6b78; --line:#e1e6eb;
  --hero:#0e2235; --accent:#1d6b84; --accent-soft:#e3f0f4; --nav:rgba(255,255,255,.9);
  --display:'Nunito',system-ui,-apple-system,sans-serif; --body:'Nunito Sans',system-ui,-apple-system,sans-serif;
  --serif:Georgia,'Times New Roman',serif;
}
@media screen and (prefers-color-scheme:dark){:root{
  --bg:#10161c; --surface:#18212a; --ink:#e8eef3; --muted:#a2afbc; --line:#2a3642;
  --hero:#0b1a29; --accent:#7cc4da; --accent-soft:#1b3340; --nav:rgba(24,33,42,.9); color-scheme:dark}}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
a{color:inherit;text-decoration:none}
ul,ol{list-style:none}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.6}
h1,h2,h3{font-family:var(--display)}
.btn{display:inline-block;font-family:var(--display);font-weight:700;font-size:.95rem;padding:10px 20px;border-radius:999px;border:1.5px solid var(--accent);color:var(--accent);transition:transform .15s,background .2s,color .2s}
.btn:hover{transform:translateY(-2px);background:var(--accent-soft)}
.btn.solid{background:var(--accent);color:var(--surface)}
.btn.solid:hover{filter:brightness(1.1);background:var(--accent)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips li{font-size:.86rem;padding:3px 11px;border-radius:999px;background:var(--accent-soft);transition:background .15s,color .15s}
.chips li:hover{background:var(--accent);color:var(--surface)}

/* Nav */
nav{position:sticky;top:0;z-index:10;background:var(--nav);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav-in{max-width:1080px;margin:0 auto;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:16px}
.brand{font-family:var(--display);font-weight:800;font-size:1.1rem;white-space:nowrap}
.links{display:flex;gap:26px;font-family:var(--display);font-weight:700;font-size:.93rem;color:var(--muted)}
.links a{padding:4px 0;border-bottom:2px solid transparent;transition:color .15s,border-color .15s}
.links a:hover,.links a.on{color:var(--ink);border-color:var(--accent)}
nav .btn{padding:8px 18px;font-size:.9rem}

/* Intro */
.intro{background:var(--surface);text-align:center;padding:104px 16px 96px;border-bottom:1px solid var(--line)}
.kicker{font-family:var(--display);font-weight:800;color:var(--accent);letter-spacing:.14em;text-transform:uppercase;font-size:.85rem}
h1{font-family:var(--serif);font-weight:400;font-size:clamp(3rem,9vw,5.6rem);line-height:1.02;letter-spacing:-.01em;margin:14px 0 8px}
.edu-line{color:var(--muted);font-weight:600;margin-bottom:22px}
.intro .profile{max-width:660px;margin:0 auto 30px;color:var(--muted);font-size:1.12rem}
.intro .btns{display:flex;justify-content:center;flex-wrap:wrap;gap:12px}
.print-contact{display:none}

/* Sections */
section{max-width:1080px;margin:0 auto;padding:88px 16px 0;scroll-margin-top:40px}
section > h2{font-size:clamp(1.8rem,4vw,2.3rem);line-height:1.2;margin-bottom:6px}
.lead{color:var(--muted);margin-bottom:32px;font-size:1.05rem}
.card{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:28px;transition:border-color .2s,box-shadow .2s,transform .2s}
.card:hover{border-color:var(--accent);box-shadow:0 10px 28px rgba(14,34,53,.08);transform:translateY(-2px)}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
/* With an odd number of projects, the first (the thesis) spans the full width */
.projects .grid2 > .card:first-child:nth-last-child(odd){grid-column:1/-1}
.card h3{font-size:1.2rem;line-height:1.3}
.focus{color:var(--accent);font-weight:700;font-size:.92rem;margin:2px 0 10px}
.card p{color:var(--muted)}

/* Education & experience: two lists side by side */
.list h3{font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin:0 0 6px}
.item{padding:14px 0;border-bottom:1px solid var(--line)}
.item:last-child{border:0;padding-bottom:0}
.item-head{display:flex;justify-content:space-between;align-items:baseline;gap:0 12px;flex-wrap:wrap}
.item b{font-family:var(--display);font-weight:800;font-size:1.05rem}
.item .when{color:var(--accent);font-weight:700;font-size:.9rem;white-space:nowrap}
.item .where{color:var(--muted)}
.item p{color:var(--muted);font-size:.95rem;margin-top:4px}
.pill{font-family:var(--display);font-size:.7rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:3px 9px;border-radius:999px;background:var(--accent-soft);color:var(--accent);margin-left:6px;vertical-align:2px}

/* Skills */
.grid4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.skill h3{font-size:1.05rem;margin:0 0 12px}
.langs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;margin-top:20px}
.lang{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:16px 20px}
.lang b{display:block;font-family:var(--display);font-weight:800;font-size:1.1rem}
.lang span{color:var(--muted);font-size:.92rem}

/* Contact band */
.contact{max-width:none;margin-top:96px;padding:80px 16px;background:var(--hero);color:#fff;text-align:center}
.contact h2{font-family:var(--serif);font-weight:400;font-size:clamp(2.2rem,6vw,3.4rem);margin-bottom:10px}
.contact .lead{color:rgba(255,255,255,.75);margin-bottom:28px}
.contact-links{display:flex;justify-content:center;flex-wrap:wrap;gap:12px;margin-bottom:26px}
.contact-links a{padding:10px 20px;border-radius:999px;border:1.5px solid rgba(255,255,255,.35);font-weight:700;transition:background .2s,border-color .2s}
.contact-links a:hover{background:rgba(255,255,255,.1);border-color:#fff}
.contact .btn.solid{background:#fff;color:var(--hero);border-color:#fff}
.contact .where{color:rgba(255,255,255,.6);margin-top:22px;font-size:.92rem}
footer{background:var(--hero);color:rgba(255,255,255,.5);text-align:center;font-size:.85rem;padding:0 16px 32px}

/* Animations: the intro rises in on load; sections, cards and chips rise in as they scroll into view.
   Hidden states only apply once JS has marked the page (.js), and never for reduced motion or print. */
@keyframes rise{from{opacity:0;transform:translateY(26px)}}
@keyframes pop{from{opacity:0;transform:scale(.7)}}
@keyframes grow{from{transform:scaleX(0)}}
@media screen and (prefers-reduced-motion:no-preference){
  .intro > *{animation:rise .8s cubic-bezier(.2,.7,.2,1) backwards}
  .intro > :nth-child(2){animation-delay:.1s}
  .intro > :nth-child(3){animation-delay:.2s}
  .intro > :nth-child(4){animation-delay:.3s}
  .intro > :nth-child(5){animation-delay:.42s}
  .js .reveal:not(.in){opacity:0}
  .js .reveal.in{animation:rise .7s cubic-bezier(.2,.7,.2,1) var(--d,0ms) backwards}
  .js .reveal.in .chips li{animation:pop .45s cubic-bezier(.3,1.5,.5,1) calc(var(--d,0ms) + 250ms + var(--i,0) * 45ms) backwards}
  .js .reveal.in .item{animation:rise .6s cubic-bezier(.2,.7,.2,1) calc(var(--d,0ms) + 150ms + var(--i,0) * 90ms) backwards}
  .js section > h2.reveal.in::after{content:"";display:block;width:56px;height:3px;border-radius:3px;background:var(--accent);margin-top:10px;transform-origin:left;animation:grow .7s cubic-bezier(.2,.7,.2,1) .25s backwards}
  .js .contact h2.reveal.in::after{margin:14px auto 0;background:rgba(255,255,255,.6)}
  nav{transition:box-shadow .3s}
  nav.scrolled{box-shadow:0 6px 24px rgba(14,34,53,.1)}
}

@media screen and (max-width:860px){
  .links{display:none}
  .intro{padding:72px 16px 64px}
  section{padding-top:64px}
  .grid2,.grid4{grid-template-columns:minmax(0,1fr)}
  .langs{grid-template-columns:repeat(2,minmax(0,1fr))}
  .card{padding:22px}
  .contact{margin-top:72px;padding:64px 16px}
}
@media screen and (max-width:420px){nav .btn{padding:7px 14px;font-size:.85rem}.brand{font-size:1rem}}

/* One A4 page for the PDF: same sections, compacted, interactive parts hidden */
@page{size:A4;margin:0}
@media print{
  html{font-size:10.4px}
  body{font-size:8.3pt;line-height:1.34;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  nav,.intro .btns,.contact,footer,.lead{display:none}
  .intro{padding:9mm 14mm 6mm}
  /* No letter-spacing or type pills in print, so ATS software reads headings and job titles as plain words */
  .kicker{font-size:7.5pt;letter-spacing:.02em}
  .list h3{letter-spacing:.02em}
  .pill{display:none}
  h1{font-size:32pt;margin:2mm 0 1mm}
  .edu-line{margin-bottom:2.5mm;font-size:8.8pt}
  .intro .profile{font-size:8.8pt;max-width:165mm;margin-bottom:2.5mm}
  .print-contact{display:flex;justify-content:center;flex-wrap:wrap;gap:1mm 5mm;font-size:8.4pt;color:var(--accent);font-weight:700}
  section{max-width:none;padding:4mm 14mm 0}
  section > h2{font-size:11.5pt;margin-bottom:2.2mm}
  .grid2,.grid4{gap:3mm}
  .card{padding:2.6mm 3.8mm;border-radius:10px;box-shadow:none!important;transform:none!important}
  .card h3{font-size:9.6pt;margin:0}
  .focus{font-size:8pt;margin:0 0 .8mm}
  .list h3{font-size:7.5pt;margin-bottom:.5mm}
  .item{padding:1.4mm 0}
  .item b{font-size:8.8pt}
  .item .when{font-size:8pt}
  .item p{font-size:8pt;margin-top:.3mm}
  .skill h3{font-size:8.8pt;margin-bottom:1.5mm}
  .chips{gap:1mm}
  .chips li{font-size:7.4pt;padding:.2mm 2mm}
  .langs{margin-top:3mm;gap:3mm}
  .lang{padding:1.8mm 3.5mm;border-radius:10px}
  .lang b{font-size:9pt}
  .lang span{font-size:7.8pt}
  .card,.lang{break-inside:avoid}
}
"""


def e(s):
    return escape(s or "")


def project(x):
    return (f'<article class="card"><h3>{e(x["title"])}</h3>'
            f'<div class="focus">{e(x["focus"])}</div><p>{e(x["summary"])}</p></article>')


def edu(x):
    return (f'<div class="item"><div class="item-head"><b>{e(x["degree"])}</b><span class="when">{e(x["dates"])}</span></div>'
            f'<div class="where">{e(x["institution"])}</div></div>')


def job(x):
    return (f'<div class="item"><div class="item-head"><b>{e(x["role"])}<span class="pill">{e(x["type"])}</span></b>'
            f'<span class="when">{e(x["dates"])}</span></div><div class="where">{e(x["organisation"])}</div>'
            + (f'<p>{e(x["summary"])}</p>' if x.get("summary") else "") + "</div>")


def render(cv):
    c = cv["contact"]
    tel = c["phone"].replace(" ", "")
    projects = "".join(project(x) for x in cv["projects"])
    education = "".join(edu(x) for x in cv["education"])
    work = "".join(job(x) for x in cv["experience"])
    skills = "".join(f'<div class="card skill"><h3>{e(g["group"])}</h3><ul class="chips">'
                     + "".join(f"<li>{e(s)}</li>" for s in g["items"]) + "</ul></div>"
                     for g in cv["skills"])
    langs = "".join(f'<div class="lang"><b>{e(l["language"])}</b><span>{e(l["level"])}</span></div>' for l in cv["languages"])

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
<script>document.documentElement.classList.add('js')</script>
<style>{CSS}</style>
</head>
<body>
<nav><div class="nav-in">
  <a class="brand" href="#top">{e(cv["name"])}</a>
  <div class="links"><a href="#projects">Projects</a><a href="#education">Education</a><a href="#skills">Skills</a><a href="#contact">Contact</a></div>
  <a class="btn solid" href="{PDF_NAME}">Download CV</a>
</div></nav>
<header class="intro" id="top">
  <div class="kicker">{e(cv["focus"])}</div>
  <h1>{e(cv["name"])}</h1>
  <p class="edu-line">{e(cv["headline"])} · {e(cv["school"])}</p>
  <p class="profile">{e(cv["profile"])}</p>
  <div class="btns"><a class="btn solid" href="#contact">Get in touch</a><a class="btn" href="#projects">See my research</a></div>
  <div class="print-contact"><span>{e(c["location"])}</span><span>{e(c["email"])}</span><span>{e(c["phone"])}</span><span>{e(c["linkedin_url"].split("//")[-1].removeprefix("www."))}</span></div>
</header>
<main>
<section id="projects" class="projects">
  <h2>Research projects</h2>
  <p class="lead">Quantitative and qualitative research from my MSc and pre-master at Erasmus University Rotterdam.</p>
  <div class="grid2">{projects}</div>
</section>
<section id="education">
  <h2>Education &amp; experience</h2>
  <p class="lead">Studies in Milan, Paris and Rotterdam.</p>
  <div class="grid2">
    <div class="card list"><h3>Education</h3>{education}</div>
    <div class="card list"><h3>Work &amp; volunteering</h3>{work}</div>
  </div>
</section>
<section id="skills">
  <h2>Skills &amp; languages</h2>
  <p class="lead">Research methods, marketing insight and the tools I use day to day.</p>
  <div class="grid4">{skills}</div>
  <div class="langs">{langs}</div>
</section>
<section id="contact" class="contact">
  <h2>Let's talk</h2>
  <p class="lead">Open to roles in market research, consumer insights and quantitative research.</p>
  <div class="contact-links"><a href="mailto:{e(c["email"])}">{e(c["email"])}</a><a href="tel:{e(tel)}">{e(c["phone"])}</a><a href="{e(c["linkedin_url"])}">LinkedIn</a></div>
  <a class="btn solid" href="{PDF_NAME}">Download CV (PDF)</a>
  <p class="where">Based in {e(c["location"])}</p>
</section>
</main>
<footer>© 2026 {e(cv["name"])}</footer>
<script>
const links=[...document.querySelectorAll('.links a')];
const io=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting)links.forEach(a=>a.classList.toggle('on',a.hash==='#'+x.target.id));}}),{{rootMargin:'-45% 0px -50% 0px'}});
document.querySelectorAll('section[id]').forEach(s=>io.observe(s));

// Scroll reveal: siblings are staggered, and chips and list items inside a card pop in one after another
const items=document.querySelectorAll('section > h2, section > .lead, .card, .lang, .contact > :not(h2):not(.lead)');
items.forEach(el=>{{el.classList.add('reveal');const sibs=[...el.parentElement.children].filter(x=>x.matches('.card,.lang'));if(sibs.includes(el))el.style.setProperty('--d',sibs.indexOf(el)*110+'ms');}});
document.querySelectorAll('.chips,.list').forEach(l=>[...l.querySelectorAll('li,.item')].forEach((x,i)=>x.style.setProperty('--i',i)));
const show=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting){{x.target.classList.add('in');show.unobserve(x.target);}}}}),{{rootMargin:'0px 0px -8% 0px'}});
document.querySelectorAll('.reveal').forEach(el=>show.observe(el));
const nav=document.querySelector('nav');
addEventListener('scroll',()=>nav.classList.toggle('scrolled',scrollY>8),{{passive:true}});
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
