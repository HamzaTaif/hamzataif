import sys
import os
import math
from PIL import Image, ImageEnhance

def generate_portrait_svg(input_path="hamza.png", output_dark="assets/portrait-dark.svg", output_light="assets/portrait-light.svg"):
    if not os.path.exists(input_path):
        print(f"Notice: {input_path} not found. Preserving existing portrait SVGs.")
        return

    orig = Image.open(input_path).convert("RGBA")
    w, h = orig.size
    crop_h = int(h * 0.76)
    cropped = orig.crop((0, 0, w, crop_h))

    # Fine stipple resolution: 112 cols x 134 rows
    grid_w = 112
    grid_h = 134
    
    resized = cropped.resize((grid_w, grid_h), Image.Resampling.LANCZOS)

    gray = resized.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    gray_enhanced = enhancer.enhance(1.18)

    dot_spacing = 3.8
    offset_x = 24
    offset_y = 16

    num_bands = 56 # 56 horizontal bands for top-to-bottom scan animation
    rows_per_band = math.ceil(grid_h / num_bands)

    dark_bands = {i: [] for i in range(num_bands)}
    light_bands = {i: [] for i in range(num_bands)}

    total_dots_dark = 0
    total_dots_light = 0

    for gy in range(grid_h):
        band_idx = min(num_bands - 1, gy // rows_per_band)
        norm_y = gy / (grid_h - 1)
        
        if norm_y > 0.76:
            edge_fade = 1.0 - ((norm_y - 0.76) / 0.24)
        elif norm_y < 0.03:
            edge_fade = norm_y / 0.03
        else:
            edge_fade = 1.0

        for gx in range(grid_w):
            r, g, b, a = resized.getpixel((gx, gy))
            if a < 25:
                continue

            norm_x = gx / (grid_w - 1)
            dist_center = abs(norm_x - 0.5) * 2.0
            side_fade = 1.0 if dist_center < 0.76 else (1.0 - (dist_center - 0.76)/0.24)
            fade = edge_fade * side_fade
            if fade <= 0.03:
                continue

            raw_lum = gray_enhanced.getpixel((gx, gy)) / 255.0
            lum = math.pow(raw_lum, 0.84)

            cx = round(offset_x + gx * dot_spacing, 1)
            cy = round(offset_y + gy * dot_spacing, 1)

            # --- DARK MODE VIVID PALETTE ---
            r_dark = round((0.45 + lum * 1.15) * fade, 1)
            if lum > 0.72:
                col_dark = "#F5F4F1" # Warm Ivory highlight
                op_dark = round(min(1.0, (0.7 + lum * 0.3) * fade), 2)
            elif lum > 0.50:
                col_dark = "#E5B869" # Warm Gold
                op_dark = round(min(1.0, (0.65 + lum * 0.35) * fade), 2)
            elif lum > 0.32:
                col_dark = "#D4A359" # Amber
                op_dark = round(min(1.0, (0.6 + lum * 0.4) * fade), 2)
            elif lum > 0.16:
                col_dark = "#C86D3B" # Burnt Orange
                op_dark = round(min(1.0, (0.55 + lum * 0.4) * fade), 2)
            elif lum > 0.06:
                col_dark = "#8B6F47" # Warm Bronze
                op_dark = round(min(1.0, (0.45 + lum * 0.45) * fade), 2)
            else:
                col_dark = "#3A3127" # Deep Brown
                op_dark = round(min(1.0, 0.4 * fade), 2)

            if r_dark >= 0.4 and op_dark >= 0.05:
                dark_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dark}" fill="{col_dark}" opacity="{op_dark}"/>')
                total_dots_dark += 1

            # --- LIGHT MODE PALETTE ---
            inv_lum = 1.0 - lum
            r_light = round((0.45 + inv_lum * 1.15) * fade, 1)
            if inv_lum > 0.65:
                col_light = "#1A1917"
                op_light = round(min(1.0, (0.7 + inv_lum * 0.3) * fade), 2)
            elif inv_lum > 0.45:
                col_light = "#8B6F47"
                op_light = round(min(1.0, (0.65 + inv_lum * 0.35) * fade), 2)
            elif inv_lum > 0.25:
                col_light = "#C86D3B"
                op_light = round(min(1.0, (0.6 + inv_lum * 0.4) * fade), 2)
            elif inv_lum > 0.10:
                col_light = "#D4A359"
                op_light = round(min(1.0, (0.5 + inv_lum * 0.45) * fade), 2)
            else:
                col_light = "#E5E2D9"
                op_light = round(min(1.0, 0.4 * fade), 2)

            if r_light >= 0.4 and op_light >= 0.05:
                light_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_light}" fill="{col_light}" opacity="{op_light}"/>')
                total_dots_light += 1

    svg_w = int(offset_x * 2 + grid_w * dot_spacing)
    svg_h = int(offset_y * 2 + grid_h * dot_spacing)

    # CSS Keyframe Delays for Sequential Top-to-Bottom Row Construction
    css_rules = []
    total_anim_duration = 2.2 # 2.2 seconds total sweep
    delay_step = round(total_anim_duration / num_bands, 3)

    for i in range(num_bands):
        d_sec = round(i * delay_step, 3)
        css_rules.append(f'.b-{i} {{ animation-delay: {d_sec}s; }}')

    css_block = '\n    '.join(css_rules)

    dark_bands_xml = []
    for i in range(num_bands):
        if dark_bands[i]:
            dark_bands_xml.append(f'<g class="band b-{i}">\n      ' + '\n      '.join(dark_bands[i]) + '\n    </g>')

    light_bands_xml = []
    for i in range(num_bands):
        if light_bands[i]:
            light_bands_xml.append(f'<g class="band b-{i}">\n      ' + '\n      '.join(light_bands[i]) + '\n    </g>')

    dark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="100%" height="100%">
  <title>Hamza Taif — Sequential Top-to-Bottom Stipple Portrait (Dark)</title>
  <style>
    .band {{
      opacity: 0;
      animation: rowReveal 0.32s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }}
    @keyframes rowReveal {{
      0% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    {css_block}
    @media (prefers-reduced-motion: reduce) {{
      .band {{ animation: none; opacity: 1; }}
    }}
  </style>
  <g class="portrait-container">
    {'\n    '.join(dark_bands_xml)}
  </g>
</svg>'''

    light_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="100%" height="100%">
  <title>Hamza Taif — Sequential Top-to-Bottom Stipple Portrait (Light)</title>
  <style>
    .band {{
      opacity: 0;
      animation: rowReveal 0.32s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }}
    @keyframes rowReveal {{
      0% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    {css_block}
    @media (prefers-reduced-motion: reduce) {{
      .band {{ animation: none; opacity: 1; }}
    }}
  </style>
  <g class="portrait-container">
    {'\n    '.join(light_bands_xml)}
  </g>
</svg>'''

    os.makedirs("assets", exist_ok=True)
    with open(output_dark, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(output_light, "w", encoding="utf-8") as f:
        f.write(light_svg)

    dark_size_kb = os.path.getsize(output_dark) / 1024.0
    light_size_kb = os.path.getsize(output_light) / 1024.0

    print(f"Generated {output_dark}: {dark_size_kb:.1f} KB ({total_dots_dark} dots across {num_bands} bands)")
    print(f"Generated {output_light}: {light_size_kb:.1f} KB ({total_dots_light} dots across {num_bands} bands)")
    print(f"Dimensions: {svg_w}x{svg_h} viewBox (Large scale)")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "hamza.png"
    generate_portrait_svg(input_file)
