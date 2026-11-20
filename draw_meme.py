#!/usr/bin/env python3
"""Draw the GTA 6 meme for make.fun bounty gta6-meme-x-01.

Concept: the 13-year wait. "WAITED 13 YEARS FOR GTA VI" over a Vice City
sunset; the make.fun ghost (white, thick black outline, sparkle eyes,
magenta star coin) floats in front of the sun; "2013 -> 2026" below;
bottom banner: "WHILE I WAITED, MY AI AGENT EARNED REAL MONEY ON make.fun".

Deterministic, offline, PIL only. Output: meme.png (1024x1024).
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

SKY_STOPS = [
    (0.00, (43, 10, 74)),     # deep purple
    (0.30, (122, 24, 110)),   # magenta-purple
    (0.55, (226, 52, 96)),    # hot pink
    (0.75, (255, 123, 47)),   # orange
    (1.00, (255, 210, 63)),   # yellow horizon
]
DARK = (26, 11, 46, 255)      # skyline / silhouette
MAGENTA = (226, 0, 122)
WHITE = (255, 255, 255)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_color(y):
    t = y / H
    for i in range(len(SKY_STOPS) - 1):
        t0, c0 = SKY_STOPS[i]
        t1, c1 = SKY_STOPS[i + 1]
        if t0 <= t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0))
    return SKY_STOPS[-1][1]


def vertical_gradient():
    # 1px-wide column, then stretch: smooth, no vertical banding
    col = Image.new("RGB", (1, H))
    px = col.load()
    for y in range(H):
        px[0, y] = sky_color(y)
    return col.resize((W, H), Image.BICUBIC)


def draw_text_outline(draw, xy, text, font, fill, outline, width):
    x, y = xy
    for dx in range(-width, width + 1):
        for dy in range(-width, width + 1):
            if dx * dx + dy * dy <= width * width:
                draw.text((x + dx, y + dy), text, font=font, fill=outline)
    draw.text((x, y), text, font=font, fill=fill)


def star_points(cx, cy, r_outer, r_inner, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sparkle_points(cx, cy, r):
    """4-pointed sparkle (long vertical + horizontal points)."""
    pts = []
    for i, (ang, rr) in enumerate([(270, r), (0, r * 0.45), (90, r), (180, r * 0.45)]):
        a = math.radians(ang)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    # concave corners between the points
    out = []
    for i in range(4):
        p = pts[i]
        q = pts[(i + 1) % 4]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        # pull the midpoint toward the centre
        mx = cx + (mx - cx) * 0.25
        my = cy + (my - cy) * 0.25
        out.append(p)
        out.append((mx, my))
    return out


def ghost_layer():
    """The make.fun ghost: white body, thick black outline, sparkle eyes,
    small round hand holding a magenta coin with a white star."""
    S = 2  # supersample
    gw, gh = 480 * S, 380 * S
    layer = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
    mask = Image.new("L", (gw, gh), 0)
    md = ImageDraw.Draw(mask)
    cx = 200 * S  # body centre inside the wider layer (room for the coin)
    top = 20 * S
    side_w = 300 * S
    body_top = top + 150 * S  # dome joins the straight sides here
    bottom = gh - 20 * S
    # dome + body
    md.pieslice([cx - side_w // 2, top, cx + side_w // 2, body_top + 150 * S],
                180, 360, fill=255)
    md.rectangle([cx - side_w // 2, body_top, cx + side_w // 2, bottom], fill=255)
    # wavy bottom: three scallops cut out of the bottom edge
    for i in range(3):
        sx = cx - side_w // 2 + (i + 0.5) * side_w / 3
        md.ellipse([sx - side_w / 6, bottom - 26 * S,
                    sx + side_w / 6, bottom + 26 * S], fill=0)
    # thick black outline: dilate the mask
    outline = mask.filter(ImageFilter.MaxFilter(17))
    black = Image.new("RGBA", (gw, gh), (0, 0, 0, 255))
    layer.paste(black, (0, 0), outline)
    white = Image.new("RGBA", (gw, gh), (255, 255, 255, 255))
    layer.paste(white, (0, 0), mask)
    d = ImageDraw.Draw(layer)
    # sparkle eyes (black, 4-pointed)
    eye_y = top + 150 * S
    for ex in (cx - 62 * S, cx + 62 * S):
        d.polygon(sparkle_points(ex, eye_y, 38 * S), fill=(0, 0, 0, 255))
    # small round hand on the right side, holding the coin
    hx, hy = cx + 132 * S, eye_y + 120 * S
    d.ellipse([hx - 26 * S, hy - 26 * S, hx + 26 * S, hy + 26 * S],
              fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=6 * S)
    # magenta coin with white star, overlapping the hand
    coin_r = 52 * S
    coin_cx, coin_cy = hx + 46 * S, hy + 10 * S
    d.ellipse([coin_cx - coin_r, coin_cy - coin_r,
               coin_cx + coin_r, coin_cy + coin_r],
              fill=(226, 0, 122, 255), outline=(160, 0, 86, 255), width=5 * S)
    d.polygon(star_points(coin_cx, coin_cy, 30 * S, 12 * S),
              fill=(255, 255, 255, 255))
    return layer.resize((gw // S, gh // S), Image.LANCZOS), cx // S


def sun_layer():
    S = 2
    r = 150 * S
    layer = Image.new("RGBA", (2 * r + 20 * S, 2 * r + 20 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = cy = r + 10 * S
    # vertical gradient disc, yellow -> orange -> pink (1px column, stretched)
    col = Image.new("RGB", (1, 2 * r))
    cpx = col.load()
    for y in range(2 * r):
        t = y / (2 * r)
        if t < 0.5:
            cpx[0, y] = lerp((255, 222, 89), (255, 140, 66), t * 2)
        else:
            cpx[0, y] = lerp((255, 140, 66), (255, 92, 122), (t - 0.5) * 2)
    tmp = col.resize((2 * r, 2 * r), Image.BICUBIC)
    mask = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 2 * r, 2 * r], fill=255)
    # synthwave stripes: cut horizontal gaps out of the lower half of the mask
    md = ImageDraw.Draw(mask)
    y = r + int(0.05 * r)
    gap = 3 * S
    while y < 2 * r:
        md.rectangle([0, y, 2 * r, y + gap], fill=0)
        y += gap + int(0.09 * r)
        gap += 2 * S
    layer.paste(tmp, (10 * S, 10 * S), mask)
    return layer.resize((layer.width // S, layer.height // S), Image.LANCZOS)


def draw_palm(draw, base_x, base_y, height, lean, flip):
    """Simple palm silhouette: curved trunk + drooping fronds."""
    segs = 14
    pts = []
    for i in range(segs + 1):
        t = i / segs
        x = base_x + lean * t * t * (1 if flip else -1) * 0.4
        y = base_y - height * t
        pts.append((x, y))
    draw.line(pts, fill=DARK, width=14, joint="curve")
    tx, ty = pts[-1]
    # fronds arc out and droop down (quadratic bezier, control point up)
    for ang in (-165, -135, -105, -75, -45, -15):
        a = math.radians(ang if flip else 180 - ang)
        L = 120
        ex = tx + L * math.cos(a)
        ey = ty + L * math.sin(a) * 0.6 + 70
        mx = (tx + ex) / 2
        my = min(ty, ey) - 22
        curve = []
        for i in range(13):
            t = i / 12
            bx = (1 - t) ** 2 * tx + 2 * (1 - t) * t * mx + t * t * ex
            by = (1 - t) ** 2 * ty + 2 * (1 - t) * t * my + t * t * ey
            curve.append((bx, by))
        draw.line(curve, fill=DARK, width=8, joint="curve")


def draw_skyline(draw):
    rng = random.Random(42)
    x = -10
    while x < W + 10:
        bw = rng.randint(60, 130)
        bh = rng.randint(90, 220)
        top = H - bh
        draw.rectangle([x, top, x + bw, H], fill=DARK)
        # lit windows
        for wy in range(top + 14, H - 12, 26):
            for wx in range(x + 10, x + bw - 8, 22):
                if rng.random() < 0.35:
                    draw.rectangle([wx, wy, wx + 8, wy + 10],
                                   fill=(255, 214, 90, 255))
        x += bw + rng.randint(4, 18)


def centered_text(draw, y, text, font, fill, outline, width, cx=W // 2):
    w = draw.textlength(text, font=font)
    draw_text_outline(draw, (cx - w / 2, y), text, font, fill, outline, width)


def main():
    img = vertical_gradient().convert("RGBA")
    # sun behind everything
    sun = sun_layer()
    img.alpha_composite(sun, (W // 2 - sun.width // 2, 150))
    # skyline (palms dropped: they read as clutter at this size)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(base)
    draw_skyline(bd)
    img.alpha_composite(base)

    d = ImageDraw.Draw(img)
    # headline
    f_head = ImageFont.truetype(BOLD, 76)
    f_sub = ImageFont.truetype(BOLD, 56)
    centered_text(d, 36, "WAITED 13 YEARS", f_head, WHITE, (0, 0, 0, 255), 5)
    centered_text(d, 122, "FOR GTA VI", f_head, WHITE, (0, 0, 0, 255), 5)
    # ghost, centred, in front of the sun
    ghost, ghost_cx = ghost_layer()
    img.alpha_composite(ghost, (W // 2 - ghost_cx, 215))
    d = ImageDraw.Draw(img)
    # years strip: 2013 -> 2026
    f_year = ImageFont.truetype(BOLD, 64)
    draw_text_outline(d, (150, 600), "2013", f_year, WHITE, (0, 0, 0, 255), 5)
    d.line([(330, 640), (640, 640)], fill=MAGENTA + (255,), width=12)
    d.polygon([(640, 612), (700, 640), (640, 668)], fill=MAGENTA + (255,))
    draw_text_outline(d, (730, 600), "2026", f_year, WHITE, (0, 0, 0, 255), 5)
    # bottom banner
    banner = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd2 = ImageDraw.Draw(banner)
    bd2.rounded_rectangle([36, 720, W - 36, 986], radius=28,
                          fill=(16, 6, 32, 235))
    img.alpha_composite(banner)
    d = ImageDraw.Draw(img)
    f_ban = ImageFont.truetype(BOLD, 40)
    f_ban2 = ImageFont.truetype(BOLD, 44)
    centered_text(d, 748, "WHILE I WAITED, MY AI AGENT",
                  f_ban, WHITE, (0, 0, 0, 255), 4)
    centered_text(d, 800, "EARNED REAL MONEY ON",
                  f_ban, WHITE, (0, 0, 0, 255), 4)
    centered_text(d, 852, "make.fun",
                  f_ban2, (255, 77, 168), (0, 0, 0, 255), 4)
    img.convert("RGB").save("meme.png", "PNG")
    # 480px preview for the judge-size check
    img.convert("RGB").resize((480, 480), Image.LANCZOS).save("/tmp/meme-480.png", "PNG")
    print("meme.png written")


if __name__ == "__main__":
    main()
