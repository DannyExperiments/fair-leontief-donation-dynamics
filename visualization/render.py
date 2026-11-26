"""Regenerate the exact data, rotating GIF, checksums, and offline bundle."""

import argparse
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from json import dumps
from math import cos, pi, radians, sin
from pathlib import Path
from re import DOTALL, sub
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

HERE = Path(__file__).resolve().parent
WEIGHTS = ((1, 1, 0), (0, 1, 1), (1, 0, 2))
TARGET = (F(1), F(1), F(1))
FIRST, LAST = 3, 15
NAMES = ("A", "B", "C")

BACKGROUND = "#101824"
PANEL = "#162331"
INK = "#f5f8fb"
MUTED = "#b4c7d5"
RULE = "#415867"
GRID = "#365561"
FACE = "#1b3543"
AXES = ("#f9ac8d", "#b6d696", "#87d4ee")
PATH = "#64afbe"
AQUA = "#91f0e7"
GOLD = "#ffd184"
SIZE = (672, 622)
GIF_NAME = "fair-schedule.gif"
ZIP_NAME = "fair-leontief-explorer.zip"


def best_response(others, weights):
    """Solve the budget equation exactly by testing the supported active sets."""
    support = tuple(x for x, weight in enumerate(weights) if weight)
    for k in range(1, len(support) + 1):
        for active in combinations(support, k):
            level = (1 + sum(others[x] for x in active)) / sum(weights[x] for x in active)
            response = tuple(max(F(0), level * weight - value) for value, weight in zip(others, weights))
            if sum(response) == 1:
                assert min((b + q) / v for b, q, v in zip(others, response, weights) if v) == level
                return level, response
    raise ValueError("No supported unit-budget best response")


def step_schedule(max_round):
    """Yield A, B repeated k times, then C, for k = 1, 2, ... ."""
    t = 0
    k = 1
    while t < max_round:
        for i in (0, 1) * k + (2,):
            t += 1
            yield t, i
            if t == max_round:
                return
        k += 1


def example():
    state = [(F(0),) * 3] * 3
    rounds = []
    for t, i in step_schedule(48):
        others = tuple(sum((state[j][x] for j in range(3) if j != i), F(0)) for x in range(3))
        previous = state[i]
        level, state[i] = best_response(others, WEIGHTS[i])
        total = tuple(map(sum, zip(*state)))
        rounds.append({
            "round": t,
            "donor": NAMES[i],
            "level": str(level),
            "previous": list(map(str, previous)),
            "response": list(map(str, state[i])),
            "others": list(map(str, others)),
            "total": list(map(str, total)),
            "point": list(map(float, total)),
            "changed": state[i] != previous,
        })
        if t >= FIRST:
            assert sum(total) == 3
        if t >= 8:
            assert state[2] == (0, 0, 1)
        if t > 8 and i == 0:
            assert state[0][1] == state[1][2] / 2
        if t > 8 and i == 1:
            assert state[1][2] == state[0][1] / 2
    assert [r["round"] for r in rounds if r["donor"] == "C"] == [3, 8, 15, 24, 35, 48]
    assert rounds[2]["total"] == ["3/4", "3/4", "3/2"]
    assert rounds[6]["total"] == ["15/16", "33/32", "33/32"]
    assert rounds[7]["total"] == ["11/16", "33/32", "41/32"]
    assert rounds[7]["level"] == "41/64"
    assert rounds[7]["response"] == ["0", "0", "1"]
    assert rounds[14]["total"] == rounds[13]["total"]
    assert all(
        min(F(n) for n in row["total"]) >= F(1, 2)
        for row in rounds[FIRST - 1:LAST]
    )
    equilibrium_blocks = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
    for i, weights in enumerate(WEIGHTS):
        others = tuple(d - w for d, w in zip(TARGET, equilibrium_blocks[i]))
        assert best_response(others, weights)[1] == equilibrium_blocks[i]
    return rounds


def embed_html(rounds):
    file = HERE / "index.html"
    current = file.read_text(encoding="utf-8")
    encoded = dumps(rounds[:LAST], separators=(",", ":"))
    updated = sub(
        r'(?<=<script id="exact-rounds" type="application/json">).*?(?=</script>)',
        lambda _: encoded,
        current,
        count=1,
        flags=DOTALL,
    )
    if updated == current and encoded not in current:
        raise ValueError("Missing the data element in index.html")
    file.write_text(updated, encoding="utf-8")


def default_fonts():
    pairs = (
        ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    )
    return next(((a, b) for a, b in pairs if Path(a).is_file() and Path(b).is_file()), (None, None))


def make_frame(angle, tick, rows, regular, bold, image_modules):
    Image, ImageDraw, ImageFont = image_modules
    im = Image.new("RGB", SIZE, BACKGROUND)
    draw = ImageDraw.Draw(im)

    @lru_cache(maxsize=None)
    def font(size, heavy=False):
        return ImageFont.truetype(bold if heavy else regular, size)

    def label(x, y, text, size, color=INK, heavy=False, anchor="lt"):
        face = font(size, heavy)
        left, top, right, bottom = draw.textbbox((x, y), text, font=face, anchor=anchor)
        if left < 0 or top < 0 or right > SIZE[0] or bottom > SIZE[1]:
            raise ValueError(f"Text overflows the GIF frame: {text}")
        draw.text((x, y), text, font=face, fill=color, anchor=anchor)

    elev = radians(64 + 3 * cos(angle))
    c_yaw, s_yaw = cos(angle), sin(angle)
    c_elev, s_elev = cos(elev), sin(elev)

    def project(point):
        x, y, z = (float(v) - 1 for v in point)
        u = c_yaw * x - s_yaw * y
        depth = s_yaw * x + c_yaw * y
        v = c_elev * z - s_elev * depth
        return (336 + 116 * u, 241 - 116 * v)

    def line(points, color, width=1):
        draw.line([project(p) for p in points], fill=color, width=width)

    def dot(point, radius, fill, border=None, width=1):
        x, y = project(point)
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=fill, outline=border, width=width)

    draw.rounded_rectangle((22, 98, 650, 418), radius=19, fill=PANEL)
    label(27, 22, "A fair donation schedule", 36, heavy=True)
    label(28, 65, "Exact best responses for three donors", 23, MUTED)

    vertices = ((2, .5, .5), (.5, 2, .5), (.5, .5, 2))
    draw.polygon([project(p) for p in vertices], fill=FACE)
    line((*vertices, vertices[0]), RULE, 2)
    for fixed in (0, 1, 2):
        for value in (0.75, 1.0, 1.25, 1.5, 1.75):
            a = [0.5] * 3
            b = [0.5] * 3
            a[fixed] = b[fixed] = value
            a[(fixed+1) % 3] = b[(fixed+2) % 3] = 2.5-value
            line((a,b), GRID, 1)

    origin = (0.5, 0.5, 0.5)
    for j, (vertex, color) in enumerate(zip(vertices, AXES)):
        line((origin, vertex), color, 2)
        x, y = project(vertex)
        center_x, center_y = project((1, 1, 1))
        offset = x - center_x if abs(x-center_x) > 7 else 15
        label(x + (10 if offset > 0 else -10), y - 7, "XYZ"[j], 22, color, True,
              anchor="lt" if offset > 0 else "rt")

    shown = rows[FIRST - 1:tick]
    for a, b in zip(shown, shown[1:]):
        line((a["point"], b["point"]), PATH, 3)
    for row in shown[:-1]:
        dot(row["point"], 3, PATH)
    current = shown[-1]
    accent = GOLD if current["donor"] == "C" else AQUA
    dot(TARGET, 11, None, INK, 2)
    dot(current["point"], 6, accent, PANEL, 1)

    # Keep the explanatory labels fixed on screen during the 3-D rotation.
    draw.ellipse((40, 395, 52, 407), fill=accent)
    label(60, 392, "Current total", 19)
    draw.ellipse((264, 395, 276, 407), outline=INK, width=2)
    label(285, 392, "Nash target (1, 1, 1)", 19)
    label(496, 392, "X + Y + Z = 3", 19, MUTED)

    label(28, 437, f'Round {tick}  ·  Donor {current["donor"]}', 27, accent, True)
    label(29, 475, "Total (X, Y, Z) = (" + ", ".join(current["total"]) + ")", 24)
    if tick == FIRST:
        caption = "All three budgets are now allocated."
    elif tick == 8:
        caption = "C moves 1/4 unit from X to Z."
    elif not current["changed"]:
        caption = f'Donor {current["donor"]} keeps the same allocation.'
    else:
        caption = "C has moved once." if tick < 8 else "C has moved twice."
    label(29, 509, caption, 21, MUTED)
    draw.line((28, 543, 644, 543), fill=RULE, width=1)
    label(29, 555, "C’s turns: 3, 8, 15, 24, …    Gaps: 5, 7, 9, …", 22, heavy=True)
    label(29, 587, "Finite replay. The paper proves every fair schedule.", 20, MUTED)
    return im


def render_gif(rounds, regular, bold):
    from PIL import Image, ImageDraw, ImageFont
    frames = []
    frames_per_round = 3
    count = (LAST - FIRST + 1) * frames_per_round
    for frame in range(count):
        phase = 2 * pi * frame / count
        tick = FIRST + frame // frames_per_round
        rgb = make_frame(phase + .38, tick, rounds, regular, bold, (Image, ImageDraw, ImageFont))
        frame = rgb.quantize(colors=48, dither=Image.Dither.NONE)
        frames.append(frame)
    durations = [115] * count
    for tick in (FIRST, 8, LAST):
        start = (tick - FIRST) * frames_per_round
        durations[start:start + frames_per_round] = [155] * frames_per_round
    frames[0].save(HERE / GIF_NAME, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=True, disposal=1)


def archive():
    assets = [HERE / name for name in ("index.html", GIF_NAME, "README.md", "render.py")]
    checksum = HERE / "SHA256SUMS.txt"
    checksum.write_text(
        "".join(f"{sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in assets),
        encoding="utf-8",
    )
    with ZipFile(HERE / ZIP_NAME, "w") as out:
        for path in (*assets, checksum):
            out.writestr(ZipInfo(path.name), path.read_bytes(), compress_type=ZIP_DEFLATED,
                         compresslevel=9)


def main():
    default_regular, default_bold = default_fonts()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regular", default=default_regular, help="Path to a regular TrueType font")
    parser.add_argument("--bold", default=default_bold, help="Path to a bold TrueType font")
    parser.add_argument("--check-only", action="store_true", help="Check exact arithmetic without rendering")
    args = parser.parse_args()
    rounds = example()
    print(f"Checked {len(rounds)} exact best responses. Round 8 total: {rounds[7]['total']}")
    if args.check_only:
        return
    if not (args.regular and args.bold):
        parser.error("Specify --regular and --bold with fonts containing the displayed characters.")
    embed_html(rounds)
    render_gif(rounds, args.regular, args.bold)
    archive()
    for name in ("index.html", GIF_NAME, ZIP_NAME):
        print(f"{name}: {(HERE / name).stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
