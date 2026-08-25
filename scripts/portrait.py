import sys
import os
import math
from PIL import Image, ImageEnhance, ImageFilter

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def blend_colors(c1, c2, factor):
    factor = max(0.0, min(1.0, factor))
    return (
        int(c1[0] + (c2[0] - c1[0]) * factor),
        int(c1[1] + (c2[1] - c1[1]) * factor),
        int(c1[2] + (c2[2] - c1[2]) * factor)
    )

def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def generate_portrait_svg(input_path="hamza.png", output_dark="assets/portrait-dark.svg", output_light="assets/portrait-light.svg"):
    if not os.path.exists(input_path):
        print(f"Notice: {input_path} not found. Preserving existing portrait SVGs.")
        return

    orig = Image.open(input_path).convert("RGBA")
    w, h = orig.size
    crop_h = int(h * 0.78)
    cropped = orig.crop((0, 0, w, crop_h))

    # Grid matching reference he.png: 78 cols x 92 rows (clearly exposed dot structure)
    grid_w = 78
    grid_h = 92
    
    resized = cropped.resize((grid_w, grid_h), Image.Resampling.LANCZOS)
    
    # Contrast lift for sharp feature definition
    enhancer = ImageEnhance.Contrast(resized)
    enhanced = enhancer.enhance(1.30)

    dot_spacing = 5.8
    offset_x = 10
    offset_y = 10

    num_bands = 54 # 54 horizontal bands for 3.5s smooth top-to-bottom scan
    rows_per_band = math.ceil(grid_h / num_bands)

    dark_bands = {i: [] for i in range(num_bands)}
    light_bands = {i: [] for i in range(num_bands)}

    total_dots_dark = 0
    total_dots_light = 0

    # Rich Warm Palette derived from reference he.png:
    # Deep Brown -> Burnt Maroon -> Copper -> Burnt Orange -> Warm Amber -> Gold -> Warm Gold Cream -> Bright Highlight
    warm_palette = [
        (0.00, hex_to_rgb("#1A0D08")), # Shadow baseline
        (0.18, hex_to_rgb("#441D12")), # Deep brown maroon
        (0.32, hex_to_rgb("#6E2B15")), # Burnt maroon
        (0.48, hex_to_rgb("#993C17")), # Rich copper
        (0.62, hex_to_rgb("#C6561A")), # Burnt orange
        (0.75, hex_to_rgb("#E5741E")), # Warm amber
        (0.86, hex_to_rgb("#EF9D35")), # Gold
        (0.94, hex_to_rgb("#F4C065")), # Warm gold cream
        (1.00, hex_to_rgb("#F7E5B5"))  # Bright highlight
    ]

    def get_warm_color(val):
        val = max(0.0, min(1.0, val))
        for i in range(len(warm_palette) - 1):
            v1, c1 = warm_palette[i]
            v2, c2 = warm_palette[i+1]
            if v1 <= val <= v2:
                f = (val - v1) / (v2 - v1)
                return blend_colors(c1, c2, f)
        return warm_palette[-1][1]

    for gy in range(grid_h):
        band_idx = min(num_bands - 1, gy // rows_per_band)
        norm_y = gy / (grid_h - 1)
        norm_x = gx_norm = gx = 0 # placeholder

        # Edge fade at very bottom
        if norm_y > 0.86:
            edge_fade = 1.0 - ((norm_y - 0.86) / 0.14)
        else:
            edge_fade = 1.0

        for gx in range(grid_w):
            r, g, b, a = enhanced.getpixel((gx, gy))
            if a < 35:
                continue

            norm_x = gx / (grid_w - 1)
            dist_center = abs(norm_x - 0.5) * 2.0
            side_fade = 1.0 if dist_center < 0.85 else (1.0 - (dist_center - 0.85)/0.15)
            fade = edge_fade * side_fade
            if fade <= 0.03:
                continue

            # Perceptual luminance
            raw_lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0

            # Lift midtones with gamma 0.52
            lum = (raw_lum ** 0.52) * fade

            cx = round(offset_x + gx * dot_spacing, 1)
            cy = round(offset_y + gy * dot_spacing, 1)

            # Region detection: White shirt vs Dark waistcoat vs Face & Hair
            is_white_shirt = (r > 180 and g > 180 and b > 180 and norm_y > 0.40 and (norm_x < 0.28 or norm_x > 0.72 or norm_y > 0.80))
            is_dark_waistcoat = (norm_y > 0.40 and not is_white_shirt and raw_lum < 0.35)
            is_face_region = (norm_y < 0.52 and not is_white_shirt)

            # --- DARK MODE COLOR & DOT SIZING ---
            if is_white_shirt:
                # White sleeves: soft warm cream with restrained dot radius so face remains primary focal point
                color_dark = "#DCD5C9"
                r_dot = round(max(1.4, 1.4 + raw_lum * 1.4), 2)
                opacity = 0.78
            elif is_dark_waistcoat:
                # Dark waistcoat: subtle warm dark copper dots so vest texture & buttons pop without overpowering face
                wc_lum = max(0.08, raw_lum * 1.8)
                wc_rgb = blend_colors((20, 16, 14), (85, 68, 55), wc_lum)
                color_dark = rgb_to_hex(wc_rgb)
                r_dot = round(max(1.1, 1.1 + raw_lum * 2.8), 2)
                opacity = round(min(1.0, max(0.5, 0.5 + raw_lum * 0.5)), 2)
            elif is_face_region:
                # Face & Hair: Glowing warm gold/amber gradient matching reference he.png
                skin_lum = min(1.0, lum * 1.18)
                color_dark = rgb_to_hex(get_warm_color(skin_lum))
                # Large, bold circular dots (up to 3.85px radius) matching he.png
                r_dot = round(max(1.0, 1.0 + skin_lum * 2.85), 2)
                opacity = round(min(1.0, max(0.55, 0.55 + skin_lum * 0.45)), 2)
            else:
                color_dark = rgb_to_hex(get_warm_color(lum))
                r_dot = round(max(1.0, 1.0 + lum * 2.6), 2)
                opacity = round(min(1.0, max(0.5, 0.5 + lum * 0.5)), 2)

            dark_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot}" fill="{color_dark}" opacity="{opacity}"/>')
            total_dots_dark += 1

            # --- LIGHT MODE COLOR & DOT SIZING ---
            if is_white_shirt:
                color_light = "#2D2620"
                r_dot_light = round(max(1.3, 1.3 + raw_lum * 1.4), 2)
            elif is_dark_waistcoat:
                color_light = "#181412"
                r_dot_light = r_dot
            elif is_face_region:
                light_rgb = blend_colors((25, 18, 12), (180, 110, 35), lum)
                color_light = rgb_to_hex(light_rgb)
                r_dot_light = r_dot
            else:
                light_rgb = blend_colors((20, 15, 10), (160, 90, 30), lum)
                color_light = rgb_to_hex(light_rgb)
                r_dot_light = r_dot

            light_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot_light}" fill="{color_light}" opacity="{opacity}"/>')
            total_dots_light += 1

    svg_w = int(offset_x * 2 + grid_w * dot_spacing)
    svg_h = int(offset_y * 2 + grid_h * dot_spacing)

    # CSS Keyframe Delays for 3.5s Smooth Top-to-Bottom Construction Sweep
    css_rules = []
    total_anim_duration = 3.5 # 3.5 seconds
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
  <title>Hamza Taif — Warm Stipple Pixel Portrait (Dark)</title>
  <style>
    .band {{
      opacity: 0;
      animation: rowReveal 0.35s cubic-bezier(0.25, 1, 0.5, 1) forwards;
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
  <title>Hamza Taif — Warm Stipple Pixel Portrait (Light)</title>
  <style>
    .band {{
      opacity: 0;
      animation: rowReveal 0.35s cubic-bezier(0.25, 1, 0.5, 1) forwards;
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

    print(f"Generated {output_dark}: {dark_size_kb:.1f} KB ({total_dots_dark} warm pixel dots across {num_bands} bands)")
    print(f"Generated {output_light}: {light_size_kb:.1f} KB ({total_dots_light} warm pixel dots across {num_bands} bands)")
    print(f"Dimensions: {svg_w}x{svg_h} viewBox")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "hamza.png"
    generate_portrait_svg(input_file)
