#!/usr/bin/env python3
"""Slot 1 - "The World in One Day" - news-image-20261122.

Renders entry.png (1024x1024 broadsheet) from 36 verified 22 Nov 2026
stories. Stdlib + PIL only, no network, fully deterministic: the same
input bytes always produce the same output bytes (no randomness, no
clock, no environment input). Art is drawn with PIL primitives only;
all text is real text rendered with DejaVu fonts (nothing garbled).
See AUDIT.md for the story list and sources.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (25, 25, 25)
RED = (163, 22, 33)
DARKRED = (120, 16, 24)
NAVY = (30, 58, 95)
GREY = (90, 88, 80)
LIGHT = (233, 228, 214)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)             # noqa: E731
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)        # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)               # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, leading, color=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=color)
    return y + len(lines) * leading


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def stars(draw, box, pts, color=(255, 255, 220)):
    x0, y0, x1, y1 = box
    for fx, fy, r in pts:
        cx, cy = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def tag(draw, x, y, text, fnt=None, bg=RED, fg=(255, 255, 255)):
    fnt = fnt or F_SANS_B(10)
    w = draw.textlength(text, font=fnt) + 10
    h = fnt.size + 7
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.text((x + 5, y + 3), text, font=fnt, fill=fg)
    return w


def chip(draw, x, y, text):
    """Small black caption chip, bottom-left of an artwork."""
    fnt = F_SANS_B(10)
    w = draw.textlength(text, font=fnt) + 12
    draw.rectangle([x, y, x + w, y + 18], fill=(15, 15, 15))
    draw.text((x + 6, y + 3), text, font=fnt, fill=(255, 255, 255))


# ---------------------------------------------------------------- art: heroes

def art_cop31(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (24, 44, 66), (52, 84, 110))
    # wall clock, stopped at overtime
    cx, cy, r = x1 - 52, y0 + 46, 30
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 240, 225),
                 outline=(20, 20, 20), width=3)
    for a in range(12):
        import math
        ang = math.pi * 2 * a / 12
        x2, y2 = cx + 24 * math.sin(ang), cy - 24 * math.cos(ang)
        draw.ellipse([x2 - 2, y2 - 2, x2 + 2, y2 + 2], fill=(20, 20, 20))
    draw.line([cx, cy, cx + 16, cy - 12], fill=(163, 22, 33), width=3)
    draw.line([cx, cy, cx - 4, cy - 20], fill=(20, 20, 20), width=3)
    # rows of delegate desks
    for row, yy in enumerate([y0 + 72, y0 + 96, y0 + 116]):
        desks = 6 if row != 1 else 5
        for i in range(desks):
            dx = x0 + 16 + i * 52
            draw.rectangle([dx, yy, dx + 40, yy + 10], fill=(120, 84, 50))
            draw.ellipse([dx + 13, yy - 12, dx + 27, yy + 2], fill=(210, 180, 140))
            draw.rectangle([dx + 8, yy - 2, dx + 32, yy + 4], fill=(40, 60, 80))
    # empty chairs, a few delegates walking out
    for i, dx in enumerate([x0 + 30, x0 + 90, x0 + 210]):
        draw.rectangle([dx, y1 - 34, dx + 26, y1 - 8], fill=(70, 50, 30))
        draw.rectangle([dx + 4, y1 - 52, dx + 22, y1 - 32], fill=(70, 50, 30))
    # red banner, no deal
    draw.rectangle([x0, y1 - 8, x1, y1], fill=RED)


def art_sparta(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (10, 18, 38), (30, 52, 84))
    stars(draw, box, [(0.08, 0.12, 1.5), (0.22, 0.06, 1), (0.4, 0.15, 1.5),
                      (0.6, 0.08, 1), (0.78, 0.18, 1.5), (0.92, 0.07, 1),
                      (0.5, 0.22, 1), (0.3, 0.25, 1)])
    # moon
    draw.ellipse([x1 - 62, y0 + 12, x1 - 30, y0 + 44], fill=(240, 235, 210))
    # sea
    sea_y = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, sea_y, x1, y1], fill=(16, 38, 66))
    for i in range(5):
        yy = sea_y + 10 + i * 9
        draw.line([(x0 + 8 + i * 7, yy), (x0 + 70 + i * 11, yy)],
                  fill=(90, 130, 170), width=2)
    # ship hull + superstructure, listing slightly
    hx0, hy = x0 + 42, sea_y - 6
    draw.polygon([(hx0, hy), (hx0 + 210, hy), (hx0 + 196, hy + 26),
                  (hx0 + 14, hy + 26)], fill=(38, 38, 42))
    draw.rectangle([hx0 + 30, hy - 22, hx0 + 90, hy], fill=(52, 52, 58))
    draw.rectangle([hx0 + 100, hy - 14, hx0 + 150, hy], fill=(70, 70, 76))
    draw.rectangle([hx0 + 120, hy - 30, hx0 + 128, hy - 14], fill=(52, 52, 58))
    # containers
    draw.rectangle([hx0 + 155, hy - 12, hx0 + 175, hy], fill=(200, 60, 50))
    # flames
    for fx, fy, s in [(hx0 + 60, hy - 22, 16), (hx0 + 88, hy - 26, 20),
                      (hx0 + 118, hy - 20, 14)]:
        draw.polygon([(fx - s, fy), (fx, fy - s * 1.7), (fx + s, fy),
                      (fx + s * 0.5, fy - s * 0.6), (fx - s * 0.5, fy - s * 0.6)],
                     fill=(255, 140, 30))
        draw.polygon([(fx - s * 0.55, fy), (fx, fy - s), (fx + s * 0.55, fy)],
                     fill=(255, 210, 80))
    # smoke
    for sx, sy, sr in [(hx0 + 70, hy - 48, 10), (hx0 + 95, hy - 58, 12),
                       (hx0 + 120, hy - 66, 9)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 125))
    # two drones
    for dx, dy in [(x0 + 200, y0 + 26), (x0 + 235, y0 + 44)]:
        draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 255, 255))
        draw.line([dx - 8, dy, dx + 8, dy], fill=(255, 255, 255), width=1)
        draw.line([dx, dy - 8, dx, dy + 8], fill=(255, 255, 255), width=1)


def art_hormuz(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (250, 200, 120), (235, 160, 80))
    # sun low over the strait
    draw.ellipse([x0 + 120, y0 + 12, x0 + 168, y0 + 60], fill=(255, 236, 180))
    # land masses left and right
    draw.polygon([(x0, y0), (x0 + 62, y0), (x0 + 78, y0 + 60), (x0 + 58, y1),
                  (x0, y1)], fill=(196, 160, 110))
    draw.polygon([(x1, y0), (x1 - 58, y0), (x1 - 74, y0 + 60), (x1 - 56, y1),
                  (x1, y1)], fill=(188, 150, 100))
    # strait water
    draw.polygon([(x0 + 62, y0), (x1 - 58, y0), (x1 - 74, y0 + 60),
                  (x1 - 56, y1), (x0 + 58, y1), (x0 + 78, y0 + 60)],
                 fill=(36, 90, 140))
    for i in range(4):
        yy = y0 + 66 + i * 14
        draw.line([(x0 + 84, yy), (x1 - 84, yy)], fill=(120, 170, 210), width=2)
    # tanker crossing the strait
    tx, ty = x0 + 108, y0 + 84
    draw.polygon([(tx, ty), (tx + 96, ty), (tx + 86, ty + 16), (tx + 10, ty + 16)],
                 fill=(40, 40, 44))
    draw.rectangle([tx + 14, ty - 12, tx + 34, ty], fill=(60, 60, 66))
    draw.rectangle([tx + 60, ty - 8, tx + 80, ty], fill=(200, 60, 50))
    # drones above, one with a trail
    for dx, dy in [(x0 + 190, y0 + 30), (x0 + 225, y0 + 52)]:
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(30, 30, 30))
        draw.line([dx - 10, dy, dx + 10, dy], fill=(30, 30, 30), width=2)
        draw.line([dx, dy - 10, dx, dy + 10], fill=(30, 30, 30), width=2)
    draw.line([(x0 + 190, y0 + 30), (x0 + 150, y0 + 70)], fill=(90, 90, 90),
              width=1)
    # radar arcs from a small patrol boat
    bx, by = x0 + 250, y1 - 26
    draw.polygon([(bx - 16, by), (bx + 16, by), (bx + 8, by - 10), (bx - 8, by - 10)],
                 fill=(50, 50, 55))
    for r in (10, 18, 26):
        draw.arc([bx - r, by - 34 - r, bx + r, by - 34 + r], 200, 340,
                 fill=(255, 255, 255), width=2)


# ---------------------------------------------------------------- art: panels

def _panel_bg(draw, box, top, bottom):
    vgrad(draw, box, top, bottom)


def art_sinaloa(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (18, 22, 44), (44, 34, 60))
    stars(draw, box, [(0.1, 0.15, 1), (0.5, 0.1, 1), (0.85, 0.2, 1)])
    # buildings
    for bx, bw, bh in [(0, 34, 26), (40, 28, 36), (72, 40, 22), (118, 30, 30),
                       (152, 36, 24)]:
        draw.rectangle([x0 + bx, y1 - bh - 8, x0 + bx + bw, y1 - 8],
                       fill=(24, 26, 40))
        for wy in range(2):
            draw.rectangle([x0 + bx + 6, y1 - bh + 2 + wy * 12, x0 + bx + 12,
                            y1 - bh + 8 + wy * 12], fill=(255, 200, 90))
    # burning truck
    tx, ty = x0 + 66, y1 - 30
    draw.rectangle([tx, ty, tx + 58, ty + 14], fill=(150, 60, 30))
    draw.rectangle([tx + 40, ty - 12, tx + 58, ty], fill=(120, 50, 30))
    draw.ellipse([tx + 8, ty + 12, tx + 20, ty + 24], fill=(15, 15, 15))
    draw.ellipse([tx + 42, ty + 12, tx + 54, ty + 24], fill=(15, 15, 15))
    for fx, s in [(tx + 18, 12), (tx + 38, 15)]:
        draw.polygon([(fx - s, ty), (fx, ty - s * 1.6), (fx + s, ty)],
                     fill=(255, 140, 30))


def art_estonia(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (200, 214, 226), (168, 188, 205))
    # road
    draw.polygon([(x0, y1), (x0 + 60, y0 + 18), (x0 + 130, y0 + 18), (x1, y1)],
                 fill=(90, 90, 95))
    draw.line([(x0 + 96, y0 + 18), (x0 + 60, y1)], fill=(240, 240, 240), width=2)
    # border fence / barrier
    for i in range(9):
        bx = x0 + 12 + i * 20
        draw.line([(bx, y0 + 22), (bx, y0 + 52)], fill=(40, 40, 44), width=3)
    draw.rectangle([x0 + 8, y0 + 20, x1 - 8, y0 + 26], fill=(40, 40, 44))
    # striped barrier arm
    draw.rectangle([x0 + 20, y0 + 56, x1 - 20, y0 + 64], fill=(255, 255, 255),
                   outline=(163, 22, 33), width=2)
    for i in range(4):
        draw.rectangle([x0 + 28 + i * 40, y0 + 56, x0 + 44 + i * 40, y0 + 64],
                       fill=RED)
    # Estonian flag
    fx, fy = x0 + 130, y0 + 8
    for j, c in enumerate([(0, 114, 206), (20, 20, 20), (255, 255, 255)]):
        draw.rectangle([fx, fy + j * 6, fx + 34, fy + j * 6 + 6], fill=c)


def art_bolsonaro(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (232, 240, 244), (200, 216, 226))
    # wall + red cross sign
    draw.rectangle([x0 + 12, y0 + 8, x0 + 44, y0 + 40], fill=(255, 255, 255),
                   outline=(163, 22, 33), width=2)
    draw.rectangle([x0 + 24, y0 + 14, x0 + 32, y0 + 34], fill=RED)
    draw.rectangle([x0 + 18, y0 + 20, x0 + 38, y0 + 28], fill=RED)
    # bed
    draw.rectangle([x0 + 60, y1 - 30, x1 - 12, y1 - 22], fill=(70, 110, 150))
    draw.rectangle([x0 + 60, y1 - 22, x1 - 12, y1 - 14], fill=(240, 240, 235))
    draw.rectangle([x0 + 60, y1 - 38, x0 + 76, y1 - 22], fill=(200, 210, 220))
    draw.ellipse([x0 + 78, y1 - 36, x0 + 96, y1 - 22], fill=(230, 200, 170))
    draw.rectangle([x0 + 96, y1 - 30, x1 - 30, y1 - 22], fill=(180, 200, 220))
    # drip stand
    draw.line([(x1 - 24, y0 + 10), (x1 - 24, y1 - 22)], fill=(60, 60, 60), width=2)
    draw.rectangle([x1 - 32, y0 + 10, x1 - 16, y0 + 22], fill=(200, 220, 230),
                   outline=(60, 60, 60))


def art_un(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (214, 228, 240), (170, 195, 220))
    # globe
    cx, cy, r = x0 + 96, y0 + 32, 24
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 140, 190),
                 outline=(30, 58, 95), width=2)
    draw.ellipse([cx - 12, cy - r, cx + 12, cy + r], outline=(255, 255, 255),
                 width=1)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=1)
    draw.arc([cx - r, cy - 12, cx + r, cy + 12], 0, 360, fill=(255, 255, 255))
    # flag poles
    for fx in (x0 + 18, x0 + 40, x0 + 150, x0 + 172):
        draw.line([(fx, y0 + 14), (fx, y1 - 10)], fill=(60, 60, 60), width=2)
        draw.rectangle([fx, y0 + 14, fx + 16, y0 + 24],
                       fill=(0, 114, 206) if fx < x0 + 100 else (163, 22, 33))
    # steps
    for i in range(3):
        draw.rectangle([x0 + 60, y1 - 12 - i * 5, x0 + 132, y1 - 7 - i * 5],
                       fill=(120, 130, 140))


def art_manila(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (250, 190, 120), (235, 140, 70))
    draw.ellipse([x0 + 140, y0 + 8, x0 + 168, y0 + 36], fill=(255, 240, 200))
    # coastline
    draw.polygon([(x0, y1), (x0, y1 - 18), (x0 + 60, y1 - 26), (x0 + 120, y1 - 14),
                  (x1, y1 - 20), (x1, y1)], fill=(90, 140, 90))
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(36, 90, 140))
    # jet turning away
    jx, jy = x0 + 70, y0 + 26
    draw.polygon([(jx, jy), (jx + 46, jy + 6), (jx, jy + 12)], fill=(40, 40, 44))
    draw.polygon([(jx + 14, jy + 2), (jx + 26, jy - 12), (jx + 30, jy + 4)],
                 fill=(40, 40, 44))
    draw.polygon([(jx + 14, jy + 10), (jx + 26, jy + 22), (jx + 30, jy + 8)],
                 fill=(40, 40, 44))
    # dashed turn-back path
    for i in range(6):
        px = jx + 52 + i * 12
        py = jy + 8 + i * 3
        draw.ellipse([px, py, px + 4, py + 4], fill=(255, 255, 255))


def art_gaza(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (60, 50, 70), (30, 26, 40))
    draw.ellipse([x0 + 150, y0 + 8, x0 + 176, y0 + 34], fill=(240, 220, 180))
    # skyline
    for bx, bw, bh in [(0, 30, 30), (34, 24, 42), (62, 34, 26), (100, 28, 38),
                       (132, 30, 24), (166, 24, 32)]:
        draw.rectangle([x0 + bx, y1 - bh - 6, x0 + bx + bw, y1 - 6],
                       fill=(16, 14, 22))
        for wy in range(2):
            draw.rectangle([x0 + bx + 5, y1 - bh + 3 + wy * 12, x0 + bx + 11,
                            y1 - bh + 9 + wy * 12], fill=(255, 200, 90))
    # smoke plume
    for sx, sy, sr in [(x0 + 78, y0 + 16, 9), (x0 + 88, y0 + 8, 11),
                       (x0 + 100, y0 + 4, 8)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(140, 135, 130))
    draw.polygon([(x0 + 74, y0 + 26), (x0 + 82, y0 + 6), (x0 + 90, y0 + 26)],
                 fill=(255, 140, 30))


def art_bridge(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (200, 225, 240), (160, 195, 220))
    draw.ellipse([x0 + 140, y0 + 6, x0 + 166, y0 + 32], fill=(255, 240, 190))
    # river
    draw.rectangle([x0, y1 - 16, x1, y1], fill=(60, 120, 170))
    for i in range(4):
        draw.line([(x0 + 10 + i * 20, y1 - 8), (x0 + 40 + i * 20, y1 - 8)],
                  fill=(150, 200, 230), width=2)
    # bridge deck + arch + towers
    draw.rectangle([x0 + 6, y1 - 26, x1 - 6, y1 - 20], fill=(120, 70, 40))
    draw.arc([x0 + 30, y1 - 52, x1 - 30, y1 - 8], 180, 360, fill=(120, 70, 40),
             width=4)
    for tx in (x0 + 40, x0 + 136):
        draw.rectangle([tx, y0 + 18, tx + 8, y1 - 20], fill=(140, 80, 45))
    # cars
    for cx, c in [(x0 + 60, (200, 60, 50)), (x0 + 110, (40, 90, 160))]:
        draw.rectangle([cx, y1 - 34, cx + 18, y1 - 26], fill=c)


def art_airlines(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (210, 228, 242), (170, 200, 225))
    # clouds
    for cx, cy in [(30, 14), (120, 10), (160, 44)]:
        draw.ellipse([x0 + cx, y0 + cy, x0 + cx + 34, y0 + cy + 12],
                     fill=(255, 255, 255))
    # plane
    px, py = x0 + 46, y0 + 26
    draw.polygon([(px, py), (px + 62, py + 6), (px, py + 12)], fill=(40, 60, 90))
    draw.polygon([(px + 22, py + 2), (px + 36, py - 12), (px + 40, py + 4)],
                 fill=(40, 60, 90))
    draw.polygon([(px + 22, py + 10), (px + 36, py + 22), (px + 40, py + 8)],
                 fill=(40, 60, 90))
    # warning triangle
    tx, ty = x0 + 138, y0 + 22
    draw.polygon([(tx, ty), (tx + 34, ty), (tx + 17, ty + 30)], fill=(255, 200, 0),
                 outline=(20, 20, 20), width=2)
    draw.rectangle([tx + 15, ty + 8, tx + 19, ty + 20], fill=(20, 20, 20))
    draw.ellipse([tx + 14, ty + 23, tx + 20, ty + 29], fill=(20, 20, 20))


def art_unchief(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (200, 216, 232), (160, 186, 210))
    # globe
    cx, cy, r = x0 + 52, y0 + 30, 22
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 140, 190),
                 outline=(30, 58, 95), width=2)
    draw.ellipse([cx - 11, cy - r, cx + 11, cy + r], outline=(255, 255, 255))
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=1)
    # empty chair
    draw.rectangle([x0 + 118, y1 - 34, x0 + 164, y1 - 28], fill=(120, 80, 40))
    draw.rectangle([x0 + 118, y1 - 56, x0 + 126, y1 - 28], fill=(120, 80, 40))
    draw.rectangle([x0 + 122, y1 - 28, x0 + 126, y1 - 10], fill=(90, 60, 30))
    draw.rectangle([x0 + 156, y1 - 28, x0 + 160, y1 - 10], fill=(90, 60, 30))
    # question mark
    draw.text((x0 + 132, y0 + 8), "?", font=F_SANS_B(22), fill=RED)


def art_basra(draw, box):
    x0, y0, x1, y1 = box
    _panel_bg(draw, box, (40, 36, 44), (20, 18, 24))
    # cooling towers
    for bx, bw in [(14, 34), (56, 40), (104, 34)]:
        draw.polygon([(x0 + bx, y1 - 8), (x0 + bx + 4, y0 + 26),
                      (x0 + bx + bw - 4, y0 + 26), (x0 + bx + bw, y1 - 8)],
                     fill=(90, 88, 96))
        draw.ellipse([x0 + bx + 2, y0 + 20, x0 + bx + bw - 2, y0 + 32],
                     fill=(60, 58, 64))
    # flames at base of one tower
    for fx, s in [(x0 + 120, 12), (x0 + 136, 15)]:
        draw.polygon([(fx - s, y1 - 8), (fx, y1 - 8 - s * 1.8), (fx + s, y1 - 8)],
                     fill=(255, 140, 30))
    # smoke
    for sx, sy, sr in [(x0 + 128, y0 + 12, 9), (x0 + 142, y0 + 6, 11)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(130, 128, 130))
    # sparks
    for sx, sy in [(x0 + 170, y0 + 20), (x0 + 178, y0 + 34), (x0 + 164, y0 + 40)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 200, 80))


# ---------------------------------------------------------------- world map

# Coarse continent outlines (lon, lat), equirectangular, stylised.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-110, 73), (-95, 80),
     (-85, 76), (-80, 73), (-70, 62), (-60, 55), (-55, 47), (-60, 44),
     (-70, 42), (-75, 35), (-81, 26), (-84, 30), (-90, 21), (-94, 17),
     (-97, 16), (-105, 20), (-112, 24), (-117, 32), (-124, 40), (-124, 49),
     (-132, 54), (-145, 60), (-158, 58), (-165, 60)],
    # South America
    [(-80, 10), (-72, 12), (-62, 9), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-54, -34), (-58, -38),
     (-62, -41), (-66, -47), (-69, -52), (-71, -54), (-74, -44), (-73, -32),
     (-71, -20), (-77, -12), (-81, -5), (-80, 2)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (2, 51),
     (5, 53), (8, 57), (10, 59), (12, 56), (18, 56), (21, 55), (24, 58),
     (28, 60), (30, 62), (30, 70), (40, 68), (44, 66), (48, 62), (44, 58),
     (40, 55), (38, 52), (35, 50), (33, 46), (30, 46), (28, 44), (24, 40),
     (23, 36), (19, 40), (15, 44), (12, 44), (8, 44), (3, 42), (0, 39),
     (-2, 37), (-6, 36)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (12, 34), (20, 32), (25, 32), (30, 31),
     (32, 31), (34, 28), (37, 22), (39, 18), (43, 12), (48, 11), (51, 11),
     (51, 2), (46, -2), (41, -6), (39, -12), (36, -18), (35, -22), (33, -26),
     (32, -29), (28, -33), (20, -35), (17, -32), (15, -27), (13, -22),
     (12, -18), (13, -12), (9, -1), (9, 4), (6, 4), (2, 6), (-4, 5),
     (-8, 5), (-13, 8), (-16, 12), (-17, 15), (-16, 20), (-15, 24),
     (-13, 28), (-10, 31)],
    # Asia
    [(30, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 76), (120, 74), (130, 72), (140, 72), (150, 70),
     (160, 70), (170, 67), (178, 65), (173, 64), (170, 60), (162, 56),
     (158, 51), (156, 51), (150, 47), (142, 45), (140, 40), (138, 37),
     (135, 34), (131, 33), (129, 31), (127, 35), (126, 38), (122, 40),
     (121, 36), (120, 32), (121, 28), (118, 25), (113, 22), (109, 20),
     (108, 18), (106, 15), (105, 10), (103, 8), (100, 8), (98, 12),
     (98, 16), (97, 16), (94, 18), (92, 21), (91, 22), (89, 22), (87, 21),
     (86, 20), (83, 18), (80, 15), (80, 13), (77, 8), (76, 10), (75, 12),
     (73, 16), (72, 20), (70, 22), (68, 23), (66, 25), (63, 25), (61, 25),
     (58, 26), (57, 27), (55, 26), (53, 27), (51, 29), (50, 29), (48, 30),
     (47, 30), (44, 29), (43, 26), (42, 20), (41, 16), (39, 15), (38, 18),
     (36, 22), (35, 28), (34, 29), (36, 36), (33, 36), (30, 36), (27, 37),
     (26, 38), (27, 40), (30, 41), (33, 42), (36, 44), (39, 46), (40, 48),
     (42, 52), (43, 55), (44, 58), (46, 62), (44, 66), (40, 68)],
    # Australia
    [(113, -22), (114, -28), (115, -32), (118, -35), (124, -33), (129, -32),
     (132, -32), (136, -35), (138, -35), (140, -38), (144, -38), (147, -39),
     (150, -37), (153, -32), (153, -27), (151, -24), (150, -22), (147, -19),
     (146, -19), (142, -15), (142, -11), (141, -13), (137, -12), (135, -12),
     (132, -12), (130, -13), (126, -14), (124, -15), (122, -17), (120, -19),
     (117, -20), (114, -22)],
    # SE Asia islands + New Guinea
    [(95, 5), (98, 4), (100, 0), (103, -2), (106, -6), (110, -7), (114, -8),
     (118, -9), (120, -10), (123, -10), (126, -9), (129, -6), (131, -4),
     (134, -4), (137, -3), (140, -4), (143, -6), (146, -7), (147, -6),
     (146, -8), (142, -8), (140, -8), (137, -2), (135, 0), (132, -1),
     (130, -1), (128, 0), (126, 1), (123, 1), (120, 0), (117, -1), (114, -2),
     (111, -3), (108, -3), (105, -1), (102, 1), (100, 3), (97, 5)],
    # New Zealand
    [(167, -45), (168, -44), (171, -42), (174, -41), (176, -38), (178, -38),
     (175, -40), (173, -41), (171, -43), (168, -46), (167, -45)],
]

# Story number -> (lon, lat) for the map dots.
DOTS = {
    1: (30.7, 36.9), 2: (27.0, 60.0), 3: (56.5, 26.5), 4: (-108.5, 25.5),
    5: (28.2, 59.4), 6: (-47.9, -15.8), 7: (2.35, 48.85), 8: (121.0, 14.6),
    9: (34.5, 31.5), 10: (85.1, 25.6), 11: (-77.0, 38.9), 12: (-74.0, 40.7),
    13: (47.8, 30.5),
}

# Dots that would collide are drawn offset, with a leader line to the
# true position: number -> (dx, dy) in pixels.
DOT_OFFSETS = {5: (13, -9), 9: (11, 7), 12: (13, -9), 13: (-13, 9)}


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(207, 227, 238))
    lon0, lon1, lat0, lat1 = -180.0, 180.0, 84.0, -58.0

    def proj(lon, lat):
        px = x0 + (lon - lon0) / (lon1 - lon0) * (x1 - x0)
        py = y0 + (lat0 - lat) / (lat0 - lat1) * (y1 - y0)
        return px, py

    for lon in range(-150, 181, 30):
        px, _ = proj(lon, 0)
        draw.line([(px, y0), (px, y1)], fill=(225, 238, 245), width=1)
    for lat in range(60, -59, -30):
        _, py = proj(0, lat)
        draw.line([(x0, py), (x1, py)], fill=(225, 238, 245), width=1)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=(232, 217, 168), outline=(138, 125, 90))
    fnt = F_SANS_B(8)
    for num, (lon, lat) in DOTS.items():
        px, py = proj(lon, lat)
        if num in DOT_OFFSETS:
            ox, oy = DOT_OFFSETS[num]
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
            draw.line([(px, py), (px + ox, py + oy)], fill=RED, width=1)
            px, py = px + ox, py + oy
        r = 7
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        tw = draw.textlength(str(num), font=fnt)
        draw.text((px - tw / 2, py - 5), str(num), font=fnt,
                  fill=(255, 255, 255))


# ---------------------------------------------------------------- content

HEROES = [
    dict(n=1, kicker="1 ANTALYA · CLIMATE", tag="COP31: NO DEAL",
         chip="Overtime · AP", art=art_cop31,
         head="COP31 still without a deal as talks run on",
         body="Talks suspended after a draft dropped all fossil-fuel "
              "references and the $120bn-a-year adaptation target. A third "
              "draft is due. (AP, Guardian)"),
    dict(n=2, kicker="2 GULF OF FINLAND · WAR", tag="SPARTA II",
         chip="Crew evacuated · Reuters", art=art_sparta,
         head="Russian ship ablaze in the Baltic after drone strike",
         body="Bound for Kaliningrad, the Sparta II caught fire after two "
              "drones hit it; all 16 crew were evacuated. Finland says "
              "Ukraine was likely behind it. (Reuters)"),
    dict(n=3, kicker="3 HORMUZ · CONFLICT", tag="HORMUZ: 2 DOWN",
         chip="Two 'downed' · Al Jazeera", art=art_hormuz,
         head="Iran says it downed two US drones over Hormuz",
         body="The IRGC claims an MQ-9 over the Strait and an MQ-1 over "
              "Qeshm — its 58th and 19th such downings. No Pentagon "
              "comment. (Al Jazeera)"),
]

PANELS = [
    dict(n=4, kicker="4 SINALOA · CARTELS", tag="CAPTURED", art=art_sinaloa,
         head="‘El Chapo Isidro’ captured; Sinaloa burns",
         body="FBI fugitive Meza Flores seized at Guasave; 11 killed in "
              "the violence. (AP)"),
    dict(n=5, kicker="5 TALLINN · SECURITY", tag="1 DEC", art=art_estonia,
         head="Estonia to shut its Russia border on 1 Dec",
         body="All five crossings shut after a sabotage bid; families rush "
              "to cross. (Reuters)"),
    dict(n=6, kicker="6 BRASÍLIA · HEALTH", tag="ICU", art=art_bolsonaro,
         head="Bolsonaro in intensive care in Brasília",
         body="The jailed ex-president was admitted with an acute bowel "
              "obstruction. (AP)"),
    dict(n=7, kicker="7 PARIS · DIPLOMACY", tag="UNSC", art=art_un,
         head="France seeks UN action over Myanmar ruling",
         body="Myanmar rejected the ICJ ruling; Paris wants the Security "
              "Council to act. (UN)"),
    dict(n=8, kicker="8 MANILA · SECURITY", tag="170 KM", art=art_manila,
         head="Chinese bomber turns back 170 km from Manila",
         body="A missile-carrying bomber flew at the capital, then turned "
              "away. (Reports)"),
    dict(n=9, kicker="9 GAZA · CEASEFIRE", tag="4 KILLED", art=art_gaza,
         head="Four killed in Gaza ceasefire violations",
         body="Four Palestinians killed and 14 injured across the Strip, "
              "QNA reports. (QNA)"),
    dict(n=10, kicker="10 PATNA · INDIA", tag="BRIDGE", art=art_bridge,
         head="Modi opens Nitish Setu bridge in Bihar",
         body="The Patna–Vaishali bridge opens; Akvan cancels 14 flights "
              "at Ranchi. (PTI)"),
    dict(n=11, kicker="11 WASHINGTON · SECURITY", tag="WARNING",
         art=art_airlines,
         head="US airlines warned of Thanksgiving terror threat",
         body="Carriers warned of a possible al-Qaeda attack before the "
              "holiday. (Reports)"),
    dict(n=12, kicker="12 NEW YORK · UNITED NATIONS", tag="DEADLOCK",
         art=art_unchief,
         head="US ‘open to’ a Western Hemisphere UN chief",
         body="The UN chief race is deadlocked; envoy Waltz signals US "
              "openness. (UN)"),
    dict(n=13, kicker="13 BASRA · DISASTER", tag="4 DEAD", art=art_basra,
         head="Four die in fire at Basra power plant",
         body="A blaze at an electricity facility also injures 35 in the "
              "city. (Reports)"),
]

ALSO = [
    "Somalia expels the UAE ambassador, recalls its envoy (Sat)",
    "~700,000 displaced by fighting in southern Ethiopia (Sat)",
    "At least 40 civilians killed in Cantine, DR Congo (Sat)",
    "Iran: Qeshm blasts were US munitions disposal, Tehran says",
    "Bahrain probes Patriot interceptor crash amid drone reports",
    "Tankers hit by unidentified projectiles off Oman (UKMTO)",
    "N. Gupta gets 19 years in the Pannun murder-plot case",
    "Sweden summons Russia's ambassador as tensions grow",
    "Hegseth tightens US security cooperation with Canada",
    "Bessent: no new limits needed on Nvidia chip sales to China",
    "Japan to train live-fire at Indian facilities, a first",
    "EU floats an online tax; draft budget $224bn below plan",
    "Spain to widen its bank tax to fund housing",
    "Thai students protest in Bangkok for education reform",
    "Ex-Italian police chief De Gennaro dies amid mafia probe",
    "Swedish Gripen 'could not detect' missile over Poland",
    "Melania Trump presses for more Russia-Ukraine ceasefires",
    "Oleshky ceasefire holds; Zelenskyy eyes G20 talks",
    "Macklemore gives a single's profits to Gaza recovery",
    "India face New Zealand in a windy Wellington Test",
    "Pat Cummins keeps Australia's Test captaincy",
    "Air India extends its Jeddah suspension to 24 Nov",
    "COP31 AI pledge fails to draw big US tech firms",
]

STATS = [
    ("0", "deals agreed\nat COP31"),
    ("16", "crew evacuated\nfrom Sparta II"),
    ("11", "killed in Sinaloa\nviolence"),
    ("2", "US drones the IRGC\nsays it downed"),
    ("5", "Estonia crossings\nto shut on 1 Dec"),
    ("700,000", "displaced in\nsouthern Ethiopia"),
]

REGIONS = [
    ("EUROPE", 11, (30, 79, 156)), ("AMERICAS", 8, (140, 47, 57)),
    ("ASIA", 5, (179, 84, 30)), ("MIDDLE EAST", 6, (122, 92, 0)),
    ("AFRICA", 3, (46, 125, 50)), ("OCEANIA", 2, (0, 105, 92)),
    ("WORLD", 1, (85, 85, 85)),
]


# ---------------------------------------------------------------- render

def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14
    x0, x1 = M, W - M

    # --- masthead eyebrow
    d.text((x0, 8), "THE WORLD IN ONE DAY", font=F_SANS_B(13), fill=RED)
    right = "36 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    d.text((x1 - d.textlength(right, font=F_SANS_B(10)), 11), right,
           font=F_SANS_B(10), fill=INK)
    d.line([(x0, 30), (x1, 30)], fill=INK, width=2)

    # --- headline + subhead
    head = "Sunday 22 November 2026"
    hf = F_SERIF_B(60)
    d.text(((W - d.textlength(head, font=hf)) / 2, 34), head, font=hf, fill=INK)
    sub = ("COP31 still without a deal  ·  Russian ship ablaze in the Baltic  ·  "
           "US drones ‘downed’ over Hormuz")
    sf = F_SERIF(15)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 104), sub, font=sf, fill=INK)
    d.line([(x0, 126), (x1, 126)], fill=INK, width=2)

    # --- stat strip
    y = 130
    cw = (x1 - x0) / 6
    for i, (num, cap) in enumerate(STATS):
        cx = x0 + i * cw
        nf = F_SERIF_B(24)
        d.text((cx + 8, y), num, font=nf, fill=INK)
        text_block(d, cx + 8, y + 28, cap, F_SANS(9), cw - 16, 10, GREY)
        if i:
            d.line([(cx, y + 2), (cx, y + 40)], fill=(200, 194, 178), width=1)
    d.line([(x0, 178), (x1, 178)], fill=INK, width=1)

    # --- region strip
    y = 182
    widths = {"EUROPE": 284, "AMERICAS": 206, "ASIA": 138, "MIDDLE EAST": 166,
              "AFRICA": 83, "OCEANIA": 66, "WORLD": 52}
    rx = x0
    for name, count, color in REGIONS:
        w = widths[name]
        d.rectangle([rx, y, rx + w - 1, y + 18], fill=color)
        label = "%s %d" % (name, count)
        lf = F_SANS_B(10)
        d.text((rx + (w - d.textlength(label, font=lf)) / 2, y + 3), label,
               font=lf, fill=(255, 255, 255))
        rx += w

    # --- heroes
    y = 204
    colw = (x1 - x0 - 20) / 3
    for i, h in enumerate(HEROES):
        hx = x0 + i * (colw + 10)
        art = (hx, y, hx + colw, y + 126)
        d.rectangle([art[0] - 1, art[1] - 1, art[2] + 1, art[3] + 1],
                    outline=INK, width=1)
        h["art"](d, art)
        tag(d, art[0] + 4, art[1] + 4, h["tag"])
        chip(d, art[0] + 4, art[3] - 22, h["chip"])
        ky = y + 132
        d.text((hx, ky), h["kicker"], font=F_SANS_B(10), fill=RED)
        text_block(d, hx, ky + 14, h["head"], F_SANS_B(16), colw, 19,
                   max_lines=2)
        text_block(d, hx, ky + 54, h["body"], F_SANS(11), colw, 14,
                   max_lines=3)
    # --- panels, two rows of five
    pw = (x1 - x0 - 4 * 8) / 5
    for row in range(2):
        py = 438 + row * 146
        for col in range(5):
            p = PANELS[row * 5 + col]
            px = x0 + col * (pw + 8)
            art = (px, py, px + pw, py + 62)
            d.rectangle([art[0] - 1, art[1] - 1, art[2] + 1, art[3] + 1],
                        outline=INK, width=1)
            p["art"](d, art)
            tag(d, art[0] + 3, art[1] + 3, p["tag"], fnt=F_SANS_B(9))
            ky = py + 66
            d.text((px, ky), p["kicker"], font=F_SANS_B(9), fill=RED)
            text_block(d, px, ky + 12, p["head"], F_SANS_B(12), pw, 15,
                       max_lines=2)
            text_block(d, px, ky + 44, p["body"], F_SANS(9), pw, 12,
                       max_lines=2)

    # --- bottom: map + ALSO list
    y = 734
    d.line([(x0, y), (x1, y)], fill=INK, width=2)
    d.text((x0, y + 5), "WHERE IT HAPPENED", font=F_SANS_B(12), fill=INK)
    d.text((x0 + 348, y + 5), "ALSO ON SUNDAY 22 NOVEMBER — 23 MORE STORIES",
           font=F_SANS_B(12), fill=INK)
    draw_map(d, (x0, y + 24, x0 + 330, y + 168))
    d.text((x0, y + 172),
           "Red numbers mark stories 1–13 on the map.",
           font=F_SANS(8), fill=GREY)
    # ALSO list, two columns
    ax = x0 + 348
    colw2 = (x1 - ax - 12) / 2
    af = F_SANS(10)
    for i, item in enumerate(ALSO):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        ix = ax + col * (colw2 + 12)
        iy = y + 24 + row * 14
        num = "%d" % (14 + i)
        d.text((ix, iy), num, font=F_SANS_B(10), fill=RED)
        text_block(d, ix + 22, iy, item, af, colw2 - 22, 13, max_lines=1)

    # --- by the clock
    y = 930
    d.line([(x0, y), (x1, y)], fill=INK, width=1)
    clock = ("BY THE CLOCK · UTC   Sat 07:35  Sparta II fire reported   "
             "Sat 12:08 CST  Mexico announces capture   "
             "01:23  France seeks UNSC action   "
             "01:36  US ‘open to’ a Western Hemisphere UN chief")
    text_block(d, x0, y + 4, clock, F_SANS(10), x1 - x0, 13, max_lines=1)

    # --- date check
    y = 952
    d.rectangle([x0, y, x1, y + 44], outline=RED, width=2)
    dc = ("DATE CHECK   Left out as other days’ news: the APEC trilateral in Shenzhen "
          "(Thu 19 Nov) · the Kyiv barrage and the missiles over Poland (Fri 20 Nov) · "
          "Wall Street’s correction (Fri 20 Nov) · the Denmark ‘assassination plot’ "
          "(Fri 20 Nov) · the Peru quake (Fri 20 Nov local) · the Anthropic IPO debut "
          "(Thu 19 Nov) · the GTA VI launch (Thu 19 Nov). Not yet happened, so not "
          "shown: any final COP31 text; the Las Vegas GP result.")
    text_block(d, x0 + 6, y + 4, dc, F_SANS(10), x1 - x0 - 12, 13, max_lines=3)

    # --- footer
    d.text((x0, 1004),
           "Every story here happened, or was first reported, on Sunday 22 November 2026. "
           "Officials’ counts are attributed.",
           font=F_SANS(9), fill=INK)
    foot_r = "Sources named beside each story · original drawings"
    d.text((x1 - d.textlength(foot_r, font=F_SANS(9)), 1004), foot_r,
           font=F_SANS(9), fill=GREY)

    img.save(path, "PNG")
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    render(out)
    data = open(out, "rb").read()
    print("wrote %s (%d bytes, sha256 %s)" %
          (out, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
