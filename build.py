#!/usr/bin/env python3
"""Build Riccardo Galbiati's CV website from cv.json.

    python3 build.py   # writes the website, both PDFs, the link-preview image and icons
"""
import json
import subprocess
import tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
PDF_NAME = "Riccardo-Galbiati-CV.pdf"
ATS_PDF_NAME = "Riccardo-Galbiati-CV-ATS.pdf"
SITE_URL = "https://riccardogalbiati-cv.github.io/Riccardo-CV/"
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
.nav-actions{display:flex;align-items:center;gap:10px}
/* Phone menu: the section links fold into a dropdown behind this button */
.menu-btn{display:none;width:38px;height:38px;border-radius:50%;border:1.5px solid var(--line);background:var(--surface);color:var(--ink);align-items:center;justify-content:center;cursor:pointer}
.menu-btn svg{width:18px;height:18px}
.menu-btn .x,nav.open .menu-btn .bars{display:none}
nav.open .menu-btn .x{display:block}

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
.card-head{display:flex;justify-content:space-between;align-items:baseline;gap:0 12px;flex-wrap:wrap}
.card-head .when{color:var(--muted);font-weight:700;font-size:.88rem;white-space:nowrap}
.focus{color:var(--accent);font-weight:700;font-size:.92rem;margin:2px 0 10px}
.card p{color:var(--muted)}
.tags{margin-top:14px}
.tags li{background:none;border:1px solid var(--line);color:var(--muted);font-size:.8rem;padding:2px 10px}

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
/* Certifications next to languages, which sit in two columns */
.extras{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:20px;align-items:start}
.langs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 28px}
.langs .item:nth-last-child(-n+2){border:0;padding-bottom:0}

/* Contact band */
.contact{max-width:none;margin-top:96px;padding:80px 16px;background:var(--hero);color:#fff;text-align:center}
.contact h2{font-family:var(--serif);font-weight:400;font-size:clamp(2.2rem,6vw,3.4rem);margin-bottom:10px}
.contact .lead{color:rgba(255,255,255,.75);margin-bottom:28px}
.contact-links{display:flex;justify-content:center;flex-wrap:wrap;gap:12px;margin-bottom:26px}
.contact-links a{padding:10px 20px;border-radius:999px;border:1.5px solid rgba(255,255,255,.35);font-weight:700;transition:background .2s,border-color .2s}
.contact-links a:hover{background:rgba(255,255,255,.1);border-color:#fff}
.contact .dl{display:flex;justify-content:center;flex-wrap:wrap;gap:12px}
.contact .btn.solid{background:#fff;color:var(--hero);border-color:#fff}
.contact .btn:not(.solid){color:#fff;border-color:rgba(255,255,255,.45)}
.contact .btn:not(.solid):hover{background:rgba(255,255,255,.1);border-color:#fff}
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
  .menu-btn{display:inline-flex}
  nav.open .links{display:flex;flex-direction:column;gap:0;position:absolute;top:100%;left:0;right:0;background:var(--surface);border-bottom:1px solid var(--line);box-shadow:0 12px 24px rgba(14,34,53,.12);padding:4px 16px 10px}
  nav.open .links a{padding:13px 0;border-bottom:1px solid var(--line);font-size:1rem}
  nav.open .links a:last-child{border-bottom:0}
  .intro{padding:72px 16px 64px}
  section{padding-top:64px}
  .grid2,.grid4{grid-template-columns:minmax(0,1fr)}
  .extras{grid-template-columns:minmax(0,1fr)}
  .card{padding:22px}
  .contact{margin-top:72px;padding:64px 16px}
}
@media screen and (max-width:420px){nav .btn{padding:7px 14px;font-size:.85rem}.brand{font-size:1rem}}

/* One A4 page for the PDF: same sections, compacted, interactive parts hidden */
@page{size:A4;margin:0}
@media print{
  html{font-size:10.4px}
  body{font-size:8.3pt;line-height:1.3;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  nav,.intro .btns,.contact,footer,.lead{display:none}
  .intro{padding:6.5mm 14mm 4.5mm}
  /* No letter-spacing or type pills in print, so ATS software reads headings and job titles as plain words */
  .kicker{font-size:7.5pt;letter-spacing:.02em}
  .list h3{letter-spacing:.02em}
  .pill{display:none}
  h1{font-size:32pt;margin:2mm 0 1mm}
  .edu-line{margin-bottom:2.5mm;font-size:8.8pt}
  .intro .profile{font-size:8.8pt;max-width:165mm;margin-bottom:2.5mm}
  .print-contact{display:flex;justify-content:center;flex-wrap:wrap;gap:1mm 5mm;font-size:8.4pt;color:var(--accent);font-weight:700}
  section{max-width:none;padding:2.8mm 14mm 0}
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
  .extras{margin-top:3mm;gap:3mm}
  .langs{gap:0 6mm}
  .card-head .when{font-size:8pt}
  .tags{display:none} /* shown on the website and in the ATS PDF; hidden here to keep one page */
  .card{break-inside:avoid}
}
"""


def e(s):
    return escape(s or "")


def project(x):
    return (f'<article class="card"><div class="card-head"><h3>{e(x["title"])}</h3><span class="when">{e(x.get("dates"))}</span></div>'
            f'<div class="focus">{e(x["focus"])}</div><p>{e(x["summary"])}</p>'
            + (f'<ul class="chips tags" aria-label="Tools and methods">' + "".join(f"<li>{e(t)}</li>" for t in x["tags"]) + "</ul>" if x.get("tags") else "")
            + "</article>")


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
    certs = "".join(f'<div class="item"><div class="item-head"><b>{e(x["name"])}</b><span class="where">{e(x["issuer"])}</span></div></div>' for x in cv.get("certifications", []))
    langs = "".join(f'<div class="item"><div class="item-head"><b>{e(l["language"])}</b><span class="when">{e(l["level"])}</span></div></div>' for l in cv["languages"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(cv["name"])} — CV</title>
<meta name="description" content="{e(cv["name"])} — {e(cv["focus"])}. {e(cv["headline"])}, {e(cv["school"])}.">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:title" content="{e(cv["name"])} — CV">
<meta property="og:description" content="{e(cv["focus"])}. {e(cv["headline"])}, {e(cv["school"])}.">
<meta property="og:image" content="{SITE_URL}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<script>document.documentElement.classList.add('js');
// Always open at the top: drop any #section from the address and don't restore the old scroll position
if('scrollRestoration' in history)history.scrollRestoration='manual';
if(location.hash)history.replaceState(null,'',location.pathname+location.search);
addEventListener('load',()=>scrollTo({{top:0,behavior:'instant'}}))</script>
<style>{CSS}</style>
</head>
<body>
<nav><div class="nav-in">
  <a class="brand" href="#top">{e(cv["name"])}</a>
  <div class="links"><a href="#projects">Projects</a><a href="#education">Education</a><a href="#skills">Skills</a><a href="#contact">Contact</a></div>
  <div class="nav-actions">
    <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false"><svg class="bars" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg><svg class="x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <a class="btn solid" href="{PDF_NAME}">Download CV</a>
  </div>
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
  <p class="lead">Quantitative and qualitative research from my MA and pre-master at Erasmus University Rotterdam.</p>
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
  <div class="extras">
    <div class="card list"><h3>Certifications &amp; coursework</h3>{certs}</div>
    <div class="card list"><h3>Languages</h3><div class="langs">{langs}</div></div>
  </div>
</section>
<section id="contact" class="contact">
  <h2>Let's talk</h2>
  <p class="lead">Open to roles in market research, consumer insights and quantitative research.</p>
  <div class="contact-links"><a href="mailto:{e(c["email"])}">{e(c["email"])}</a><a href="tel:{e(tel)}">{e(c["phone"])}</a><a href="{e(c["linkedin_url"])}">LinkedIn</a></div>
  <div class="dl"><a class="btn solid" href="{PDF_NAME}">Download CV (PDF)</a><a class="btn" href="{ATS_PDF_NAME}" title="Plain single-column version for online application forms">ATS version (PDF)</a></div>
  <p class="where">Based in {e(c["location"])}</p>
</section>
</main>
<footer>© 2026 {e(cv["name"])}</footer>
<script>
const nav=document.querySelector('nav'),menuBtn=document.querySelector('.menu-btn');
const links=[...document.querySelectorAll('.links a')];
const setMenu=open=>{{nav.classList.toggle('open',open);menuBtn.setAttribute('aria-expanded',open);}};
menuBtn.addEventListener('click',()=>setMenu(!nav.classList.contains('open')));
links.forEach(a=>a.addEventListener('click',()=>setMenu(false)));
addEventListener('keydown',ev=>{{if(ev.key==='Escape')setMenu(false);}});

const io=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting)links.forEach(a=>a.classList.toggle('on',a.hash==='#'+x.target.id));}}),{{rootMargin:'-45% 0px -50% 0px'}});
document.querySelectorAll('section[id]').forEach(s=>io.observe(s));

// Scroll reveal: siblings are staggered, and chips and list items inside a card pop in one after another
const items=document.querySelectorAll('section > h2, section > .lead, .card, .contact > :not(h2):not(.lead)');
items.forEach(el=>{{el.classList.add('reveal');const sibs=[...el.parentElement.children].filter(x=>x.matches('.card'));if(sibs.includes(el))el.style.setProperty('--d',sibs.indexOf(el)*110+'ms');}});
document.querySelectorAll('.chips,.list').forEach(l=>[...l.querySelectorAll('li,.item')].forEach((x,i)=>x.style.setProperty('--i',i)));
const show=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting){{x.target.classList.add('in');show.unobserve(x.target);}}}}),{{rootMargin:'0px 0px -8% 0px'}});
document.querySelectorAll('.reveal').forEach(el=>show.observe(el));
addEventListener('scroll',()=>nav.classList.toggle('scrolled',scrollY>8),{{passive:true}});
</script>
</body>
</html>
"""


ATS_CSS = """
@page{size:A4;margin:10mm 15mm}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;font-size:9.5pt;line-height:1.28;color:#000;max-width:180mm;margin:0 auto}
@media screen{body{padding:24px 16px}}
h1{font-size:20pt}
.sub{font-size:10.5pt;margin-top:1pt}
.contact{margin-top:3pt}
.contact span{white-space:nowrap}
h2{font-size:10.5pt;text-transform:uppercase;border-bottom:1px solid #000;padding-bottom:1pt;margin:7pt 0 3.5pt}
.entry{margin-bottom:3.5pt;break-inside:avoid}
.row{display:flex;justify-content:space-between;gap:12pt}
.row span{white-space:nowrap}
p{margin-top:1pt}
"""


def render_ats(cv):
    """Plain single-column CV for application portals: standard headings, one font, no columns or graphics."""
    c = cv["contact"]
    linkedin = c["linkedin_url"].split("//")[-1].removeprefix("www.")

    def entry(title, dates, *lines):
        return (f'<div class="entry"><div class="row"><b>{title}</b><span>{e(dates)}</span></div>'
                + "".join(f"<p>{l}</p>" for l in lines if l) + "</div>")

    education = "".join(entry(f'{e(x["degree"])}, {e(x["institution"])}', x["dates"]) for x in cv["education"])
    projects = "".join(entry(f'{e(x["title"])} | {e(x["focus"])}', x.get("dates"), e(x["summary"]),
                             "Tools and methods: " + e(", ".join(x["tags"])) if x.get("tags") else "")
                       for x in cv["projects"])
    work = "".join(entry(f'{e(x["role"])}, {e(x["organisation"])}', x["dates"], e(x.get("summary"))) for x in cv["experience"])
    skills = "".join(f'<p><b>{e(g["group"])}:</b> {e(", ".join(g["items"]))}</p>' for g in cv["skills"])
    certs = "".join(f'<p>{e(x["name"])}, {e(x["issuer"]).replace(" · ", ", ")}</p>' for x in cv.get("certifications", []))
    langs = e(", ".join(f'{l["language"]} ({l["level"]})' for l in cv["languages"]))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{e(cv["name"])} — CV (ATS version)</title>
<style>{ATS_CSS}</style>
</head>
<body>
<h1>{e(cv["name"])}</h1>
<p class="sub">{e(cv["focus"])}</p>
<p class="contact">{" | ".join(f"<span>{e(v)}</span>" for v in (c["location"], c["phone"], c["email"], linkedin))}</p>
<h2>Profile</h2>
<p>{e(cv["profile"])}</p>
<h2>Education</h2>
{education}
<h2>Research Projects</h2>
{projects}
<h2>Experience</h2>
{work}
<h2>Skills</h2>
{skills}
<h2>Certifications</h2>
{certs}
<h2>Languages</h2>
<p>{langs}</p>
</body>
</html>
"""


ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="{rx}" fill="#0e2235"/><text x="32" y="42.5" text-anchor="middle" font-family="Georgia,'Times New Roman',serif" font-size="29" fill="#ffffff">RG</text></svg>"""


def og_image_html(cv):
    """1200×630 card shown when the link is shared on LinkedIn, WhatsApp, email and so on."""
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><link href="{FONTS}" rel="stylesheet"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#0e2235;color:#fff;font-family:'Nunito Sans',sans-serif;padding:84px 96px;display:flex;flex-direction:column;position:relative;overflow:hidden}}
body::after{{content:"";position:absolute;right:-160px;top:-160px;width:560px;height:560px;border-radius:50%;border:2px solid rgba(124,196,218,.18)}}
.mark{{width:76px;height:76px;border-radius:14px;box-shadow:0 0 0 2px rgba(255,255,255,.28)}}
.kicker{{font-family:'Nunito',sans-serif;font-weight:800;color:#7cc4da;letter-spacing:.14em;text-transform:uppercase;font-size:22px;margin-top:auto}}
h1{{font-family:Georgia,'Times New Roman',serif;font-weight:400;font-size:104px;line-height:1.05;margin:18px 0 16px}}
.sub{{font-size:28px;color:rgba(255,255,255,.78);font-weight:600}}
</style></head><body>
{ICON_SVG.replace('<svg ', '<svg class="mark" ').format(rx=14)}
<div class="kicker">{e(cv["focus"])}</div>
<h1>{e(cv["name"])}</h1>
<div class="sub">{e(cv["headline"])} · {e(cv["school"])}</div>
</body></html>"""


def chrome(*args):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=8000", *args],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def print_pdf(html_name, pdf_name):
    """Print a page to PDF with headless Chrome (uses the page's print styles)."""
    chrome("--no-pdf-header-footer", f"--print-to-pdf={ROOT / pdf_name}", (ROOT / html_name).as_uri())
    print(pdf_name)


def screenshot(html, png_name, width, height):
    with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as f:
        f.write(html)
    try:
        chrome(f"--window-size={width},{height}", f"--screenshot={ROOT / png_name}", Path(f.name).as_uri())
    finally:
        Path(f.name).unlink()
    print(png_name)


def build_images(cv):
    (ROOT / "favicon.svg").write_text(ICON_SVG.format(rx=14), encoding="utf-8")
    print("favicon.svg")
    # iOS rounds the corners itself, so the touch icon is a full square
    screenshot(f'<body style="margin:0">{ICON_SVG.format(rx=0).replace("<svg ", "<svg width=180 height=180 ")}</body>',
               "apple-touch-icon.png", 180, 180)
    screenshot(og_image_html(cv), "og-image.png", 1200, 630)


def main():
    cv = json.loads((ROOT / "cv.json").read_text(encoding="utf-8"))
    (ROOT / "index.html").write_text(render(cv), encoding="utf-8")
    (ROOT / "cv-ats.html").write_text(render_ats(cv), encoding="utf-8")
    print("index.html\ncv-ats.html")
    if not Path(CHROME).exists():
        print("skipped PDFs and images: Google Chrome not found")
        return
    print_pdf("index.html", PDF_NAME)
    print_pdf("cv-ats.html", ATS_PDF_NAME)
    build_images(cv)


if __name__ == "__main__":
    main()
