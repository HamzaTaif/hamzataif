# HT Profile Architecture & Development Guide

This repository powers the personal GitHub Profile README for **Hamza Taif**. It is designed as a self-contained engineering project featuring locally generated SVG graphics, GitHub API integration, dynamic language metrics, activity pulse tracking, and GitHub Actions automation.

---

## 🎨 Asset Architecture

All graphic components are generated as self-contained, theme-aware SVG assets supporting both **Dark Mode** (`*-dark.svg`) and **Light Mode** (`*-light.svg`):

| Asset Path | Generator Script | Description |
|---|---|---|
| `assets/hero-*.svg` | `scripts/hero.py` | Command typography hero banner with high-contrast `HAMZA TAIF` text & stipple portrait |
| `assets/project-*-*.svg` | `scripts/cards.py` | Enlarged case-study cards using `config/projects.json` & GitHub repo API |
| `assets/toolbox-*.svg` | `scripts/toolbox.py` | Restrained typographic technology strip for core stack |
| `assets/languages-*.svg` | `scripts/languages.py` | Repository code composition derived from public GitHub repos (filtered noise) |
| `assets/journey-*.svg` | `scripts/journey.py` | Restrained engineering milestone timeline |
| `assets/pulse-*.svg` | `scripts/pulse.py` | Repository update activity timeline bars (Oct 2023 – 2026) |
| `assets/signature-*.svg` | `scripts/signature.py` | Pure typographic signature mark for profile footer |

---

## 🛠️ Noise Filtering & Data Rules

### Code Composition Filtering:
- `scripts/languages.py` filters out repository noise (such as generated `HTML` or auto-generated `Shell` config) to focus strictly on primary authored software engineering languages (`Python`, `TypeScript`, `JavaScript`, `Dart`, `C++`).

### Repository Rhythm Semantics:
- `scripts/pulse.py` visualizes public repository creation and update activity timestamps. It explicitly states repository update activity in its header and footnote without claiming unverified commit streaks.

---

## 🛠️ Local Development & Regeneration

### 1. Regenerate All Assets
To run all Python generator scripts and update all SVG assets in `assets/`:

```bash
python scripts/generate_all.py
```

### 2. Local Visual Preview
Open `preview.html` in any web browser to inspect generated SVG graphics across dark (`#0D0C0A`) and light (`#FAF9F6`) canvas themes side-by-side at **actual GitHub width (880px)** and **Mobile width (380px)**:

```bash
# On Windows PowerShell
Invoke-Item preview.html
```

---

## 🖼️ Personal Portrait Generator

A custom vector dot-matrix / halftone generator is included in `scripts/portrait.py`.

### How to generate your SVG portrait:
1. Ensure your photo (`hamza.png`) is in the workspace.
2. Run the generator script:
   ```bash
   python scripts/portrait.py hamza.png
   ```
3. `scripts/hero.py` automatically incorporates the fine stipple matrix into `assets/hero-dark.svg` and `assets/hero-light.svg`.
