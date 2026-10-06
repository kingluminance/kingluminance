"""Regenerate the profile SVGs: python3 assets/build.py"""
import random
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
GOLD, INK, BG, MUTED = "#f5c451", "#e6edf3", "#0b1020", "#8b98b8"

# (file, emoji, name, description, language, language color, status)
PROJECTS = [
    ("cartotree", "🌳", "cartotree",
     "Annotated directory trees for AI context. Map a codebase once, spend fewer tokens forever.",
     "JavaScript", "#f1e05a", "npm"),
    ("arc-agi-3", "🧩", "arc-agi-3",
     "An agent for ARC Prize 2026 that figures out wordless grid games by itself, driven by discomfort rather than reward.",
     "Python", "#3572A5", "private · Kaggle"),
    ("desktop-pet", "🐾", "desktop-pet",
     "A featherweight pet that wanders your desktop and taskbar. Anyone can draw one and share it on the Workshop.",
     "C++", "#f34b7d", "private"),
    ("shelter-connect", "🐶", "shelter-connect",
     "Meet shelter dogs as pixel characters first. Talk, learn their habits, and only then see the photo.",
     "TypeScript", "#3178c6", "React Native"),
    ("analog-horror", "🌞", "analog_horror",
     "Daylight horror you explore on foot. Bright grass, wide FOV, and strange things that exist as if they always had.",
     "GDScript", "#355570", "private"),
    ("topside-battle", "⚔️", "TopSide-Battle",
     "1v1 online shooter that flips between top-down and side view each round. The loser picks an augment.",
     "GDScript", "#355570", "multiplayer"),
    ("doda", "🦋", "doda",
     "A story adventure about friends crossing between an animal village and a plant village.",
     "GDScript", "#355570", "private"),
]


def card(emoji, name, desc, lang, color, status):
    lines = textwrap.wrap(desc, 58)[:3]
    body = "".join(
        f'<text x="24" y="{78 + i * 20}" class="d">{escape(l)}</text>' for i, l in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="440" height="170" viewBox="0 0 440 170">
<style>
text{{font-family:{FONT}}}
.n{{font-size:18px;font-weight:700;fill:{INK}}}
.d{{font-size:13px;fill:{MUTED}}}
.m{{font-size:12px;fill:{MUTED}}}
</style>
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#121a30"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>
<rect x="1" y="1" width="438" height="168" rx="14" fill="url(#g)" stroke="#26304a"/>
<rect x="1" y="1" width="4" height="168" rx="2" fill="{GOLD}" opacity=".85"/>
<text x="24" y="44" font-size="20">{emoji}</text>
<text x="54" y="44" class="n">{escape(name)}</text>
{body}
<circle cx="30" cy="146" r="5" fill="{color}"/>
<text x="42" y="150" class="m">{lang}</text>
<text x="416" y="150" class="m" text-anchor="end" style="fill:{GOLD}">{escape(status)}</text>
</svg>
"""


def header():
    rnd = random.Random(7)
    stars = "".join(
        f'<circle cx="{rnd.randint(0, 1000)}" cy="{rnd.randint(0, 260)}" r="{rnd.choice([0.6, 0.9, 1.2, 1.6])}" fill="#fff">'
        f'<animate attributeName="opacity" values=".15;.9;.15" dur="{rnd.uniform(2.5, 6):.1f}s" '
        f'begin="{rnd.uniform(0, 5):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(70)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="260" viewBox="0 0 1000 260">
<style>
text{{font-family:{FONT}}}
</style>
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#151d3b"/><stop offset=".6" stop-color="{BG}"/><stop offset="1" stop-color="#070a14"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{GOLD}" stop-opacity=".35"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<radialGradient id="planet" cx=".35" cy=".3"><stop offset="0" stop-color="#ffe7a3"/><stop offset=".55" stop-color="{GOLD}"/><stop offset="1" stop-color="#b9792a"/></radialGradient>
<clipPath id="r"><rect width="1000" height="260" rx="18"/></clipPath>
</defs>
<g clip-path="url(#r)">
<rect width="1000" height="260" fill="url(#sky)"/>
{stars}
<circle cx="820" cy="135" r="150" fill="url(#glow)"/>
<ellipse cx="820" cy="135" rx="105" ry="30" fill="none" stroke="{GOLD}" stroke-opacity=".25" transform="rotate(-14 820 135)"/>
<g>
<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="6s" repeatCount="indefinite"/>
<circle cx="820" cy="135" r="52" fill="url(#planet)"/>
<path d="M820 63 l-14 24 h9 l-12 18 h34 l-12 -18 h9 z" fill="#2f6b4f"/>
<rect x="817" y="105" width="6" height="8" fill="#5a3b22"/>
<path d="M776 120 q44 -14 88 0" fill="none" stroke="#b9792a" stroke-opacity=".5" stroke-width="2"/>
</g>
<circle r="7" fill="#c9d1d9">
<animateMotion dur="9s" repeatCount="indefinite" path="M925 109 A105 30 -14 1 1 715 161 A105 30 -14 1 1 925 109"/>
</circle>
<text x="70" y="118" font-size="52" font-weight="800" fill="{INK}">Wang Hwi Do</text>
<text x="72" y="158" font-size="18" fill="{MUTED}">A developer who builds small worlds —</text>
<text x="72" y="184" font-size="18" fill="{MUTED}">tools, games, and the maps in between.</text>
<text x="72" y="222" font-size="13" fill="{GOLD}" letter-spacing="3">KINGLUMINANCE · KOREA</text>
</g>
</svg>
"""


(OUT / "header.svg").write_text(header())
(OUT / "cards").mkdir(exist_ok=True)
for f, *rest in PROJECTS:
    (OUT / "cards" / f"{f}.svg").write_text(card(*rest))
