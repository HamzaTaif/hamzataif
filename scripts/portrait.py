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
    return f"#{max(0, min(255, rgb[0])):02x}{max(0, min(255, rgb[1])):02x}{max(0, min(255, rgb[2])):02x}"

def generate_portrait_svg(input_path="hamza.png", output_dark="assets/portrait-dark.svg", output_light="assets/portrait-light.svg"):
    if not os.path.exists(input_path):
        print(f"Notice: {input_path} not found. Preserving existing portrait SVGs.")
        return

    orig = Image.open(input_path).convert("RGBA")
    w, h = orig.size
    crop_h = int(h * 0.78)
    cropped = orig.crop((0, 0, w, crop_h))

    # High-resolution sampling grid matching reference girl portrait: 210 cols x 250 rows (~38,000 dots)
    grid_w = 210
    grid_h = 250

    resized = cropped.resize((grid_w, grid_h), Image.Resampling.LANCZOS)

    # Mild detail sharpening to preserve crisp facial features (eyes, nose, beard contours)
    enhancer = ImageEnhance.Sharpness(resized)
    enhanced = enhancer.enhance(1.4)

    dot_spacing = 2.6
    offset_x = 12
    offset_y = 12

    num_bands = 70 # 70 horizontal bands for 4.0s smooth top-to-bottom scan reveal
    rows_per_band = math.ceil(grid_h / num_bands)

    dark_bands = {i: [] for i in range(num_bands)}
    light_bands = {i: [] for i in range(num_bands)}

    total_dots_dark = 0
    total_dots_light = 0

    # Continuous warm palette spectrum derived from reference he.png
    warm_spectrum = [
        (0.00, hex_to_rgb("#120A07")), # Deep brown shadow
        (0.25, hex_to_rgb("#4A1C10")), # Deep copper brown
        (0.45, hex_to_rgb("#7D3015")), # Burnt copper
        (0.65, hex_to_rgb("#B84D18")), # Warm amber orange
        (0.80, hex_to_rgb("#E08B2A")), # Warm gold
        (0.92, hex_to_rgb("#ECAE4E")), # Soft gold cream
        (1.00, hex_to_rgb("#F5E2B5"))  # Warm highlight cream
    ]

    def get_warm_tone(val):
        val = max(0.0, min(1.0, val))
        for i in range(len(warm_spectrum) - 1):
            v1, c1 = warm_spectrum[i]
            v2, c2 = warm_spectrum[i+1]
            if v1 <= val <= v2:
                f = (val - v1) / (v2 - v1)
                return blend_colors(c1, c2, f)
        return warm_spectrum[-1][1]

    for gy in range(grid_h):
        band_idx = min(num_bands - 1, gy // rows_per_band)
        norm_y = gy / (grid_h - 1)

        # Smooth boundary fade at very bottom
        if norm_y > 0.88:
            edge_fade = 1.0 - ((norm_y - 0.88) / 0.12)
        else:
            edge_fade = 1.0

        for gx in range(grid_w):
            r, g, b, a = enhanced.getpixel((gx, gy))
            if a < 25:
                continue

            norm_x = gx / (grid_w - 1)
            dist_center = abs(norm_x - 0.5) * 2.0
            side_fade = 1.0 if dist_center < 0.85 else (1.0 - (dist_center - 0.85)/0.15)
            fade = edge_fade * side_fade
            if fade <= 0.02:
                continue

            # Continuous perceptual luminance
            raw_lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            
            # Smooth midtone lift curve (gamma 0.65)
            lum = (raw_lum ** 0.65) * fade

            cx = round(offset_x + gx * dot_spacing, 2)
            cy = round(offset_y + gy * dot_spacing, 2)

            # Continuous dot radius (0.45px to 1.80px max) - matching reference he.png dot size
            r_dot = round(max(0.45, 0.45 + (lum ** 1.1) * 1.35), 2)
            opacity = round(min(1.0, max(0.40, 0.40 + (lum ** 0.8) * 0.58)), 2)

            # Continuous color blending: blend original photo RGB with warm tone map
            # Face region receives warm amber glow; clothing/hair preserve realistic photo contrast
            is_white_clothing = (r > 185 and g > 185 and b > 185 and norm_y > 0.45)
            is_face_skin = (norm_y < 0.50 and not is_white_clothing and raw_lum > 0.20)
            
            if is_white_clothing:
                w_factor = 0.15 # 15% warm tone, 85% photo white
            elif is_face_skin:
                w_factor = 0.42 # 42% warm gold tone, 58% photo skin
            else:
                w_factor = 0.30 # 30% warm tone, 70% photo color

            warm_rgb = get_warm_tone(lum)
            photo_rgb = (r, g, b)

            # Blend dark mode color
            dark_rgb = blend_colors(photo_rgb, warm_rgb, w_factor)
            color_dark = rgb_to_hex(dark_rgb)

            # Blend light mode color
            light_base = blend_colors((15, 12, 10), photo_rgb, 0.70)
            light_rgb = blend_colors(light_base, warm_rgb, w_factor * 0.6)
            color_light = rgb_to_hex(light_rgb)

            dark_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot}" fill="{color_dark}" opacity="{opacity}"/>')
            total_dots_dark += 1

            light_bands[band_idx].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dot}" fill="{color_light}" opacity="{opacity}"/>')
            total_dots_light += 1

    svg_w = int(offset_x * 2 + grid_w * dot_spacing)
    svg_h = int(offset_y * 2 + grid_h * dot_spacing)

    # CSS Keyframe Delays for 4.0s Smooth Top-to-Bottom Scan Sweep
    css_rules = []
    total_anim_duration = 4.0 # 4.0 seconds
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
  <title>Hamza Taif — High Resolution Halftone Portrait (Dark)</title>
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
  <title>Hamza Taif — High Resolution Halftone Portrait (Light)</title>
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

    print(f"Generated {output_dark}: {dark_size_kb:.1f} KB ({total_dots_dark} halftone dots across {num_bands} bands)")
    print(f"Generated {output_light}: {light_size_kb:.1f} KB ({total_dots_light} halftone dots across {num_bands} bands)")
    print(f"Dimensions: {svg_w}x{svg_h} viewBox")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "hamza.png"
    generate_portrait_svg(input_file)
