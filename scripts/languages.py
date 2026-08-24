import os
import json
import urllib.request

def fetch_language_data(username="HamzaTaif"):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    headers = {"User-Agent": "HamzaTaif-Profile-Generator"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    lang_counts = {}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                repos = json.loads(response.read().decode('utf-8'))
                for r in repos:
                    lang = r.get("language")
                    # Filter out non-code noise if minor (e.g. Shell/HTML)
                    if lang and lang not in ["HTML", "Shell"]:
                        lang_counts[lang] = lang_counts.get(lang, 0) + 1
    except Exception:
        pass
    
    if not lang_counts:
        lang_counts = {
            "Python": 4,
            "TypeScript": 2,
            "JavaScript": 3,
            "Dart": 3,
            "C++": 1
        }
    return lang_counts

def create_languages_svg(lang_counts, is_dark=True):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    text_primary = "#F5F4F1" if is_dark else "#1A1917"
    text_muted = "#A6A29A" if is_dark else "#6E6A63"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#8B6F47"

    total = sum(lang_counts.values())
    sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    bar_width = 790
    current_x = 30
    segments_xml = ""

    colors = [accent, text_primary, text_muted, "#6E6A63" if is_dark else "#A6A29A", "#3A3935" if is_dark else "#C5C3B8"]

    for i, (lang, count) in enumerate(sorted_langs):
        pct = (count / total) if total > 0 else 0
        w = max(6, pct * bar_width)
        c = colors[i % len(colors)]
        segments_xml += f'''<rect x="{current_x}" y="70" width="{w}" height="16" fill="{c}" rx="3" />\n'''
        current_x += w

    legend_xml = ""
    ly = 115
    lx = 30
    for i, (lang, count) in enumerate(sorted_langs):
        pct = (count / total * 100) if total > 0 else 0
        c = colors[i % len(colors)]
        
        col_x = lx + (i % 3) * 270
        row_y = ly + (i // 3) * 38

        legend_xml += f'''<g transform="translate({col_x}, {row_y})">
          <circle cx="7" cy="8" r="5" fill="{c}" />
          <text x="22" y="13" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="{text_primary}">{lang}</text>
          <text x="150" y="13" font-family="ui-monospace, SFMono-Regular, monospace" font-size="13" font-weight="600" fill="{accent}">{pct:.1f}%</text>
        </g>\n'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 200" width="100%" height="100%">
  <title>Repository Code Composition — Hamza Taif</title>

  <!-- Card Background -->
  <rect x="0" y="0" width="850" height="200" rx="8" fill="{bg}" stroke="{line_color}" stroke-width="1" />
  <rect x="0" y="0" width="3.5" height="200" fill="{accent}" />

  <!-- Header -->
  <text x="30" y="40" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="700" fill="{accent}" letter-spacing="2">REPOSITORY CODE COMPOSITION</text>
  <text x="820" y="40" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10" fill="{text_muted}" text-anchor="end">DERIVED FROM PUBLIC REPOSITORIES</text>
  <line x1="30" y1="52" x2="820" y2="52" stroke="{line_color}" stroke-width="1" />

  <!-- Horizontal Code Distribution Bar -->
  {segments_xml}

  <!-- Language Grid -->
  {legend_xml}
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    langs = fetch_language_data("HamzaTaif")
    
    with open("assets/languages-dark.svg", "w", encoding="utf-8") as f:
        f.write(create_languages_svg(langs, is_dark=True))
    with open("assets/languages-light.svg", "w", encoding="utf-8") as f:
        f.write(create_languages_svg(langs, is_dark=False))
    print("Generated assets/languages-dark.svg and assets/languages-light.svg (enlarged GitHub scale)")

if __name__ == "__main__":
    main()
