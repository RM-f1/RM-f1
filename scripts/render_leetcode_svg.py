"""
render_leetcode_svg.py
Reads data/leetcode.json, renders a retro terminal streak card.
Streak-only display - no solved-question count shown.
Writes: leetcode-card.svg
"""

import json

BG = "#0d1117"
BORDER = "#39d353"
TITLE = "#39d353"
LABEL = "#6e7681"
FLAME = "#ffb347"
SUB = "#26a641"

WIDTH = 400
HEIGHT = 150


def load_data():
    with open("data/leetcode.json", "r", encoding="utf-8") as f:
        return json.load(f)


def build_svg(d: dict) -> str:
    current = d["current_streak"]
    longest = d["longest_streak"]

    return f"""<svg viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .cell {{
      opacity: 0;
      transform: translateY(8px);
      animation: fadeUp 0.5s ease-out forwards;
    }}
    @keyframes fadeUp {{
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <text x="24" y="28" font-family="VT323, monospace" font-size="18" fill="{TITLE}">rm-f1@github ~ $ ./leetcode.sh</text>
  <line x1="0" y1="36" x2="{WIDTH}" y2="36" stroke="{LABEL}" stroke-width="1"/>

  <g class="cell" style="animation-delay:0.25s">
    <text x="24" y="90" font-family="VT323, monospace" font-size="46" fill="{FLAME}">{current}</text>
    <text x="90" y="90" font-family="VT323, monospace" font-size="20" fill="{LABEL}">day streak</text>
  </g>

  <g class="cell" style="animation-delay:0.55s">
    <text x="24" y="120" font-family="VT323, monospace" font-size="15" fill="{SUB}">best: {longest} days</text>
  </g>
</svg>"""


def main():
    data = load_data()
    svg = build_svg(data)
    with open("leetcode-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote leetcode-card.svg - {data['current_streak']}d current / {data['longest_streak']}d best")


if __name__ == "__main__":
    main()