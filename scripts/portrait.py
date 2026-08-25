import sys
import os
import math
from PIL import Image, ImageEnhance, ImageFilter

def generate_portrait_svg(input_path="hamza.png", output_dark="assets/portrait-dark.svg", output_light="assets/portrait-light.svg"):
    if not os.path.exists(input_path):
        print(f"Notice: {input_path} not found. Preserving existing portrait SVGs.")
        return

    orig = Image.open(input_path).convert("RGBA")
    w, h = orig.size
    crop_h = int(h * 0.78)
    cropped = orig.crop((0, 0, w, crop_h))

    # Substantially increased sampling density: 160 cols x 190 rows for smooth photorealism
    grid_w = 160
    grid_h = 190
    
    resized = cropped.resize((grid_w, grid_h), Image.Resampling.LANCZOS)

    # Slight smooth filter to eliminate harsh high-frequency noise & sparkling
    smoothed = resized.filter(ImageFilter.SMOOTH_MORE)

    dot_spacing = 2.6
    offset_x = 14
    offset_y = 14

    num_bands = 65 # 65 horizontal bands for 3.5s smooth top-to-bottom scan
    rows_per_band = math.ceil(grid_h / num_bands)

    dark_bands = {i: [] for i in range(num_bands)}
    light_bands = {i: [] for i in range(num_bands)}

    total_dots_dark = 0
    total_dots_light = 0

    for gy in range(grid_h):
        band_idx = min(num_bands - 1, gy // rows_per_band)
        norm_y = gy / (grid_h - 1)
        
        # Soft feathering at bottom chest
        if norm_y > 0.80:
            edge_fade = 1.0 - ((norm_y - 0.80) / 0.20)
        elif norm_y < 0.02:
            edge_fade = norm_y / 0.02
        else:
            edge_fade = 1.0

        for gx in range(grid_w):
            r, g, b, a = smoothed.getpixel((gx, gy))
            if a < 35:
                continue

            norm_x = gx / (grid_w - 1)
            dist_center = abs(norm_x - 0.5) * 2.0
            side_fade = 1.0 if dist_center < 0.80 else (1.0 - (dist_center - 0.80)/0.20)
            fade = edge_fade * side_fade
            if fade <= 0.03:
                continue

            # Perceptual luminance calculation
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0

            cx = round(offset_x + gx * dot_spacing, 1)
            cy = round(offset_y + gy * dot_spacing, 1)

            # Micro-dot sizing (0.4px to 0.85px) for a smooth photo look
            r_dot = round(max(0.4, (0.45 + lum * 0.4) * fade), 2)
            opacity = round(min(1.0, max(0.3, (0.55 + lum * 0.45) * fade)), 2)

            # --- REAL PHOTO COLORS FOR DARK MODE ---
            # Natural photo RGB fill with zero artificial contrast harshness
            r_dark = max(10, min(255, int(r)))
            g_dark = max(10, min(255, int(g)))
            b_dark = max(10, min(255, int(b)))

            color_dark = f"rgb({r_dark},{g_dark},{b_dark})"
            dark_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot}" fill="{color_dark}" opacity="{opacity}"/>')
            total_dots_dark += 1

            # --- REAL PHOTO COLORS FOR LIGHT MODE ---
            color_light = f"rgb({r},{g},{b})"
            light_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot}" fill="{color_light}" opacity="{opacity}"/>')
            total_dots_light += 1

    svg_w = int(offset_x * 2 + grid_w * dot_spacing)
    svg_h = int(offset_y * 2 + grid_h * dot_spacing)

    # CSS Keyframe Delays for 3.5s Smooth Top-to-Bottom Construction
    css_rules = []
    total_anim_duration = 3.5 # 3.5 seconds total construction sweep
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
  <title>Hamza Taif — Smooth Photo Stipple Portrait (Dark)</title>
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
  <title>Hamza Taif — Smooth Photo Stipple Portrait (Light)</title>
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

    print(f"Generated {output_dark}: {dark_size_kb:.1f} KB ({total_dots_dark} smooth dots across {num_bands} bands)")
    print(f"Generated {output_light}: {light_size_kb:.1f} KB ({total_dots_light} smooth dots across {num_bands} bands)")
    print(f"Dimensions: {svg_w}x{svg_h} viewBox")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "hamza.png"
    generate_portrait_svg(input_file)
