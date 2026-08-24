import os

def create_toolbox_svg(is_dark=True):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    text_primary = "#F5F4F1" if is_dark else "#1A1917"
    text_muted = "#A6A29A" if is_dark else "#6E6A63"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#8B6F47"

    techs = [
        "Flutter", "Dart", "Python", "FastAPI", "Firebase", 
        "React", "Next.js", "JavaScript", "C++", "Git", "Docker"
    ]

    pills_xml = ""
    tx = 24
    ty = 25

    for i, t in enumerate(techs):
        width = len(t) * 9 + 20
        if tx + width > 820:
            tx = 24
            ty += 34

        pills_xml += f'''<g transform="translate({tx}, {ty})">
          <rect x="0" y="0" width="{width}" height="26" rx="5" fill="rgba(139, 111, 71, 0.08)" stroke="{line_color}" stroke-width="1" />
          <text x="{width/2}" y="17" font-family="ui-monospace, SFMono-Regular, monospace" font-size="12" font-weight="600" fill="{text_primary}" text-anchor="middle">{t}</text>
        </g>'''
        tx += width + 10

    svg_h = ty + 38

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 {svg_h}" width="100%" height="100%">
  <title>Engineering Toolbox</title>

  <!-- Card Background -->
  <rect x="0" y="0" width="850" height="{svg_h}" rx="8" fill="{bg}" stroke="{line_color}" stroke-width="1" />
  <rect x="0" y="0" width="3.5" height="{svg_h}" fill="{accent}" />

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
    print("Generated assets/toolbox-dark.svg and assets/toolbox-light.svg")

if __name__ == "__main__":
    main()
