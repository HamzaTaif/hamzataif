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
    crop_h = int(h * 0.78)
    cropped = orig.crop((0, 0, w, crop_h))

    # High-density realistic sampling: 136 cols x 162 rows
    grid_w = 136
    grid_h = 162
    
    resized = cropped.resize((grid_w, grid_h), Image.Resampling.LANCZOS)

    # Slight contrast enhancement to keep photo features crisp
    gray = resized.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    gray_enhanced = enhancer.enhance(1.12)

    dot_spacing = 3.6
    offset_x = 16
    offset_y = 16

    num_bands = 60 # 60 horizontal bands for 3.5s top-to-bottom construction
    rows_per_band = math.ceil(grid_h / num_bands)

    dark_bands = {i: [] for i in range(num_bands)}
    light_bands = {i: [] for i in range(num_bands)}

    total_dots_dark = 0
    total_dots_light = 0

    for gy in range(grid_h):
        band_idx = min(num_bands - 1, gy // rows_per_band)
        norm_y = gy / (grid_h - 1)
        
        # Soft vertical edge feathering at bottom chest
        if norm_y > 0.78:
            edge_fade = 1.0 - ((norm_y - 0.78) / 0.22)
        elif norm_y < 0.02:
            edge_fade = norm_y / 0.02
        else:
            edge_fade = 1.0

        for gx in range(grid_w):
            r, g, b, a = resized.getpixel((gx, gy))
            if a < 30:
                continue

            norm_x = gx / (grid_w - 1)
            dist_center = abs(norm_x - 0.5) * 2.0
            side_fade = 1.0 if dist_center < 0.78 else (1.0 - (dist_center - 0.78)/0.22)
            fade = edge_fade * side_fade
            if fade <= 0.03:
                continue

            raw_lum = gray_enhanced.getpixel((gx, gy)) / 255.0
            lum = math.pow(raw_lum, 0.85)

            cx = round(offset_x + gx * dot_spacing, 1)
            cy = round(offset_y + gy * dot_spacing, 1)

            # Dot radius based on luminance & detail density
            r_dot = round(max(0.4, (0.5 + lum * 1.1) * fade), 1)
            opacity = round(min(1.0, max(0.2, (0.45 + lum * 0.55) * fade)), 2)

            # --- REAL PHOTO COLORS FOR DARK MODE ---
            # Boost color vibrancy slightly while maintaining 100% natural photo appearance
            r_real = min(255, int(r * 1.05 + 10))
            g_real = min(255, int(g * 1.02 + 5))
            b_real = min(255, int(b * 1.02))

            # If pixel is hair or dark shadow, ensure dark charcoal/black
            if lum < 0.12:
                r_real = max(15, int(r * 0.9))
                g_real = max(15, int(g * 0.9))
                b_real = max(15, int(b * 0.9))

            # Eye whites preservation: if region is bright white sclera, preserve clean white
            if lum > 0.82 and r > 180 and g > 180 and b > 180:
                r_real = 248
                g_real = 248
                b_real = 245
                r_dot = 1.5

            color_dark = f"rgb({r_real},{g_real},{b_real})"
            dark_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot}" fill="{color_dark}" opacity="{opacity}"/>')
            total_dots_dark += 1

            # --- REAL PHOTO COLORS FOR LIGHT MODE ---
            color_light = f"rgb({r},{g},{b})"
            light_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot}" fill="{color_light}" opacity="{opacity}"/>')
            total_dots_light += 1

    svg_w = int(offset_x * 2 + grid_w * dot_spacing)
    svg_h = int(offset_y * 2 + grid_h * dot_spacing)

    # CSS Keyframe Delays for 3.5s Top-to-Bottom Sequential Construction
    css_rules = []
    total_anim_duration = 3.5 # 3.5 seconds total sweep
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
  <title>Hamza Taif — Realistic Photo Stipple Portrait (Dark)</title>
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
  <title>Hamza Taif — Realistic Photo Stipple Portrait (Light)</title>
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

    print(f"Generated {output_dark}: {dark_size_kb:.1f} KB ({total_dots_dark} realistic dots across {num_bands} bands)")
    print(f"Generated {output_light}: {light_size_kb:.1f} KB ({total_dots_light} realistic dots across {num_bands} bands)")
    print(f"Dimensions: {svg_w}x{svg_h} viewBox (Large visual scale)")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "hamza.png"
    generate_portrait_svg(input_file)
