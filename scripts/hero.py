import os
import re
from PIL import Image, ImageEnhance

def extract_existing_portrait(svg_path):
    if os.path.exists(svg_path):
        with open(svg_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'<g class="hero-portrait">(.*?)</g>\s*</g>', content, re.DOTALL)
        if match:
            return match.group(1)
    return ""

def generate_portrait_elements(input_path="hamza.png", is_dark=True):
    if not os.path.exists(input_path):
        target_svg = "assets/hero-dark.svg" if is_dark else "assets/hero-light.svg"
        existing = extract_existing_portrait(target_svg)
        return existing, 320, 380

    orig = Image.open(input_path).convert("RGBA")
    w, h = orig.size
    crop_h = int(h * 0.74)
    cropped = orig.crop((0, 0, w, crop_h))

    grid_w = 78
    grid_h = 94
    resized = cropped.resize((grid_w, grid_h), Image.Resampling.LANCZOS)

    gray = resized.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    gray_enhanced = enhancer.enhance(1.4)

    dot_spacing = 3.6
    offset_x = 0
    offset_y = 0

    groups = {}
    total_dots = 0

    for gy in range(grid_h):
        norm_y = gy / (grid_h - 1)
        if norm_y > 0.74:
            edge_fade = 1.0 - ((norm_y - 0.74) / 0.26)
        elif norm_y < 0.04:
            edge_fade = norm_y / 0.04
        else:
            edge_fade = 1.0

        for gx in range(grid_w):
            r, g, b, a = resized.getpixel((gx, gy))
            if a < 25:
                continue

            norm_x = gx / (grid_w - 1)
            dist_center = abs(norm_x - 0.5) * 2.0
            side_fade = 1.0 if dist_center < 0.72 else (1.0 - (dist_center - 0.72)/0.28)
            fade = edge_fade * side_fade
            if fade <= 0.05:
                continue

            lum = gray_enhanced.getpixel((gx, gy)) / 255.0
            cx = round(offset_x + gx * dot_spacing, 1)
            cy = round(offset_y + gy * dot_spacing, 1)

            if is_dark:
                if lum > 0.1:
                    r_dot = round((0.5 + lum * 1.15) * fade, 1)
                    if lum > 0.62:
                        col = "#F5F4F1"
                        op = round(min(1.0, (0.6 + lum * 0.4) * fade), 1)
                    elif lum > 0.32:
                        col = "#8B6F47"
                        op = round(min(1.0, (0.65 + lum * 0.35) * fade), 1)
                    else:
                        col = "#B5B0A6"
                        op = round(min(1.0, (0.45 + lum * 0.5) * fade), 1)

                    if r_dot >= 0.45 and op >= 0.08:
                        key = (col, op)
                        if key not in groups:
                            groups[key] = []
                        groups[key].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot}"/>')
                        total_dots += 1
            else:
                inv_lum = 1.0 - lum
                if inv_lum > 0.1:
                    r_dot = round((0.5 + inv_lum * 1.15) * fade, 1)
                    if inv_lum > 0.55:
                        col = "#1A1917"
                        op = round(min(1.0, (0.6 + inv_lum * 0.4) * fade), 1)
                    elif inv_lum > 0.28:
                        col = "#8B6F47"
                        op = round(min(1.0, (0.65 + inv_lum * 0.35) * fade), 1)
                    else:
                        col = "#55524C"
                        op = round(min(1.0, (0.45 + inv_lum * 0.5) * fade), 1)

                    if r_dot >= 0.45 and op >= 0.08:
                        key = (col, op)
                        if key not in groups:
                            groups[key] = []
                        groups[key].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot}"/>')
                        total_dots += 1

    elements = []
    for (col, op), circles in groups.items():
        op_attr = f' opacity="{op}"' if op < 1.0 else ''
        elements.append(f'<g fill="{col}"{op_attr}>' + ''.join(circles) + '</g>')

    pw = int(grid_w * dot_spacing)
    ph = int(grid_h * dot_spacing)
    return ''.join(elements), pw, ph

def create_hero_svg(is_dark=True):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    text_primary = "#F5F4F1" if is_dark else "#1A1917"
    # Dark Mode TAIF text color set to #8B6F47 (Warm Bronze) for 100% readability & visual impact!
    text_taif = "#8B6F47" if is_dark else "#8B6F47"
    text_muted = "#A6A29A" if is_dark else "#6E6A63"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#8B6F47"

    portrait_xml, pw, ph = generate_portrait_elements("hamza.png", is_dark=is_dark)

    portrait_group = f'''<g transform="translate(570, 10)">
    <style>
      .hero-portrait {{
        animation: heroPortraitReveal 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }}
      @keyframes heroPortraitReveal {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .hero-portrait {{ animation: none; opacity: 1; }}
      }}
    </style>
    <g class="hero-portrait">
      {portrait_xml}
    </g>
  </g>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 340" width="100%" height="100%">
  <title>Hamza Taif — Software Engineering, AI, Full-Stack App Development</title>

  <!-- Background -->
  <rect x="0" y="0" width="880" height="340" fill="{bg}" />

  <!-- Left Accent Line -->
  <rect x="0" y="0" width="3.5" height="340" fill="{accent}" />

  <!-- Top Structural Line -->
  <line x1="42" y1="38" x2="530" y2="38" stroke="{line_color}" stroke-width="1" />

  <!-- Stacked Dominant Typography -->
  <text x="38" y="142" font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="88" font-weight="900" fill="{text_primary}" letter-spacing="-1">HAMZA</text>
  <text x="38" y="228" font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="88" font-weight="900" fill="{text_taif}" letter-spacing="-1">TAIF</text>

  <!-- Discipline Line -->
  <text x="40" y="274" font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" fill="{text_muted}" letter-spacing="1">SOFTWARE ENGINEERING  ·  AI  ·  FULL-STACK APP DEVELOPMENT</text>

  <!-- Tagline -->
  <text x="40" y="302" font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="400" fill="{text_primary}" opacity="0.8" letter-spacing="0.3">Building useful software, one system at a time.</text>

  <!-- Right Side Stipple Portrait -->
  {portrait_group}

  <!-- Bottom Structural Line -->
  <line x1="42" y1="318" x2="530" y2="318" stroke="{line_color}" stroke-width="1" />
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    with open("assets/hero-dark.svg", "w", encoding="utf-8") as f:
        f.write(create_hero_svg(is_dark=True))
    with open("assets/hero-light.svg", "w", encoding="utf-8") as f:
        f.write(create_hero_svg(is_dark=False))
    print("Generated assets/hero-dark.svg and assets/hero-light.svg with high-contrast typography and refined portrait.")

if __name__ == "__main__":
    main()
