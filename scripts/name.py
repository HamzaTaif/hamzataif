import os

def create_name_svg(is_dark=True):
    hamza_color = "#F5F4F1" if is_dark else "#171613"
    taif_color = "#D4A359" if is_dark else "#A87932"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 95" width="100%" height="100%">
  <title>HAMZA TAIF — Designed Typography Name Header</title>
  <style>
    .name-text {{
      font-family: ui-monospace, SFMono-Regular, "Roboto Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 48px;
      font-weight: 900;
      letter-spacing: 8px;
      text-anchor: middle;
    }}
    .hamza-part {{
      fill: {hamza_color};
      stroke: {hamza_color};
      stroke-width: 1.2px;
    }}
    .taif-part {{
      fill: {taif_color};
      stroke: {taif_color};
      stroke-width: 1.2px;
    }}
  </style>

  <g transform="translate(350, 64)">
    <text class="name-text">
      <tspan class="hamza-part">HAMZA </tspan><tspan class="taif-part">TAIF</tspan>
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
    with open("assets/name.svg", "w", encoding="utf-8") as f:
        f.write(create_name_svg(is_dark=True))
    print("Generated assets/name-dark.svg and assets/name-light.svg (Extra Bold 48px)")

if __name__ == "__main__":
    main()
