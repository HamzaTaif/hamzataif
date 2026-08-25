import os

def create_name_svg(is_dark=True):
    hamza_color = "#F5F4F1" if is_dark else "#1A1917"
    taif_color = "#D4A359" if is_dark else "#8B6F47"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 50" width="100%" height="100%">
  <title>Hamza Taif — Designed Static Typography Name</title>
  <style>
    .name-title {{
      font-family: ui-monospace, SFMono-Regular, "Roboto Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 32px;
      font-weight: 900;
      letter-spacing: 5px;
      text-anchor: middle;
    }}
  </style>

  <g transform="translate(300, 36)">
    <text class="name-title">
      <tspan fill="{hamza_color}">HAMZA </tspan><tspan fill="{taif_color}">TAIF</tspan>
    </text>
  </g>
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    with open("assets/name-dark.svg", "w", encoding="utf-8") as f:
        f.write(create_name_svg(is_dark=True))
    with open("assets/name-light.svg", "w", encoding="utf-8") as f:
        f.write(create_name_svg(is_dark=False))
    print("Generated assets/name-dark.svg and assets/name-light.svg (Designed static name)")

if __name__ == "__main__":
    main()
