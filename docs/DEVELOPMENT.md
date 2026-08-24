# HT Profile Architecture & Development Guide

This repository powers the personal GitHub Profile README for **Hamza Taif**. It is designed as a self-contained engineering project featuring locally generated SVG graphics, GitHub API integration, dynamic language metrics, activity pulse tracking, and GitHub Actions automation.

---

## 🎨 Asset Architecture

All graphic components are generated as self-contained, theme-aware SVG assets supporting both **Dark Mode** (`*-dark.svg`) and **Light Mode** (`*-light.svg`):

| Asset Path | Generator Script | Description |
|---|---|---|
| `assets/hero-*.svg` | `scripts/hero.py` | Command typography hero banner with geometric HT monogram mark |
| `assets/project-*-*.svg` | `scripts/cards.py` | Case-study cards using `config/projects.json` & GitHub repo API |
| `assets/languages-*.svg` | `scripts/languages.py` | Repository code composition derived from public GitHub repos |
| `assets/pulse-*.svg` | `scripts/pulse.py` | GitHub activity rhythm timeline bars (Oct 2023 – 2026) |
| `assets/signature-*.svg` | `scripts/signature.py` | Understated HT signature mark for profile footer |

---

## 🛠️ Local Development & Regeneration

### 1. Regenerate All Assets
To run all Python generator scripts and update all SVG assets in `assets/`:

```bash
python scripts/generate_all.py
```

### 2. Local Visual Preview
Open `preview.html` in any web browser to inspect generated SVG graphics across dark (`#0D0C0A`) and light (`#FAF9F6`) canvas themes side-by-side:

```bash
# On Windows PowerShell
start preview.html
```

---

## 🖼️ Personal Portrait Generator (Optional)

A custom vector dot-matrix / halftone generator is included in `scripts/portrait.py`.

### How to generate your SVG portrait:
1. Prepare a clear photo of yourself as a PNG or JPG file.
2. Install Pillow (if not already installed):
   ```bash
   pip install Pillow
   ```
3. Run the generator script:
   ```bash
   python scripts/portrait.py path/to/your-photo.png assets/portrait.svg
   ```
4. Embed the generated `assets/portrait.svg` into `README.md`.

---

## ⚙️ Automated Updates (GitHub Actions)

The workflow `.github/workflows/update-profile.yml` runs **daily at midnight UTC** and can also be triggered manually via `workflow_dispatch`.

It uses the built-in `${{ secrets.GITHUB_TOKEN }}` to fetch updated repository metadata, recalculate code compositions, regenerate SVG assets, and commit changes back to the repository under `chore: refresh profile data`.
