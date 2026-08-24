import os

def create_journey_svg(is_dark=True):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    text_primary = "#F5F4F1" if is_dark else "#1A1917"
    text_muted = "#A6A29A" if is_dark else "#6E6A63"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#8B6F47"

    milestones = [
        {
            "year": "2026",
            "title": "KIRO HACKATHON",
            "sub": "Ship With Kiro",
            "desc": "Built CloudGuardian AI: an LLM-powered cloud monitoring tool with TypeScript &amp; FastAPI."
        },
        {
            "year": "2023 – PRESENT",
            "title": "SOFTWARE ENGINEERING",
            "sub": "UET Peshawar",
            "desc": "Studying systems programming, data structures, algorithms, and full-stack app development."
        }
    ]

    items_xml = ""
    my = 32

    for m in milestones:
        yr = m["year"]
        title = m["title"]
        sub = m["sub"]
        desc = m["desc"]

        items_xml += f'''<g transform="translate(30, {my})">
          <!-- Year Badge Anchor -->
          <rect x="0" y="0" width="118" height="26" rx="5" fill="rgba(139, 111, 71, 0.12)" stroke="{line_color}" stroke-width="1" />
          <text x="59" y="17" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11" font-weight="700" fill="{accent}" text-anchor="middle">{yr}</text>

          <!-- Timeline Structural Line -->
          <line x1="128" y1="13" x2="160" y2="13" stroke="{accent}" stroke-width="1.5" />
          <circle cx="160" cy="13" r="3.5" fill="{accent}" />

          <!-- Content Block -->
          <text x="175" y="17" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="{text_primary}" letter-spacing="0.5">{title} <tspan font-weight="500" fill="{text_muted}">— {sub}</tspan></text>
          <text x="175" y="38" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="400" fill="{text_muted}">{desc}</text>
        </g>\n'''
        my += 64

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 170" width="100%" height="100%">
  <title>Engineering Journey — Hamza Taif</title>

  <!-- Card Background -->
  <rect x="0" y="0" width="850" height="170" rx="8" fill="{bg}" stroke="{line_color}" stroke-width="1" />
  <rect x="0" y="0" width="3.5" height="170" fill="{accent}" />

  <!-- Vertical Timeline Connector -->
  <line x1="190" y1="45" x2="190" y2="110" stroke="{line_color}" stroke-width="1" stroke-dasharray="3,3" />

  <!-- Milestones -->
  {items_xml}
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    with open("assets/journey-dark.svg", "w", encoding="utf-8") as f:
        f.write(create_journey_svg(is_dark=True))
    with open("assets/journey-light.svg", "w", encoding="utf-8") as f:
        f.write(create_journey_svg(is_dark=False))
    print("Generated assets/journey-dark.svg and assets/journey-light.svg")

if __name__ == "__main__":
    main()
