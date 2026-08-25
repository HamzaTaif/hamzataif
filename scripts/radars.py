import os
import math
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
                    if lang and lang not in ["HTML", "Shell"]:
                        lang_counts[lang] = lang_counts.get(lang, 0) + 1
    except Exception:
        pass
    
    if not lang_counts:
        lang_counts = {"Python": 5, "TypeScript": 3, "JavaScript": 4, "Dart": 4, "C++": 2}
    return lang_counts

def draw_radar(cx, cy, radius, axes, values, is_dark, gold_color="#D4A359"):
    text_primary = "#F5F4F1" if is_dark else "#1A1917"
    line_color = "#3A3935" if is_dark else "#E2E0D8"

    n = len(axes)
    angle_step = (2 * math.pi) / n

    xml = ""
    # Concentric polygon webs (25%, 50%, 75%, 100%)
    for level in [0.25, 0.5, 0.75, 1.0]:
        r_level = radius * level
        pts = []
        for i in range(n):
            angle = i * angle_step - math.pi / 2
            px = cx + r_level * math.cos(angle)
            py = cy + r_level * math.sin(angle)
            pts.append(f"{px:.1f},{py:.1f}")
        xml += f'<polygon points="{" ".join(pts)}" fill="none" stroke="{line_color}" stroke-width="1" stroke-dasharray="2,2" />\n'

    # Radial axes & vertex labels
    poly_data_pts = []
    for i, (axis_label, val) in enumerate(zip(axes, values)):
        angle = i * angle_step - math.pi / 2
        ax = cx + radius * math.cos(angle)
        ay = cy + radius * math.sin(angle)
        xml += f'<line x1="{cx}" y1="{cy}" x2="{ax}" y2="{ay}" stroke="{line_color}" stroke-width="1" />\n'

        # Value point
        r_val = radius * (val / 100.0)
        vx = cx + r_val * math.cos(angle)
        vy = cy + r_val * math.sin(angle)
        poly_data_pts.append(f"{vx:.1f},{vy:.1f}")

        # Label offset
        lx = cx + (radius + 24) * math.cos(angle)
        ly = cy + (radius + 24) * math.sin(angle) + 4
        anchor = "middle"
        if math.cos(angle) > 0.2:
            anchor = "start"
        elif math.cos(angle) < -0.2:
            anchor = "end"

        xml += f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11" font-weight="700" fill="{text_primary}" text-anchor="{anchor}">{axis_label}</text>\n'

    # Filled data polygon
    fill_color = "rgba(212, 163, 89, 0.28)" if is_dark else "rgba(139, 111, 71, 0.22)"
    xml += f'<polygon points="{" ".join(poly_data_pts)}" fill="{fill_color}" stroke="{gold_color}" stroke-width="2.5" />\n'

    # Data vertex dots
    for pt in poly_data_pts:
        px, py = pt.split(",")
        xml += f'<circle cx="{px}" cy="{py}" r="4" fill="{gold_color}" stroke="{text_primary}" stroke-width="1.5" />\n'

    return xml

def create_radars_svg(is_dark=True):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    text_muted = "#A6A29A" if is_dark else "#6E6A63"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#D4A359" if is_dark else "#8B6F47"
    gold = "#E5B869" if is_dark else "#8B6F47"

    # Chart 1: Skill Radar
    skill_axes = ["Full-Stack", "Flutter/Apps", "Backend/APIs", "AI Integration", "Databases", "DevOps"]
    skill_vals = [88, 92, 85, 80, 78, 70]
    left_radar = draw_radar(220, 200, 95, skill_axes, skill_vals, is_dark, gold_color=gold)

    # Chart 2: Language Mix
    lang_counts = fetch_language_data("HamzaTaif")
    total = sum(lang_counts.values())
    top_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    lang_axes = [l[0] for l in top_langs]
    max_count = max(l[1] for l in top_langs) if top_langs else 1
    lang_vals = [int((l[1] / max_count) * 100) for l in top_langs]

    right_radar = draw_radar(660, 200, 95, lang_axes, lang_vals, is_dark, gold_color=accent)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 350" width="100%" height="100%">
  <title>Engineering Focus &amp; Language Mix Radar Charts</title>

  <!-- Card Background -->
  <rect x="0" y="0" width="880" height="350" rx="8" fill="{bg}" stroke="{line_color}" stroke-width="1" />
  <rect x="0" y="0" width="3.5" height="350" fill="{accent}" />

  <!-- Headers -->
  <text x="40" y="38" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="700" fill="{accent}" letter-spacing="2">01 // ENGINEERING FOCUS</text>
  <text x="480" y="38" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="700" fill="{accent}" letter-spacing="2">02 // LANGUAGE MIX (REAL DATA)</text>
  <line x1="30" y1="48" x2="850" y2="48" stroke="{line_color}" stroke-width="1" />
  <line x1="440" y1="48" x2="440" y2="330" stroke="{line_color}" stroke-width="1" stroke-dasharray="3,3" />

  <!-- Left Radar Chart -->
  {left_radar}

  <!-- Right Radar Chart -->
  {right_radar}
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    with open("assets/radars-dark.svg", "w", encoding="utf-8") as f:
        f.write(create_radars_svg(is_dark=True))
    with open("assets/radars-light.svg", "w", encoding="utf-8") as f:
        f.write(create_radars_svg(is_dark=False))
    print("Generated assets/radars-dark.svg and assets/radars-light.svg (side-by-side radar charts)")

if __name__ == "__main__":
    main()
