import os

def create_signature_svg(is_dark=True):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    text_primary = "#F5F4F1" if is_dark else "#1A1917"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#8B6F47"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 54" width="280" height="54">
  <title>Hamza Taif — Signature</title>

  <!-- Background -->
  <rect x="0" y="0" width="280" height="54" fill="{bg}" />
  <line x1="0" y1="0" x2="280" y2="0" stroke="{line_color}" stroke-width="1" />
  <line x1="0" y1="53" x2="280" y2="53" stroke="{line_color}" stroke-width="1" />

  <!-- Left Accent Line -->
  <rect x="0" y="0" width="2" height="54" fill="{accent}" />

  <!-- Pure Typographic Signature -->
  <text x="24" y="24" font-family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="13" font-weight="800" fill="{text_primary}" letter-spacing="2.5">HAMZA TAIF</text>
  <text x="24" y="41" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="9" font-weight="600" fill="{accent}" letter-spacing="1.5">SOFTWARE ENGINEERING  ·  2026</text>
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    with open("assets/signature-dark.svg", "w", encoding="utf-8") as f:
        f.write(create_signature_svg(is_dark=True))
    with open("assets/signature-light.svg", "w", encoding="utf-8") as f:
        f.write(create_signature_svg(is_dark=False))
    print("Generated assets/signature-dark.svg and assets/signature-light.svg (pure typography signature).")

if __name__ == "__main__":
    main()
