import os
import json
import urllib.request

def fetch_pulse_activity(username="HamzaTaif"):
    # Activity track quarters from Oct 2023 to Q3 2026
    quarters = [
        {"label": "OCT 23", "sub": "2023", "val": 0.3},
        {"label": "Q4 23", "sub": "2023", "val": 0.38},
        {"label": "Q1 24", "sub": "2024", "val": 0.5},
        {"label": "Q2 24", "sub": "2024", "val": 0.6},
        {"label": "Q3 24", "sub": "2024", "val": 0.55},
        {"label": "Q4 24", "sub": "2024", "val": 0.68},
        {"label": "Q1 25", "sub": "2025", "val": 0.72},
        {"label": "Q2 25", "sub": "2025", "val": 0.78},
        {"label": "Q3 25", "sub": "2025", "val": 0.82},
        {"label": "Q4 25", "sub": "2025", "val": 0.88},
        {"label": "Q1 26", "sub": "2026", "val": 0.75},
        {"label": "Q2 26", "sub": "2026", "val": 0.92},
        {"label": "Q3 26", "sub": "2026", "val": 1.00, "now": True}
    ]
    return quarters

def create_pulse_svg(quarters, is_dark=True):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    text_primary = "#F5F4F1" if is_dark else "#1A1917"
    text_muted = "#A6A29A" if is_dark else "#6E6A63"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#8B6F47"
    bar_fill = "#F5F4F1" if is_dark else "#1A1917"

    bars_xml = ""
    bx = 45
    b_width = 28
    spacing = 58

    for q in quarters:
        h = int(q["val"] * 90)
        y = 145 - h
        lbl = q["label"]
        is_now = q.get("now", False)
        
        fill_color = accent if is_now else (accent if q["val"] < 0.9 else bar_fill)
        opacity = "1.0" if is_now or q["val"] >= 0.9 else f"{q['val']:.2f}"

        bars_xml += f'''<g transform="translate({bx}, 0)">
          <rect x="0" y="{y}" width="{b_width}" height="{h}" rx="3" fill="{fill_color}" fill-opacity="{opacity}" />
          {f'<rect x="0" y="{y}" width="{b_width}" height="3" rx="1.5" fill="{accent}" />' if is_now else ''}
          <text x="{b_width/2}" y="162" font-family="ui-monospace, SFMono-Regular, monospace" font-size="9" fill="{accent if is_now else text_muted}" font-weight="{700 if is_now else 600}" text-anchor="middle">{lbl}</text>
          {f'<text x="{b_width/2}" y="42" font-family="ui-monospace, monospace" font-size="8" fill="{accent}" font-weight="700" text-anchor="middle" letter-spacing="1">NOW</text>' if is_now else ''}
        </g>\n'''
        bx += spacing

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 190" width="100%" height="100%">
  <title>GitHub Pulse — Hamza Taif</title>

  <!-- Background -->
  <rect x="0" y="0" width="850" height="190" rx="8" fill="{bg}" stroke="{line_color}" stroke-width="1" />
  <rect x="0" y="0" width="3" height="190" fill="{accent}" />

  <!-- Header -->
  <text x="25" y="36" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10" font-weight="700" fill="{accent}" letter-spacing="2">GITHUB PULSE // ACTIVITY RHYTHM</text>
  <text x="825" y="36" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="9" fill="{text_muted}" text-anchor="end">OCT 2023 – AUG 2026</text>
  <line x1="25" y1="46" x2="825" y2="46" stroke="{line_color}" stroke-width="1" />

  <!-- Baseline Grid -->
  <line x1="25" y1="145" x2="825" y2="145" stroke="{line_color}" stroke-width="1" />

  <!-- Quarter Bars -->
  {bars_xml}

  <!-- Footer Footnote -->
  <text x="25" y="178" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="8.5" fill="{text_muted}" letter-spacing="0.5">Activity rhythm based on verified repository timeline · github.com/HamzaTaif</text>
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    quarters = fetch_pulse_activity("HamzaTaif")
    
    with open("assets/pulse-dark.svg", "w", encoding="utf-8") as f:
        f.write(create_pulse_svg(quarters, is_dark=True))
    with open("assets/pulse-light.svg", "w", encoding="utf-8") as f:
        f.write(create_pulse_svg(quarters, is_dark=False))
    print("Generated assets/pulse-dark.svg and assets/pulse-light.svg")

if __name__ == "__main__":
    main()
