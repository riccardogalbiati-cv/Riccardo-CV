# Riccardo Galbiati

Personal CV website, hosted with GitHub Pages.

## Updating the CV

All CV content lives in `cv.json`. Edit it, then rebuild the website, PDFs and images:

```bash
python3 build.py
```

Then commit and push. The live site updates a minute or two later.

The designed PDF (`Riccardo-Galbiati-CV.pdf`, one A4 page) is the website printed with Google Chrome, so it matches the site's design. The ATS PDF is a plain single-column version for online application forms. Chrome must be installed.

## Files

| File | What it is |
|---|---|
| `cv.json` | All website content: profile, projects, education, experience, skills, languages |
| `build.py` | Builds the website and PDF from `cv.json` |
| `index.html` | Generated website. Don't edit by hand, as `build.py` overwrites it |
| `Riccardo-Galbiati-CV.pdf` | Generated designed PDF, linked from the **Download CV** buttons |
| `cv-ats.html`, `Riccardo-Galbiati-CV-ATS.pdf` | Generated plain ATS version, linked from **ATS version (PDF)** |
| `og-image.png` | Generated preview image shown when the link is shared |
| `favicon.svg`, `apple-touch-icon.png` | Generated "RG" browser and home-screen icons |

## GitHub Pages

Serve the site from the `main` branch, root folder (**Settings** > **Pages** > **Deploy from a branch**).
