"""Regenerate the project cards: python3 assets/build.py (header lives in planet.py)"""
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



(OUT / "cards").mkdir(exist_ok=True)
for f, *rest in PROJECTS:
    (OUT / "cards" / f"{f}.svg").write_text(card(*rest))
