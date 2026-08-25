import os

def create_snake_svg(is_dark=True):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    cell_empty = "#1F1E1B" if is_dark else "#EBEDF0"
    cell_l1 = "#523F27"
    cell_l2 = "#8B6F47"
    cell_l3 = "#D4A359"
    cell_l4 = "#F5F4F1"
    snake_head = "#E5B869"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#D4A359" if is_dark else "#8B6F47"

    grid_xml = ""
    # 52 weeks x 7 days grid representation
    for w in range(52):
        for d in range(7):
            cx = 30 + w * 15
            cy = 50 + d * 15
            # Deterministic activity simulation pattern
            val = ((w * 3 + d * 7) % 11)
            if val < 5:
                color = cell_empty
            elif val < 8:
                color = cell_l1
            elif val < 10:
                color = cell_l2
            elif val < 11:
                color = cell_l3
            else:
                color = cell_l4

            grid_xml += f'<rect x="{cx}" y="{cy}" width="11" height="11" rx="2" fill="{color}" />\n'

    # Animated snake path over contribution cells
    snake_nodes = [
        (30 + 42 * 15 + 5, 50 + 2 * 15 + 5),
        (30 + 43 * 15 + 5, 50 + 2 * 15 + 5),
        (30 + 44 * 15 + 5, 50 + 2 * 15 + 5),
        (30 + 44 * 15 + 5, 50 + 3 * 15 + 5),
        (30 + 45 * 15 + 5, 50 + 3 * 15 + 5),
    ]

    snake_body_xml = ""
    for idx, (sx, sy) in enumerate(snake_nodes):
        r = 5.5 if idx == len(snake_nodes) - 1 else 4.5
        fill = snake_head if idx == len(snake_nodes) - 1 else cell_l3
        snake_body_xml += f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="{fill}" stroke="{bg}" stroke-width="1" />\n'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 175" width="100%" height="100%">
  <title>GitHub Contribution Grid Snake — Hamza Taif</title>

  <!-- Card Background -->
  <rect x="0" y="0" width="850" height="175" rx="8" fill="{bg}" stroke="{line_color}" stroke-width="1" />
  <rect x="0" y="0" width="3.5" height="175" fill="{accent}" />

  <!-- Header -->
  <text x="30" y="32" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="11" font-weight="700" fill="{accent}" letter-spacing="2">CONTRIBUTION SNAKE // AUTOMATED GITHUB ACTIVITY GRAPH</text>
  <line x1="30" y1="40" x2="820" y2="40" stroke="{line_color}" stroke-width="1" />

  <!-- Contribution Cells -->
  {grid_xml}

  <!-- Animated Contribution Snake -->
  {snake_body_xml}
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    with open("assets/github-contribution-grid-snake-dark.svg", "w", encoding="utf-8") as f:
        f.write(create_snake_svg(is_dark=True))
    with open("assets/github-contribution-grid-snake.svg", "w", encoding="utf-8") as f:
        f.write(create_snake_svg(is_dark=False))
    print("Generated initial assets/github-contribution-grid-snake-dark.svg and light SVG")

if __name__ == "__main__":
    main()
