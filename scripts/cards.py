import os
import json
import urllib.request

def fetch_repo_meta(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    headers = {"User-Agent": "HamzaTaif-Profile-Generator"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return {
                    "stars": data.get("stargazers_count", 0),
                    "forks": data.get("forks_count", 0),
                    "language": data.get("language", ""),
                    "url": data.get("html_url", f"https://github.com/{username}/{repo_name}")
                }
    except Exception:
        pass
    return None

def create_card_svg(project, is_dark=True, meta=None):
    bg = "#0D0C0A" if is_dark else "#FAF9F6"
    text_primary = "#F5F4F1" if is_dark else "#1A1917"
    text_muted = "#A6A29A" if is_dark else "#6E6A63"
    line_color = "#3A3935" if is_dark else "#E2E0D8"
    accent = "#8B6F47"
    tag_bg = "rgba(139, 111, 71, 0.10)" if is_dark else "rgba(139, 111, 71, 0.12)"

    num = project.get("number", "01")
    name = project.get("name", "").upper()
    desc = project.get("description", "")
    techs = project.get("technologies", [])
    p_id = project.get("id", "")
    
    # Only show VIEW REPOSITORY link for verified public repos (CloudGuardian AI)
    show_repo_link = (p_id == "cloudguardian" or (meta and meta.get("stars", 0) > 0))

    meta_str = ""
    if meta:
        stars = meta.get("stars", 0)
        forks = meta.get("forks", 0)
        parts = []
        if stars > 0:
            parts.append(f"★ {stars}")
        if forks > 0:
            parts.append(f"⑂ {forks}")
        if parts:
            meta_str = " · ".join(parts)

    tech_pills = ""
    tx = 0
    for t in techs:
        width = len(t) * 8.5 + 20
        tech_pills += f'''<g transform="translate({tx}, 0)">
          <rect x="0" y="0" width="{width}" height="24" rx="5" fill="{tag_bg}" stroke="{line_color}" stroke-width="0.9" />
          <text x="{width/2}" y="16" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11" font-weight="600" fill="{accent}" text-anchor="middle">{t}</text>
        </g>'''
        tx += width + 10

    meta_text_element = ""
    if meta_str:
        meta_text_element = f'''<text x="820" y="38" font-family="ui-monospace, monospace" font-size="11" fill="{text_muted}" text-anchor="end">{meta_str}</text>'''

    link_element = ""
    if show_repo_link:
        link_element = f'''<text x="820" y="118" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="{accent}" text-anchor="end">VIEW REPOSITORY ↗</text>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 148" width="100%" height="100%">
  <title>{name} — Case Study Card</title>

  <!-- Background Card -->
  <rect x="0" y="0" width="850" height="148" rx="8" fill="{bg}" stroke="{line_color}" stroke-width="1" />
  <rect x="0" y="0" width="3.5" height="148" fill="{accent}" />

  <!-- Oversized Index Number -->
  <text x="26" y="48" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="28" font-weight="800" fill="{accent}" letter-spacing="1">{num}</text>
  <line x1="68" y1="24" x2="68" y2="48" stroke="{line_color}" stroke-width="1" />

  <!-- Title -->
  <text x="82" y="42" font-family="system-ui, -apple-system, sans-serif" font-size="19" font-weight="800" fill="{text_primary}" letter-spacing="1">{name}</text>
  {meta_text_element}

  <!-- Description -->
  <text x="26" y="78" font-family="system-ui, -apple-system, sans-serif" font-size="13.5" font-weight="400" fill="{text_muted}">{desc}</text>

  <!-- Tech Stack Pills -->
  <g transform="translate(26, 102)">
    {tech_pills}
  </g>

  <!-- Arrow Link Indicator (Only if verified) -->
  {link_element}
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    with open("config/projects.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    username = config.get("username", "HamzaTaif")
    projects = config.get("projects", [])

    for p in projects:
        p_id = p.get("id")
        repo_name = p.get("repo")
        meta = fetch_repo_meta(username, repo_name)
        
        dark_svg = create_card_svg(p, is_dark=True, meta=meta)
        light_svg = create_card_svg(p, is_dark=False, meta=meta)

        with open(f"assets/project-{p_id}-dark.svg", "w", encoding="utf-8") as f:
            f.write(dark_svg)
        with open(f"assets/project-{p_id}-light.svg", "w", encoding="utf-8") as f:
            f.write(light_svg)
        print(f"Generated assets/project-{p_id}-dark.svg and light SVG (enlarged GitHub scale)")

if __name__ == "__main__":
    main()
