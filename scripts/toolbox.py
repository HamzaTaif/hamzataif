import os

def create_toolbox_svg(is_dark=True):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    text_primary = "#F5F4F1" if is_dark else "#1A1917"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#D4A359" if is_dark else "#8B6F47"

    techs = [
        {"name": "C++", "color": "#00599C", "bg": "rgba(0, 89, 156, 0.14)"},
        {"name": "JavaScript", "color": "#F7DF1E", "bg": "rgba(247, 223, 30, 0.14)"},
        {"name": "TypeScript", "color": "#3178C6", "bg": "rgba(49, 120, 198, 0.14)"},
        {"name": "React", "color": "#61DAFB", "bg": "rgba(97, 218, 251, 0.14)"},
        {"name": "Next.js", "color": "#F5F4F1" if is_dark else "#1A1917", "bg": "rgba(255, 255, 255, 0.10)" if is_dark else "rgba(0, 0, 0, 0.08)"},
        {"name": "Flutter", "color": "#02569B", "bg": "rgba(2, 86, 155, 0.14)"},
        {"name": "Dart", "color": "#0175C2", "bg": "rgba(1, 117, 194, 0.14)"},
        {"name": "Python", "color": "#3776AB", "bg": "rgba(55, 118, 171, 0.14)"},
        {"name": "FastAPI", "color": "#009688", "bg": "rgba(0, 150, 136, 0.14)"},
        {"name": "Firebase", "color": "#FFA000", "bg": "rgba(255, 160, 0, 0.14)"},
        {"name": "Git", "color": "#F05032", "bg": "rgba(240, 80, 50, 0.14)"},
        {"name": "GitHub", "color": "#F5F4F1" if is_dark else "#181717", "bg": "rgba(245, 244, 241, 0.10)" if is_dark else "rgba(24, 23, 23, 0.08)"},
        {"name": "VS Code", "color": "#007ACC", "bg": "rgba(0, 122, 204, 0.14)"},
        {"name": "Docker", "color": "#2496ED", "bg": "rgba(36, 150, 237, 0.14)"},
        {"name": "HTML5", "color": "#E34F26", "bg": "rgba(227, 79, 38, 0.14)"},
        {"name": "CSS3", "color": "#1572B6", "bg": "rgba(21, 114, 182, 0.14)"}
    ]

    pills_xml = ""
    tx = 30
    ty = 65

    for item in techs:
        name = item["name"]
        color = item["color"]
        badge_bg = item["bg"]
        width = len(name) * 9.5 + 44

        if tx + width > 820:
            tx = 30
            ty += 42

        pills_xml += f'''<g transform="translate({tx}, {ty})">
          <rect x="0" y="0" width="{width}" height="32" rx="6" fill="{badge_bg}" stroke="{color}" stroke-width="1.2" opacity="0.95" />
          <circle cx="16" cy="16" r="5" fill="{color}" />
          <text x="28" y="21" font-family="ui-monospace, SFMono-Regular, Roboto, monospace" font-size="13" font-weight="700" fill="{text_primary}">{name}</text>
        </g>'''
        tx += width + 12

    svg_h = ty + 50

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 {svg_h}" width="100%" height="100%">
  <title>Developer Toolbox — Official Brand Colors</title>

  <!-- Card Background -->
  <rect x="0" y="0" width="850" height="{svg_h}" rx="8" fill="{bg}" stroke="{line_color}" stroke-width="1" />
  <rect x="0" y="0" width="3.5" height="{svg_h}" fill="{accent}" />

  <!-- Header -->
  <text x="30" y="38" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="700" fill="{accent}" letter-spacing="2">~/ TOOLBOX // CORE TECHNOLOGIES &amp; TOOLS</text>
  <line x1="30" y1="48" x2="820" y2="48" stroke="{line_color}" stroke-width="1" />

  <!-- Technologies Grid -->
  {pills_xml}
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    with open("assets/toolbox-dark.svg", "w", encoding="utf-8") as f:
        f.write(create_toolbox_svg(is_dark=True))
    with open("assets/toolbox-light.svg", "w", encoding="utf-8") as f:
        f.write(create_toolbox_svg(is_dark=False))
    print("Generated assets/toolbox-dark.svg and assets/toolbox-light.svg (colorful tech icons)")

if __name__ == "__main__":
    main()
