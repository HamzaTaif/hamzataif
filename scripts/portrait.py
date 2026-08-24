import sys
import os
import math
from PIL import Image, ImageEnhance

def generate_portrait_svg(input_path="hamza.png", output_dark="assets/portrait-dark.svg", output_light="assets/portrait-light.svg"):
    if not os.path.exists(input_path):
        print(f"Notice: {input_path} not found. Preserving existing portrait SVGs.")
        return

    orig = Image.open(input_path).convert("RGBA")
    
    # Crop to head + shoulders + upper chest
    w, h = orig.size
    crop_h = int(h * 0.74)
    cropped = orig.crop((0, 0, w, crop_h))

    # Grid dimensions: 84 cols x 100 rows for high-definition facial contrast at GitHub width
    grid_w = 84
    grid_h = 100
    
    resized = cropped.resize((grid_w, grid_h), Image.Resampling.LANCZOS)

    # Enhance contrast to ensure eyes, nose, beard, hair contours pop crisply
    gray = resized.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    gray_enhanced = enhancer.enhance(1.4)

    dot_spacing = 3.6
    offset_x = 10
    offset_y = 10

    dark_groups = {}
    light_groups = {}

    total_dots_dark = 0
    total_dots_light = 0

    for gy in range(grid_h):
        norm_y = gy / (grid_h - 1)
        
        # Edge fade: dissolve towards bottom shoulders (bottom 25%) and top hairline
        if norm_y > 0.74:
            edge_fade = 1.0 - ((norm_y - 0.74) / 0.26)
        elif norm_y < 0.04:
            edge_fade = norm_y / 0.04
        else:
            edge_fade = 1.0
        
        for gx in range(grid_w):
            r, g, b, a = resized.getpixel((gx, gy))
            if a < 25: # Skip transparent background
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

            # --- DARK MODE ---
            if lum > 0.1:
                r_dark = round((0.5 + lum * 1.15) * fade, 1)
                
                if lum > 0.62:
                    color_dark = "#F5F4F1" # Bright Ivory highlight
                    op_dark = round(min(1.0, (0.6 + lum * 0.4) * fade), 1)
                elif lum > 0.32:
                    color_dark = "#8B6F47" # Warm bronze accent
                    op_dark = round(min(1.0, (0.65 + lum * 0.35) * fade), 1)
                else:
                    color_dark = "#B5B0A6" # Muted ivory shadow detail
                    op_dark = round(min(1.0, (0.45 + lum * 0.5) * fade), 1)

                if r_dark >= 0.45 and op_dark >= 0.08:
                    key = (color_dark, op_dark)
                    if key not in dark_groups:
                        dark_groups[key] = []
                    dark_groups[key].append(f'<circle cx="{cx}" cy="{cy}" r="{r_dark}"/>')
                    total_dots_dark += 1

            # --- LIGHT MODE ---
            inv_lum = 1.0 - lum
            if inv_lum > 0.1:
                r_light = round((0.5 + inv_lum * 1.15) * fade, 1)
                
                if inv_lum > 0.55:
                    color_light = "#1A1917" # Dark graphite
                    op_light = round(min(1.0, (0.6 + inv_lum * 0.4) * fade), 1)
                elif inv_lum > 0.28:
                    color_light = "#8B6F47" # Warm bronze
                    op_light = round(min(1.0, (0.65 + inv_lum * 0.35) * fade), 1)
                else:
                    color_light = "#55524C" # Muted dark gray
                    op_light = round(min(1.0, (0.45 + inv_lum * 0.5) * fade), 1)

                if r_light >= 0.45 and op_light >= 0.08:
                    key = (color_light, op_light)
                    if key not in light_groups:
                        light_groups[key] = []
                    light_groups[key].append(f'<circle cx="{cx}" cy="{cy}" r="{r_light}"/>')
                    total_dots_light += 1

    svg_w = int(offset_x * 2 + grid_w * dot_spacing)
    svg_h = int(offset_y * 2 + grid_h * dot_spacing)

    dark_elements = []
    for (col, op), circles in dark_groups.items():
        op_attr = f' opacity="{op}"' if op < 1.0 else ''
        dark_elements.append(f'<g fill="{col}"{op_attr}>' + ''.join(circles) + '</g>')

    light_elements = []
    for (col, op), circles in light_groups.items():
        op_attr = f' opacity="{op}"' if op < 1.0 else ''
        light_elements.append(f'<g fill="{col}"{op_attr}>' + ''.join(circles) + '</g>')

    dark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="100%" height="100%">
  <title>Hamza Taif — Stipple Portrait Dark</title>
  <style>
    .stipple-portrait {{
      animation: portraitReveal 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    @keyframes portraitReveal {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .stipple-portrait {{ animation: none; opacity: 1; }}
    }}
  </style>
  <g class="stipple-portrait">
    {''.join(dark_elements)}
  </g>
</svg>'''

    light_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="100%" height="100%">
  <title>Hamza Taif — Stipple Portrait Light</title>
  <style>
    .stipple-portrait {{
      animation: portraitReveal 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    @keyframes portraitReveal {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .stipple-portrait {{ animation: none; opacity: 1; }}
    }}
  </style>
  <g class="stipple-portrait">
    {''.join(light_elements)}
  </g>
</svg>'''

    os.makedirs("assets", exist_ok=True)
    with open(output_dark, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(output_light, "w", encoding="utf-8") as f:
        f.write(light_svg)

    dark_size_kb = os.path.getsize(output_dark) / 1024.0
    light_size_kb = os.path.getsize(output_light) / 1024.0

    print(f"Generated {output_dark}: {dark_size_kb:.1f} KB ({total_dots_dark} dots)")
    print(f"Generated {output_light}: {light_size_kb:.1f} KB ({total_dots_light} dots)")
    print(f"Dimensions: {svg_w}x{svg_h} viewBox")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "hamza.png"
    generate_portrait_svg(input_file)
