"""
make_project_card.py
Hand-authored (not scraped) project showcase card in retro terminal style.
Update PROJECTS manually when you ship something new-worthy.
Writes: project-card.svg
"""

PROJECTS = [
    {
        "name": "F1 Race Position Predictor",
        "stack": "Streamlit / FastF1 / Scikit-learn",
        "desc": "Predicts race finishing position from live timing data",
        "repo": "RM-f1/F1-Race-Position-Predictor",
    },
    {
        "name": "SmartPark AI",
        "stack": "YOLOv8 / OpenCV / SQLite",
        "desc": "Smart-city parking detection ",
        "repo": "rakhiBhatt2023/SmartPark-AI-for-smart-cities",
    },
    {
        "name": "CrimePattern",
        "stack": "Random Forest",
        "desc": "Crime pattern analysis - built w/ team PixelPulse",
        "repo": "RM-f1/CrimePattern",
    },
]

# --- retro terminal palette ---
BG = "#0d1117"
BORDER = "#39d353"
TITLE = "#39d353"
NAME = "#69f0a0"
STACK = "#26a641"
DESC = "#c9d1d9"
DIM = "#6e7681"

WIDTH = 520
ROW_H = 66
HEADER_H = 40
HEIGHT = HEADER_H + ROW_H * len(PROJECTS) + 20


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
    )


def build_svg() -> str:
    rows = []
    for i, p in enumerate(PROJECTS):
        y = HEADER_H + i * ROW_H
        delay = 0.3 + i * 0.35
        rows.append(f"""
    <g class="row" style="animation-delay:{delay}s">
      <text x="24" y="{y+22}" font-family="VT323, monospace" font-size="20" fill="{NAME}">&gt; {esc(p['name'])}</text>
      <text x="24" y="{y+42}" font-family="VT323, monospace" font-size="15" fill="{STACK}">{esc(p['stack'])}</text>
      <text x="24" y="{y+60}" font-family="VT323, monospace" font-size="14" fill="{DESC}">{esc(p['desc'])}</text>
    </g>""")

    return f"""<svg viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .row {{
      opacity: 0;
      transform: translateX(-12px);
      animation: fadeSlide 0.6s ease-out forwards;
    }}
    @keyframes fadeSlide {{
      to {{ opacity: 1; transform: translateX(0); }}
    }}
  </style>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <text x="24" y="26" font-family="VT323, monospace" font-size="18" fill="{TITLE}">rm-f1@github ~ $ ./projects.sh</text>
  <line x1="0" y1="34" x2="{WIDTH}" y2="34" stroke="{DIM}" stroke-width="1"/>
  {''.join(rows)}
</svg>"""


if __name__ == "__main__":
    svg = build_svg()
    with open("project-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote project-card.svg ({len(PROJECTS)} projects, {HEIGHT}px tall)")