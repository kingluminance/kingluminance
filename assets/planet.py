"""Living planet header.

python3 assets/planet.py STATE.json OUT.svg                 # re-render (sky follows KST)
python3 assets/planet.py STATE.json OUT.svg plant LOGIN     # prints planted | exists
python3 assets/planet.py STATE.json OUT.svg uproot LOGIN    # prints uprooted | missing
python3 assets/planet.py test
"""
import hashlib
import json
import math
import random
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

W, H = 1000, 450
CX, R, TOP = 500, 1600, 300          # ground = circle centred (CX, TOP + R)
CAP, GREEN = 20, 16                  # trees kept / newest trees that stay green
SLOTS, X0, X1 = 27, 90, 910
LANDMARK_SLOTS = [0, 4, 9, 13, 17, 22, 26]
TREE_SLOTS = [i for i in range(SLOTS) if i not in LANDMARK_SLOTS]
LOGIN_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
GOLD = "#f5c451"
KST = timezone(timedelta(hours=9))

# phase: sky top, sky mid, horizon, title, subtitle, grass, soil
SKY = {
    "dawn":  ("#2b2d5c", "#b77fa6", "#ffd1a1", "#ffffff", "#f3e6f0", "#7fbf7a", "#3f6b4a"),
    "day":   ("#3d8fd6", "#7cc0ef", "#d6efff", "#0b1020", "#24324f", "#78c46e", "#3d7a4c"),
    "dusk":  ("#2d1b4e", "#c4527a", "#ffb067", "#ffffff", "#ffe2cc", "#6aa86a", "#344f3f"),
    "night": ("#151d3b", "#0f1630", "#0b1020", "#e6edf3", "#8b98b8", "#3f7a5a", "#18302a"),
}
LEAVES = ["#4caf50", "#2e8b57", "#7cb342", "#f48fb1", "#ffb74d", "#26a69a", "#9ccc65", "#e57373"]


def phase(now=None):
    h = (now or datetime.now(timezone.utc)).astimezone(KST).hour
    return "dawn" if 6 <= h < 10 else "day" if 10 <= h < 17 else "dusk" if 17 <= h < 20 else "night"


def seed(login):
    return int(hashlib.sha256(login.lower().encode()).hexdigest(), 16)


# ---------- state ----------

def plant(trees, login, now):
    if any(t["login"].lower() == login.lower() for t in trees):
        return "exists"
    while len(trees) >= CAP:
        trees.pop(0)                                    # oldest makes room
    taken = {t["slot"] for t in trees}
    free = [s for s in TREE_SLOTS if s not in taken]
    trees.append({"login": login, "slot": free[seed(login) % len(free)], "at": now})
    return "planted"


def uproot(trees, login):
    keep = [t for t in trees if t["login"].lower() != login.lower()]
    result = "uprooted" if len(keep) < len(trees) else "missing"
    trees[:] = keep
    return result


# ---------- drawing ----------

def on_ground(slot):
    x = X0 + slot * (X1 - X0) / (SLOTS - 1)
    a = math.asin((x - CX) / R)
    return x, TOP + R - R * math.cos(a), math.degrees(a)


def label(text, color):
    t = text if len(text) <= 16 else text[:15] + "…"
    return (f'<text transform="rotate(90)" x="12" y="3" font-size="9" fill="{color}" '
            f'opacity=".85">{escape(t)}</text>')


def sway(s, amp=2.5):
    return (f'<animateTransform attributeName="transform" type="rotate" '
            f'values="-{amp};{amp};-{amp}" dur="{4 + s % 4}s" repeatCount="indefinite"/>')


def tree(login, withered):
    s = seed(login)
    h = 26 + s % 18
    if withered:
        body = (f'<path d="M0 0V{-h} M0 {-h * .6:.0f}l-8 -8 M0 {-h * .75:.0f}l7 -9 M0 {-h * .9:.0f}l-5 -6" '
                f'stroke="#7d746a" stroke-width="2.4" stroke-linecap="round" fill="none"/>')
        return f'<g>{body}</g>'
    leaf = LEAVES[(s >> 8) % len(LEAVES)]
    trunk = f'<rect x="-2" y="{-h * .55:.0f}" width="4" height="{h * .55:.0f}" rx="1" fill="#6b4a2b"/>'
    kind = (s >> 16) % 4
    if kind == 0:    # round
        crown = f'<circle cy="{-h * .72:.1f}" r="{h * .34:.1f}" fill="{leaf}"/>'
    elif kind == 1:  # pine
        crown = "".join(
            f'<path d="M0 {-h + i * h * .22:.1f} l{-h * (.22 + i * .07):.1f} {h * .32:.1f} h{h * (.44 + i * .14):.1f}z" fill="{leaf}"/>'
            for i in range(3))
    elif kind == 2:  # poplar
        crown = f'<ellipse cy="{-h * .62:.1f}" rx="{h * .17:.1f}" ry="{h * .42:.1f}" fill="{leaf}"/>'
    else:            # blossom
        crown = "".join(f'<circle cx="{dx * h:.1f}" cy="{dy * h:.1f}" r="{h * .2:.1f}" fill="{leaf}"/>'
                        for dx, dy in ((-.16, -.62), (.16, -.62), (0, -.82)))
    return f'<g>{sway(s)}{trunk}{crown}</g>'


def landmark(name):
    if name == "cartotree":
        return ('<rect x="-4" y="-36" width="8" height="36" rx="2" fill="#6b4a2b"/>'
                f'<g>{sway(3, 1.5)}<circle cy="-50" r="22" fill="{GOLD}"/><circle cx="-15" cy="-38" r="13" fill="#e9b23f"/>'
                '<circle cx="15" cy="-38" r="13" fill="#e9b23f"/></g>')
    if name == "desktop-pet":
        return ('<path d="M10 -6 q16 -4 12 -22" stroke="#f0a35e" stroke-width="4" fill="none" stroke-linecap="round">'
                '<animateTransform attributeName="transform" type="rotate" values="0 10 -6;12 10 -6;0 10 -6" dur="2s" repeatCount="indefinite"/></path>'
                '<ellipse cy="-9" rx="12" ry="9" fill="#f0a35e"/><circle cx="-7" cy="-22" r="8" fill="#f0a35e"/>'
                '<path d="M-14 -26 l2 -9 5 6z M-1 -26 l-1 -9 -5 6z" fill="#f0a35e"/>'
                '<circle cx="-10" cy="-23" r="1.3" fill="#2b2b33"/><circle cx="-4" cy="-23" r="1.3" fill="#2b2b33"/>')
    if name == "analog_horror":
        petals = "".join(f'<ellipse cx="0" cy="-48" rx="4" ry="9" fill="#ffd54f" transform="rotate({a} 0 -38)"/>'
                         for a in range(0, 360, 30))
        return ('<path d="M0 0 V-34" stroke="#4e8b3a" stroke-width="3"/><path d="M0 -14 q-10 -2 -12 -10 q9 0 12 10z" fill="#4e8b3a"/>'
                f'<g>{sway(5, 6)}{petals}<circle cy="-38" r="9" fill="#8d5a2b"/>'
                '<circle cx="-3" cy="-40" r="1.4" fill="#1a1a1a"/><circle cx="3" cy="-40" r="1.4" fill="#1a1a1a"/>'
                '<path d="M-5 -35 q5 4 10 0" stroke="#1a1a1a" stroke-width="1.2" fill="none"/></g>')
    if name == "TopSide-Battle":
        flag = ('<path d="M{x} -38 h{d} l{e} 5 l-{e} 5 h-{d}z" fill="{c}">'
                '<animate attributeName="opacity" values="1;.75;1" dur="1.6s" repeatCount="indefinite"/></path>')
        return ('<path d="M-6 0 V-40 M6 0 V-40" stroke="#c9c9c9" stroke-width="2"/>'
                + flag.format(x=-6, d=-14, e=-3, c="#e5533d") + flag.format(x=6, d=14, e=3, c="#3d7fe5"))
    if name == "doda":
        return ('<path d="M0 0 V-14" stroke="#4e8b3a" stroke-width="2"/><circle cy="-16" r="4" fill="#f48fb1"/>'
                '<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="3s" repeatCount="indefinite"/>'
                '<g transform="translate(0 -38)"><path d="M0 0 c-12 -12 -16 2 -2 4 c-12 4 -6 12 2 2z M0 0 c12 -12 16 2 2 4 c12 4 6 12 -2 2z" fill="#9fa8ff">'
                '<animateTransform attributeName="transform" type="scale" values="1 1;.3 1;1 1" dur=".6s" repeatCount="indefinite"/></path></g></g>')
    if name == "arc-agi-3":
        cols = ["#0074d9", "#ff4136", "#2ecc40", "#ffdc00", "#aaaaaa", "#f012be", "#ff851b", "#7fdbff", "#870c25"]
        cells = "".join(f'<rect x="{-12 + (i % 3) * 8}" y="{-26 + (i // 3) * 8}" width="7" height="7" fill="{c}">'
                        + (f'<animate attributeName="opacity" values="1;.2;1" dur="2.4s" begin="{i * .3:.1f}s" repeatCount="indefinite"/>' if i in (2, 6) else "")
                        + '</rect>' for i, c in enumerate(cols))
        return f'<rect x="-14" y="-28" width="27" height="28" rx="2" fill="#1b1f2a"/>{cells}'
    if name == "shelter-connect":
        return ('<rect x="-14" y="-20" width="28" height="20" fill="#c98b5a"/><path d="M-18 -19 L0 -34 L18 -19z" fill="#d9534f"/>'
                '<path d="M-6 0 v-8 a6 6 0 0 1 12 0 v8z" fill="#3b2a1e"/>')
    return ""


LANDMARKS = ["cartotree", "arc-agi-3", "desktop-pet", "shelter-connect", "analog_horror", "TopSide-Battle", "doda"]


def sky(p, top, mid, low):
    rnd = random.Random(7)
    out = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    if p in ("night", "dawn"):
        n, op = (70, ".9") if p == "night" else (25, ".5")
        out += [f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(0, 240)}" r="{rnd.choice([.6, .9, 1.2, 1.6])}" fill="#fff">'
                f'<animate attributeName="opacity" values=".1;{op};.1" dur="{rnd.uniform(2.5, 6):.1f}s" '
                f'begin="{rnd.uniform(0, 5):.1f}s" repeatCount="indefinite"/></circle>' for _ in range(n)]
    if p == "night":
        out.append('<mask id="moon"><rect width="1000" height="300" fill="#fff"/><circle cx="862" cy="82" r="24"/></mask>'
                   '<circle cx="850" cy="90" r="80" fill="url(#glow)"/><circle cx="850" cy="90" r="26" fill="#f4f1de" mask="url(#moon)"/>')
    elif p == "day":
        out.append('<circle cx="840" cy="85" r="90" fill="url(#glow)"/><circle cx="840" cy="85" r="30" fill="#ffe066"/>')
        for i, (x, y, s) in enumerate(((560, 70, 1), (700, 150, .7), (300, 230, .8))):
            out.append(f'<g opacity=".9"><animateTransform attributeName="transform" type="translate" values="0 0;40 0;0 0" '
                       f'dur="{30 + i * 9}s" repeatCount="indefinite"/><g transform="translate({x} {y}) scale({s})" fill="#fff">'
                       '<ellipse rx="34" ry="12"/><ellipse cx="-14" cy="-8" rx="16" ry="12"/><ellipse cx="12" cy="-12" rx="18" ry="14"/></g></g>')
    else:
        x, c = (860, "#ffb36b") if p == "dawn" else (820, "#ff8a4c")
        out.append(f'<circle cx="{x}" cy="275" r="140" fill="url(#glow)"/><circle cx="{x}" cy="275" r="38" fill="{c}"/>')
    return "".join(out)


def render(trees, p):
    top, mid, low, title, sub, grass, soil = SKY[p]
    glow = {"night": "#f4f1de", "day": "#fff3b0"}.get(p, "#ffb36b")
    objs = []
    for slot, name in zip(LANDMARK_SLOTS, LANDMARKS):
        x, y, a = on_ground(slot)
        objs.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({a:.2f})">{landmark(name)}{label(name, GOLD)}</g>')
    old = len(trees) - GREEN
    for i, t in enumerate(trees):
        x, y, a = on_ground(t["slot"])
        objs.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({a:.2f})">'
                    f'{tree(t["login"], i < old)}{label("@" + t["login"], "#e8f5e9")}</g>')
    count = f"{len(trees)} tree{'s' if len(trees) != 1 else ''} planted by visitors"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>text{{font-family:{FONT}}}</style>
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset=".55" stop-color="{mid}"/><stop offset="1" stop-color="{low}"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{glow}" stop-opacity=".45"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
<linearGradient id="soil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{soil}"/><stop offset=".08" stop-color="#2a1f17"/><stop offset="1" stop-color="#120d0a"/></linearGradient>
<clipPath id="r"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#r)">
{sky(p, top, mid, low)}
<circle cx="{CX}" cy="{TOP + R}" r="{R}" fill="url(#soil)" stroke="{grass}" stroke-width="7"/>
{"".join(objs)}
<text x="64" y="104" font-size="52" font-weight="800" fill="{title}">Wang Hwi Do</text>
<text x="66" y="144" font-size="18" fill="{sub}">A developer who builds small worlds —</text>
<text x="66" y="170" font-size="18" fill="{sub}">tools, games, and the maps in between.</text>
<text x="66" y="206" font-size="13" fill="{"#a8670f" if p == "day" else GOLD}" letter-spacing="3">KINGLUMINANCE · KOREA</text>
<text x="{W - 24}" y="{H - 14}" font-size="11" fill="#e8f5e9" opacity=".6" text-anchor="end">{count}</text>
</g>
</svg>
"""


def test():
    trees = []
    assert plant(trees, "alice", "t") == "planted"
    assert plant(trees, "ALICE", "t") == "exists"
    for i in range(CAP + 5):
        plant(trees, f"user{i}", "t")
    assert len(trees) == CAP and trees[0]["login"] == "user5"            # oldest gone
    assert len({t["slot"] for t in trees}) == CAP                        # no shared slots
    assert set(t["slot"] for t in trees) <= set(TREE_SLOTS)
    assert uproot(trees, "user5") == "uprooted" and uproot(trees, "user5") == "missing"
    assert plant(trees, "alice", "t") == "planted"                       # gone people may return
    assert not LOGIN_RE.match("a b") and not LOGIN_RE.match("x<y") and LOGIN_RE.match("king-lum1")
    assert [phase(datetime(2026, 1, 1, h, tzinfo=KST)) for h in (7, 12, 18, 23)] == ["dawn", "day", "dusk", "night"]
    for p in SKY:
        assert render(trees, p).count("<svg") == 1
    print("ok")


def main(argv):
    if argv[:1] == ["test"]:
        return test()
    state, out, *cmd = argv
    path = Path(state)
    trees = json.loads(path.read_text())["trees"] if path.exists() else []
    result = ""
    if cmd:
        verb, login = cmd
        if not LOGIN_RE.match(login):
            sys.exit(f"bad login: {login!r}")
        result = plant(trees, login, datetime.now(timezone.utc).isoformat(timespec="seconds")) if verb == "plant" else uproot(trees, login)
    path.write_text(json.dumps({"trees": trees}, indent=1) + "\n")
    Path(out).write_text(render(trees, phase()))
    print(result)


if __name__ == "__main__":
    main(sys.argv[1:])
