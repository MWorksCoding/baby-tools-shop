"""Flat illustrations for the seed products, drawn with Pillow (one drawing per item type)."""

from math import cos, radians, sin

from PIL import Image, ImageDraw

WIDTH, HEIGHT = 600, 460
SCALE = 4  # draw four times bigger, then shrink for smooth edges
INK = (70, 70, 88)
WHITE = (255, 255, 255)
GREY = (160, 162, 178)
WOOD = (225, 188, 140)
TEAT = (242, 204, 160)
ORANGE = (255, 165, 80)
RAINBOW = [(255, 145, 145), (255, 200, 120), (250, 228, 120), (150, 215, 150), (130, 190, 240), (190, 160, 230)]


def mix(color, other, amount):
    return tuple(round(a + (b - a) * amount) for a, b in zip(color, other))


def light(color, amount=0.45):
    return mix(color, WHITE, amount)


def dark(color, amount=0.2):
    return mix(color, (0, 0, 0), amount)


def ellipse_points(cx, cy, rx, ry, start, end, steps=36):
    return [
        (cx + rx * cos(radians(start + (end - start) * i / steps)), cy + ry * sin(radians(start + (end - start) * i / steps)))
        for i in range(steps + 1)
    ]


def star_points(cx, cy, outer, inner, spikes=5):
    return [
        (cx + r * cos(radians(-90 + i * 180 / spikes)), cy + r * sin(radians(-90 + i * 180 / spikes)))
        for i, r in enumerate([outer, inner] * spikes)
    ]


class Pen:
    """Draws on a 100 x 100 grid in the middle of the image, with a dark outline around every shape."""

    def __init__(self, image, color, stage):
        self.draw = ImageDraw.Draw(image)
        self.color = color  # main colour of the product
        self.stage = stage  # colour behind the product, used to cut holes
        self.unit = 3.6 * SCALE
        self.left = WIDTH * SCALE / 2 - 50 * self.unit
        self.top = HEIGHT * SCALE / 2 - 50 * self.unit
        self.stroke = round(1.3 * self.unit)

    def xy(self, *points):
        return [(self.left + x * self.unit, self.top + y * self.unit) for x, y in points]

    def box(self, x0, y0, x1, y1, grow=0):
        (a, b), (c, d) = self.xy((x0, y0), (x1, y1))
        return [a - grow, b - grow, c + grow, d + grow]

    def _ink(self, outline):
        return {"outline": INK, "width": self.stroke} if outline else {}

    def rect(self, x0, y0, x1, y1, fill, radius=0, outline=True):
        self.draw.rounded_rectangle(self.box(x0, y0, x1, y1), radius=radius * self.unit, fill=fill, **self._ink(outline))

    def ellipse(self, x0, y0, x1, y1, fill, outline=True):
        self.draw.ellipse(self.box(x0, y0, x1, y1), fill=fill, **self._ink(outline))

    def circle(self, x, y, r, fill, outline=True):
        self.ellipse(x - r, y - r, x + r, y + r, fill, outline)

    def poly(self, points, fill, outline=True):
        self.draw.polygon(self.xy(*points), fill=fill, **self._ink(outline))

    def chord(self, x0, y0, x1, y1, start, end, fill, outline=True):
        self.draw.chord(self.box(x0, y0, x1, y1), start, end, fill=fill, **self._ink(outline))

    def pieslice(self, x0, y0, x1, y1, start, end, fill, outline=True):
        self.draw.pieslice(self.box(x0, y0, x1, y1), start, end, fill=fill, **self._ink(outline))

    def line(self, points, width=0.8, fill=INK):
        self.draw.line(self.xy(*points), fill=fill, width=round(width * self.unit), joint="curve")

    def bar(self, points, width, fill):
        """A thick, outlined line with round ends, e.g. a stroller frame."""
        for color, w in ((INK, width * self.unit + 2 * self.stroke), (fill, width * self.unit)):
            pixels = self.xy(*points)
            self.draw.line(pixels, fill=color, width=round(w), joint="curve")
            for x, y in pixels:
                self.draw.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=color)

    def arc(self, x0, y0, x1, y1, start, end, width, fill):
        """A thick, outlined arc centred on the given ellipse."""
        w = width * self.unit
        self.draw.arc(self.box(x0, y0, x1, y1, w / 2 + self.stroke), start, end, fill=INK, width=round(w + 2 * self.stroke))
        self.draw.arc(self.box(x0, y0, x1, y1, w / 2), start, end, fill=fill, width=round(w))


def wheel(pen, x, y, r):
    pen.circle(x, y, r, (90, 90, 105))
    pen.circle(x, y, r * 0.4, (215, 215, 225), outline=False)


def bottle(pen, x, y, height, color):
    w = height * 0.42
    pen.ellipse(x - w * 0.22, y, x + w * 0.22, y + height * 0.32, TEAT)
    pen.rect(x - w / 2, y + height * 0.3, x + w / 2, y + height, light(color, 0.75), radius=w * 0.3)
    pen.rect(x - w / 2 + 1.5, y + height * 0.62, x + w / 2 - 1.5, y + height - 1.5, WHITE, radius=w * 0.22, outline=False)
    pen.rect(x - w * 0.58, y + height * 0.22, x + w * 0.58, y + height * 0.36, color, radius=1.5)
    for i in range(3):
        mark = y + height * (0.5 + i * 0.13)
        pen.line([(x + w / 2 - 4, mark), (x + w / 2 - 1, mark)], 0.6)


# --- Strollers --------------------------------------------------------------

def draw_stroller(pen):
    c = pen.color
    pen.bar([(34, 62), (20, 84)], 2.5, GREY)
    pen.bar([(60, 64), (76, 84)], 2.5, GREY)
    pen.bar([(42, 60), (24, 16)], 2.5, GREY)
    pen.bar([(18, 15), (28, 15)], 4, INK)
    pen.poly([(36, 40), (62, 46), (70, 64), (66, 70), (38, 68)], c)
    pen.pieslice(30, 20, 76, 66, 180, 300, dark(c))
    wheel(pen, 20, 85, 7)
    wheel(pen, 76, 85, 7)


def draw_pram(pen):
    c = pen.color
    pen.bar([(32, 64), (70, 86)], 2.5, GREY)
    pen.bar([(68, 64), (30, 86)], 2.5, GREY)
    pen.bar([(78, 52), (90, 24)], 2.5, GREY)
    pen.bar([(86, 22), (94, 26)], 4, INK)
    pen.chord(12, 24, 88, 76, 0, 180, c)
    pen.pieslice(12, 24, 88, 76, 180, 255, dark(c))
    pen.rect(10, 47, 90, 54, light(c), radius=3)
    wheel(pen, 30, 86, 8)
    wheel(pen, 70, 86, 8)


def draw_jogger(pen):
    c = pen.color
    pen.bar([(24, 80), (50, 66), (82, 86)], 2.5, GREY)
    pen.bar([(42, 60), (22, 14)], 2.5, GREY)
    pen.bar([(16, 13), (26, 13)], 4, INK)
    pen.poly([(38, 40), (62, 46), (70, 64), (66, 70), (40, 68)], c)
    pen.pieslice(32, 20, 78, 66, 180, 300, dark(c))
    wheel(pen, 24, 79, 12)
    wheel(pen, 82, 86, 6)


def draw_double_stroller(pen):
    c = pen.color
    pen.bar([(16, 70), (84, 70)], 2.5, GREY)
    pen.bar([(30, 70), (20, 86)], 2.5, GREY)
    pen.bar([(70, 70), (80, 86)], 2.5, GREY)
    pen.bar([(20, 66), (10, 20)], 2.5, GREY)
    pen.bar([(5, 19), (15, 19)], 4, INK)
    for x in (18, 50):
        pen.poly([(x, 44), (x + 24, 48), (x + 30, 66), (x + 2, 68)], c)
        pen.pieslice(x - 4, 26, x + 34, 64, 180, 300, dark(c))
    wheel(pen, 20, 86, 7)
    wheel(pen, 50, 86, 7)
    wheel(pen, 80, 86, 7)


# --- Car seats --------------------------------------------------------------

def draw_infant_car_seat(pen):
    c = pen.color
    pen.rect(16, 80, 84, 90, GREY, radius=3)
    pen.chord(12, 36, 88, 88, 0, 180, c)
    pen.chord(22, 50, 78, 80, 0, 180, light(c), outline=False)
    pen.rect(12, 40, 30, 74, c, radius=8)
    pen.pieslice(8, 22, 58, 72, 180, 270, dark(c))
    pen.arc(22, 30, 78, 94, 180, 360, 3, dark(c))
    pen.circle(22, 62, 3.5, GREY)
    pen.circle(78, 62, 3.5, GREY)


def draw_car_seat(pen, swivel=False):
    c = pen.color
    if swivel:
        pen.ellipse(18, 80, 82, 94, GREY)
        pen.rect(40, 74, 60, 84, dark(GREY), radius=2)
    else:
        pen.rect(20, 82, 80, 92, GREY, radius=3)
    pen.rect(24, 10, 46, 84, c, radius=10)
    pen.rect(20, 10, 50, 36, dark(c), radius=9)
    pen.rect(24, 62, 78, 84, c, radius=9)
    pen.rect(40, 50, 72, 62, light(c), radius=5)
    pen.bar([(46, 40), (54, 66)], 2, INK)


def draw_swivel_car_seat(pen):
    draw_car_seat(pen, swivel=True)


# --- Feeding ----------------------------------------------------------------

def draw_bottle_set(pen):
    bottle(pen, 38, 12, 80, pen.color)
    bottle(pen, 68, 40, 52, light(pen.color, 0.3))


def draw_high_chair(pen):
    c = pen.color
    pen.bar([(38, 58), (24, 92)], 3, dark(c))
    pen.bar([(64, 58), (78, 92)], 3, dark(c))
    pen.bar([(30, 78), (72, 78)], 2.5, dark(c))
    pen.rect(30, 12, 54, 62, c, radius=8)
    pen.rect(30, 52, 72, 62, c, radius=4)
    pen.bar([(68, 46), (68, 54)], 2, GREY)
    pen.rect(56, 40, 86, 47, light(c), radius=3)


def draw_bottle_warmer(pen):
    c = pen.color
    bottle(pen, 50, 8, 52, light(c, 0.3))
    pen.rect(26, 46, 74, 90, c, radius=12)
    pen.ellipse(26, 40, 74, 54, dark(c))
    pen.ellipse(34, 43, 66, 51, INK, outline=False)
    pen.circle(50, 72, 6, WHITE)
    pen.circle(64, 82, 2, (130, 220, 130), outline=False)


def draw_bib(pen):
    c = pen.color
    outer = ellipse_points(50, 58, 30, 34, -60, 240)
    neck = ellipse_points(50, 24, 15.7, 15.7, 163, 17)
    pen.rect(26, 16, 38, 32, c, radius=5)
    pen.rect(62, 16, 74, 32, c, radius=5)
    pen.poly(outer + neck, c)
    pen.chord(20, 24, 80, 92, 25, 155, dark(c))
    for x, y in [(38, 50), (60, 46), (50, 62), (34, 66), (66, 64)]:
        pen.circle(x, y, 2.5, light(c, 0.7), outline=False)


def draw_suction_bowl(pen):
    c = pen.color
    pen.rect(36, 80, 64, 90, dark(c), radius=3)
    pen.chord(14, 30, 86, 88, 0, 180, c)
    pen.ellipse(14, 52, 86, 66, light(c))
    pen.ellipse(22, 54, 78, 64, (250, 222, 150), outline=False)
    pen.bar([(60, 56), (84, 26)], 2.5, light(c, 0.6))
    pen.ellipse(78, 16, 92, 30, light(c, 0.6))


def draw_sippy_cup(pen):
    c = pen.color
    for x in (20, 66):
        pen.arc(x, 48, x + 14, 70, 0, 360, 2.5, dark(c))
    pen.poly([(42, 34), (58, 34), (54, 12), (46, 12)], light(c, 0.6))
    pen.rect(32, 40, 68, 90, c, radius=8)
    pen.rect(30, 30, 70, 42, dark(c), radius=4)
    pen.rect(36, 60, 64, 72, light(c), radius=4, outline=False)


def draw_steam_sterilizer(pen):
    c = pen.color
    pen.chord(20, 20, 80, 100, 180, 360, light(c, 0.75))
    bottle(pen, 40, 30, 32, c)
    bottle(pen, 60, 34, 28, c)
    pen.rect(44, 12, 56, 22, dark(c), radius=3)
    pen.rect(16, 58, 84, 88, c, radius=10)
    pen.circle(50, 73, 5, WHITE)


# --- Nursery ----------------------------------------------------------------

def draw_crib(pen):
    c = pen.color
    pen.rect(18, 60, 82, 70, WHITE, radius=2)
    for x in range(26, 78, 8):
        pen.bar([(x, 36), (x, 74)], 1.6, c)
    pen.rect(14, 30, 86, 37, dark(c), radius=2)
    pen.rect(14, 72, 86, 79, dark(c), radius=2)
    pen.rect(10, 20, 18, 92, c, radius=3)
    pen.rect(82, 20, 90, 92, c, radius=3)


def draw_changing_table(pen):
    c = pen.color
    pen.rect(18, 44, 82, 88, c, radius=4)
    for y in (50, 68):
        pen.rect(24, y, 76, y + 14, light(c), radius=3)
        pen.circle(50, y + 7, 2, dark(c))
    pen.rect(22, 88, 28, 94, dark(c), outline=False)
    pen.rect(72, 88, 78, 94, dark(c), outline=False)
    pen.rect(14, 30, 86, 44, light(c, 0.7), radius=7)
    pen.rect(12, 26, 18, 44, c, radius=2)
    pen.rect(82, 26, 88, 44, c, radius=2)


def draw_rocking_chair(pen):
    c = pen.color
    pen.bar([(32, 58), (30, 85)], 2.5, dark(c))
    pen.bar([(68, 58), (68, 85)], 2.5, dark(c))
    pen.arc(6, 40, 94, 88, 25, 155, 3, dark(c))
    pen.rect(26, 8, 42, 62, c, radius=7)
    pen.rect(26, 52, 74, 60, c, radius=3)
    pen.bar([(36, 40), (70, 40)], 2.5, dark(c))
    pen.bar([(68, 40), (68, 52)], 2, dark(c))
    pen.rect(30, 14, 38, 50, light(c), radius=3, outline=False)


def draw_bassinet(pen):
    c = pen.color
    pen.bar([(36, 64), (64, 90)], 2.5, dark(c))
    pen.bar([(64, 64), (36, 90)], 2.5, dark(c))
    pen.bar([(28, 90), (44, 90)], 2.5, dark(c))
    pen.bar([(56, 90), (72, 90)], 2.5, dark(c))
    pen.chord(14, 22, 86, 72, 0, 180, c)
    pen.pieslice(14, 18, 66, 76, 180, 270, light(c, 0.6))
    pen.rect(12, 44, 88, 50, dark(c), radius=3)


def draw_toy_chest(pen):
    c = pen.color
    pen.circle(34, 30, 11, RAINBOW[0])
    pen.arc(23, 26, 45, 34, 180, 360, 1.5, WHITE)
    pen.rect(54, 20, 70, 38, RAINBOW[2], radius=2)
    pen.circle(62, 28, 2.5, WHITE, outline=False)
    pen.rect(14, 44, 86, 90, c, radius=4)
    pen.rect(10, 38, 90, 50, dark(c), radius=4)
    pen.rect(40, 62, 60, 70, light(c), radius=3)


def draw_dresser(pen):
    c = pen.color
    pen.rect(24, 86, 30, 93, dark(c), outline=False)
    pen.rect(70, 86, 76, 93, dark(c), outline=False)
    pen.rect(18, 24, 82, 88, c, radius=4)
    for y in (30, 50, 70):
        pen.rect(24, y, 76, y + 14, light(c), radius=3)
        pen.circle(50, y + 7, 2, dark(c))
    pen.rect(58, 10, 74, 24, light(RAINBOW[3]), radius=2)
    pen.circle(66, 8, 6, RAINBOW[3])


def draw_bookshelf(pen):
    c = pen.color
    pen.rect(22, 8, 78, 92, c, radius=3)
    pen.rect(27, 13, 73, 87, dark(c, 0.35), outline=False)
    for row, y in enumerate((36, 61, 86)):
        x = 28
        for i, (w, h) in enumerate([(6, 18), (7, 21), (5, 16), (8, 20), (6, 15)]):
            color = RAINBOW[(i + row * 2) % len(RAINBOW)]
            pen.rect(x, y - h, x + w, y, color, radius=1)
            x += w + 1.8
        pen.rect(22, y, 78, y + 4, c)


# --- Toys -------------------------------------------------------------------

def draw_rattle(pen):
    c = pen.color
    pen.rect(45, 48, 55, 84, dark(c), radius=4)
    pen.circle(50, 86, 7, c)
    pen.circle(50, 32, 22, c)
    pen.ellipse(28, 28, 72, 36, light(c))
    for x, y in [(40, 20), (60, 20), (50, 46), (38, 44), (62, 44)]:
        pen.circle(x, y, 2.5, WHITE, outline=False)


def draw_plush_bunny(pen):
    c = pen.color
    pen.ellipse(36, 4, 48, 34, c)
    pen.ellipse(52, 4, 64, 34, c)
    pen.ellipse(39, 9, 45, 30, light(RAINBOW[0], 0.5), outline=False)
    pen.ellipse(55, 9, 61, 30, light(RAINBOW[0], 0.5), outline=False)
    pen.ellipse(30, 50, 70, 92, c)
    pen.ellipse(40, 62, 60, 86, light(c), outline=False)
    pen.circle(24, 70, 7, c)
    pen.circle(76, 70, 7, c)
    pen.circle(50, 38, 16, c)
    pen.circle(44, 36, 2, INK, outline=False)
    pen.circle(56, 36, 2, INK, outline=False)
    pen.circle(50, 42, 2.2, RAINBOW[0], outline=False)


def draw_stacking_rings(pen):
    pen.rect(46, 12, 54, 84, WOOD, radius=3)
    for i, (y, half) in enumerate([(74, 30), (64, 25), (54, 20), (44, 16), (34, 12)]):
        color = pen.color if i == 0 else RAINBOW[i]
        pen.ellipse(50 - half, y - 4, 50 + half, y + 8, color)
    pen.rect(22, 82, 78, 90, WOOD, radius=3)
    pen.circle(50, 14, 6, RAINBOW[0])


def draw_activity_gym(pen):
    c = pen.color
    pen.ellipse(6, 76, 94, 94, light(c))
    for x in (30, 50, 70):
        top = 85 - 71 * (1 - ((x - 50) / 38) ** 2) ** 0.5
        pen.line([(x, top), (x, top + 26)], 0.6)
    pen.poly(star_points(30, 50, 7, 3.2), RAINBOW[2])
    pen.circle(50, 46, 6, RAINBOW[0])
    pen.ellipse(64, 46, 76, 58, RAINBOW[4])
    pen.arc(12, 14, 88, 156, 180, 360, 3, c)


def draw_teether(pen):
    c = pen.color
    pen.ellipse(20, 24, 80, 84, c)
    pen.ellipse(36, 40, 64, 68, pen.stage)
    for angle in range(0, 360, 45):
        x, y = 50 + 23 * cos(radians(angle)), 54 + 23 * sin(radians(angle))
        pen.circle(x, y, 2.5, light(c, 0.6), outline=False)


def draw_wooden_puzzle(pen):
    pen.rect(12, 22, 84, 82, WOOD, radius=6)
    pen.circle(32, 40, 9, dark(WOOD, 0.3))
    pen.rect(52, 32, 72, 50, RAINBOW[4], radius=2)
    pen.circle(62, 41, 2, WHITE)
    pen.poly([(24, 72), (34, 56), (44, 72)], RAINBOW[2])
    pen.circle(34, 66, 2, WHITE)
    pen.poly(star_points(62, 66, 10, 4.5), RAINBOW[0])
    pen.circle(80, 82, 9, pen.color)
    pen.circle(80, 82, 2, WHITE)


def draw_musical_mobile(pen):
    c = pen.color
    for x, length in ((22, 48), (50, 58), (78, 48)):
        pen.line([(x, 22), (x, length)], 0.6)
    pen.bar([(50, 6), (50, 20)], 2, dark(c))
    pen.arc(16, 18, 84, 34, 180, 360, 2.5, c)
    pen.poly(star_points(22, 56, 9, 4), RAINBOW[2])
    pen.circle(50, 68, 11, light(RAINBOW[2], 0.3))
    pen.circle(56, 63, 9, pen.stage, outline=False)
    for x, y, r in ((72, 56, 6), (79, 52, 7), (85, 57, 5)):
        pen.circle(x, y, r, WHITE)
    pen.rect(70, 55, 88, 62, WHITE, radius=3, outline=False)


def draw_shape_sorter(pen):
    c = pen.color
    pen.poly([(20, 40), (36, 26), (80, 26), (64, 40)], light(c))
    pen.poly([(64, 40), (80, 26), (80, 76), (64, 90)], dark(c))
    pen.rect(20, 40, 64, 90, c)
    pen.circle(42, 54, 7, INK, outline=False)
    pen.poly(star_points(42, 76, 8, 3.5), INK, outline=False)
    pen.poly([(44, 30), (50, 36), (56, 30)], INK, outline=False)
    pen.poly([(76, 92), (86, 76), (96, 92)], RAINBOW[2])


# --- Bath & care ------------------------------------------------------------

def draw_baby_bathtub(pen):
    c = pen.color
    for x, y, r in ((30, 40, 6), (42, 32, 8), (56, 38, 6), (66, 30, 5), (74, 42, 6)):
        pen.circle(x, y, r, WHITE)
    pen.rect(22, 84, 30, 92, dark(c), radius=2)
    pen.rect(70, 84, 78, 92, dark(c), radius=2)
    pen.chord(10, 26, 90, 92, 0, 180, c)
    pen.rect(8, 54, 92, 62, light(c), radius=3)


def draw_hooded_towel(pen):
    c = pen.color
    pen.circle(38, 20, 6, c)
    pen.circle(62, 20, 6, c)
    pen.poly([(50, 16), (88, 54), (50, 92), (12, 54)], c)
    pen.poly([(50, 16), (68, 34), (32, 34)], light(c))
    pen.circle(45, 28, 1.5, INK, outline=False)
    pen.circle(55, 28, 1.5, INK, outline=False)
    for y in (62, 70):
        pen.line([(30 + (y - 54), y), (70 - (y - 54), y)], 1.2, light(c, 0.6))


def draw_bath_thermometer(pen):
    c = pen.color
    pen.rect(40, 8, 60, 76, WHITE, radius=10)
    pen.circle(50, 78, 13, c)
    pen.rect(47, 34, 53, 78, c, outline=False)
    for y in range(18, 66, 8):
        pen.line([(56, y), (60, y)], 0.6)
    for x in (18, 76):
        pen.arc(x - 8, 82, x + 8, 92, 200, 340, 1.5, light(c, 0.4))


def draw_grooming_kit(pen):
    c = pen.color
    pen.bar([(34, 88), (36, 52)], 6, dark(c))
    pen.ellipse(20, 12, 52, 56, c)
    for x, y in [(30, 24), (36, 20), (42, 24), (28, 34), (36, 32), (44, 34), (32, 44), (40, 44)]:
        pen.circle(x, y, 1.6, WHITE, outline=False)
    for y in range(24, 86, 6):
        pen.bar([(64, y), (74, y)], 1, light(c))
    pen.rect(58, 18, 66, 88, light(c), radius=3)


def draw_bath_sponge(pen):
    c = pen.color
    for x, y, r in ((30, 26, 6), (44, 18, 8), (60, 24, 5), (70, 16, 4)):
        pen.circle(x, y, r, WHITE)
    pen.rect(18, 38, 82, 86, c, radius=18)
    for x, y in [(30, 52), (44, 48), (60, 54), (70, 66), (36, 70), (52, 72), (66, 46)]:
        pen.ellipse(x - 3, y - 2, x + 3, y + 2, dark(c), outline=False)


def draw_bath_seat(pen):
    c = pen.color
    for x in (24, 50, 76):
        pen.chord(x - 6, 84, x + 6, 96, 180, 360, dark(c))
    pen.ellipse(14, 78, 86, 92, light(c))
    pen.rect(46, 64, 54, 84, c, outline=False)
    pen.rect(22, 18, 42, 70, c, radius=8)
    pen.rect(22, 58, 74, 70, c, radius=5)
    pen.arc(42, 40, 78, 76, 180, 360, 3, dark(c))


def draw_bath_toy_set(pen):
    c = pen.color
    pen.poly([(62, 74), (94, 74), (88, 88), (68, 88)], light(RAINBOW[4], 0.2))
    pen.bar([(77, 40), (77, 74)], 1.2, WOOD)
    pen.poly([(79, 42), (79, 70), (94, 70)], WHITE)
    pen.ellipse(10, 54, 62, 88, c)
    pen.poly([(54, 58), (64, 50), (62, 66)], c)
    pen.circle(26, 44, 14, c)
    pen.poly([(14, 42), (2, 47), (14, 52)], ORANGE)
    pen.circle(24, 40, 2, INK, outline=False)
    pen.chord(30, 60, 54, 80, 0, 180, dark(c))


# --- Clothing ---------------------------------------------------------------

def neckline(left, right, y, depth):
    centre = (left + right) / 2
    return [(right, y), (centre + (right - centre) * 0.6, y + depth * 0.7), (centre, y + depth), (centre - (centre - left) * 0.6, y + depth * 0.7), (left, y)]


def draw_bodysuit(pen):
    c = pen.color
    pen.poly([
        (40, 12), (26, 14), (10, 30), (18, 42), (30, 34), (30, 62), (33, 74), (40, 86), (60, 86), (67, 74),
        (70, 62), (70, 34), (82, 42), (90, 30), (74, 14), (60, 12), *neckline(40, 60, 12, 8)[:-1],
    ], c)
    pen.rect(40, 82, 60, 88, dark(c), radius=2)
    for x in (44, 50, 56):
        pen.circle(x, 85, 1.4, WHITE, outline=False)


def draw_sleepsuit(pen, hood=False):
    c = pen.color
    if hood:
        pen.circle(50, 14, 14, dark(c))
        pen.circle(50, 15, 9, pen.stage)
    pen.poly([
        (40, 18), (26, 20), (10, 52), (20, 56), (30, 36), (30, 64), (28, 90), (46, 92), (48, 66), (52, 66),
        (54, 92), (72, 90), (70, 64), (70, 36), (80, 56), (90, 52), (74, 20), (60, 18), *neckline(40, 60, 18, 6)[:-1],
    ], c)
    pen.line([(50, 26), (50, 64)], 1, dark(c))
    if hood:
        for y in (34, 46, 58, 76):
            pen.line([(32, y), (68, y)], 0.8, dark(c, 0.1))


def draw_snowsuit(pen):
    draw_sleepsuit(pen, hood=True)


def draw_cardigan(pen):
    c = pen.color
    pen.poly([(38, 12), (24, 14), (8, 56), (20, 60), (28, 36), (28, 86), (72, 86), (72, 36), (80, 60), (92, 56), (76, 14), (62, 12), (50, 40)], c)
    pen.rect(28, 78, 72, 86, dark(c), radius=2)
    pen.line([(50, 40), (50, 86)], 0.8)
    for y in (48, 58, 68):
        pen.circle(54, y, 2, WHITE)


def draw_romper(pen):
    c = pen.color
    pen.bar([(36, 32), (32, 10)], 4, c)
    pen.bar([(64, 32), (68, 10)], 4, c)
    pen.poly([(28, 30), (72, 30), (72, 62), (82, 86), (56, 88), (50, 74), (44, 88), (18, 86), (28, 62)], c)
    pen.rect(40, 38, 60, 52, light(c), radius=3)
    pen.circle(36, 32, 2, WHITE)
    pen.circle(64, 32, 2, WHITE)


def draw_sleeping_bag(pen):
    c = pen.color
    pen.rect(28, 10, 40, 32, c, radius=5)
    pen.rect(60, 10, 72, 32, c, radius=5)
    pen.rect(22, 24, 78, 92, c, radius=18)
    pen.ellipse(38, 14, 62, 34, pen.stage)
    pen.line([(56, 34), (56, 84)], 1, dark(c))
    for x, y in [(36, 52), (44, 72), (66, 60), (68, 80)]:
        pen.poly(star_points(x, y, 4, 1.8), light(c, 0.7), outline=False)


def draw_beanie_and_mittens(pen):
    c = pen.color
    pen.chord(12, 12, 64, 76, 180, 360, c)
    pen.rect(10, 40, 66, 52, dark(c), radius=4)
    pen.circle(38, 12, 7, light(c, 0.6))
    for x, y in ((50, 58), (70, 54)):
        pen.ellipse(x - 6, y + 8, x + 4, y + 22, c)
        pen.rect(x, y, x + 18, y + 32, c, radius=9)
        pen.rect(x, y + 26, x + 18, y + 36, dark(c), radius=2)


# --- Diapering --------------------------------------------------------------

def draw_diaper_bag(pen):
    c = pen.color
    pen.arc(30, 14, 70, 62, 180, 360, 3.5, dark(c))
    pen.rect(14, 36, 86, 90, c, radius=10)
    pen.rect(14, 36, 86, 56, dark(c), radius=10)
    pen.rect(44, 50, 56, 60, WHITE, radius=2)
    pen.rect(28, 66, 72, 84, light(c), radius=6)


def draw_changing_mat(pen):
    c = pen.color
    pen.rect(6, 46, 94, 88, c, radius=14)
    pen.rect(16, 54, 84, 80, light(c), radius=8)
    for x in range(26, 80, 12):
        pen.line([(x, 58), (x, 76)], 0.6, c)
    pen.rect(10, 50, 24, 84, dark(c), radius=7)


def draw_wipes_warmer(pen):
    c = pen.color
    pen.poly([(42, 40), (40, 26), (46, 20), (54, 24), (60, 20), (62, 40)], WHITE)
    pen.rect(20, 46, 80, 90, c, radius=10)
    pen.rect(18, 36, 82, 52, dark(c), radius=8)
    pen.rect(38, 40, 62, 46, INK, radius=2, outline=False)
    pen.circle(68, 78, 3, (130, 220, 130))


def draw_diaper_pail(pen):
    c = pen.color
    pen.rect(42, 86, 58, 94, GREY, radius=2)
    pen.poly([(28, 34), (72, 34), (68, 90), (32, 90)], c)
    pen.rect(42, 18, 58, 28, dark(c), radius=3)
    pen.rect(22, 26, 78, 38, dark(c), radius=6)
    pen.rect(34, 50, 66, 58, light(c), radius=3, outline=False)


def draw_cloth_diaper_set(pen):
    for offset, color in ((8, light(pen.color, 0.4)), (0, pen.color)):
        x, y = offset, -offset
        pen.poly([(14 + x, 34 + y), (86 + x, 34 + y), (80 + x, 56 + y), (62 + x, 84 + y), (38 + x, 84 + y), (20 + x, 56 + y)], color)
        pen.rect(14 + x, 34 + y, 86 + x, 44 + y, light(color), radius=2)
    for x in (22, 34, 66, 78):
        pen.circle(x, 39, 2, WHITE)


def draw_changing_caddy(pen):
    c = pen.color
    pen.rect(18, 18, 30, 52, WHITE, radius=3)
    pen.rect(20, 12, 28, 20, RAINBOW[0], radius=2)
    pen.rect(62, 28, 84, 52, light(RAINBOW[4], 0.3), radius=4)
    pen.bar([(46, 44), (46, 18)], 3, dark(c))
    pen.bar([(54, 44), (54, 18)], 3, dark(c))
    pen.rect(36, 12, 64, 20, dark(c), radius=4)
    pen.poly([(12, 44), (88, 44), (82, 90), (18, 90)], c)
    pen.rect(12, 44, 88, 52, light(c), radius=2)


def draw_gift(pen):
    c = pen.color
    pen.ellipse(30, 18, 50, 40, light(c, 0.6))
    pen.ellipse(50, 18, 70, 40, light(c, 0.6))
    pen.rect(22, 48, 78, 92, c, radius=3)
    pen.rect(18, 38, 82, 50, dark(c), radius=3)
    pen.rect(45, 38, 55, 92, light(c, 0.6))
    pen.circle(50, 37, 5, light(c, 0.6))


DRAWINGS = {
    "Stroller": draw_stroller,
    "Travel System": draw_pram,
    "Jogging Stroller": draw_jogger,
    "Compact Buggy": draw_stroller,
    "Pram": draw_pram,
    "Double Stroller": draw_double_stroller,
    "Infant Car Seat": draw_infant_car_seat,
    "Convertible Car Seat": draw_car_seat,
    "Rear-Facing Car Seat": draw_car_seat,
    "Swivel Car Seat": draw_swivel_car_seat,
    "Baby Bottle Set": draw_bottle_set,
    "High Chair": draw_high_chair,
    "Bottle Warmer": draw_bottle_warmer,
    "Silicone Bib": draw_bib,
    "Suction Bowl": draw_suction_bowl,
    "Sippy Cup": draw_sippy_cup,
    "Steam Sterilizer": draw_steam_sterilizer,
    "Crib": draw_crib,
    "Changing Table": draw_changing_table,
    "Rocking Chair": draw_rocking_chair,
    "Bassinet": draw_bassinet,
    "Toy Chest": draw_toy_chest,
    "Dresser": draw_dresser,
    "Bookshelf": draw_bookshelf,
    "Rattle": draw_rattle,
    "Plush Bunny": draw_plush_bunny,
    "Stacking Rings": draw_stacking_rings,
    "Activity Gym": draw_activity_gym,
    "Teether": draw_teether,
    "Wooden Puzzle": draw_wooden_puzzle,
    "Musical Mobile": draw_musical_mobile,
    "Shape Sorter": draw_shape_sorter,
    "Baby Bathtub": draw_baby_bathtub,
    "Hooded Towel": draw_hooded_towel,
    "Bath Thermometer": draw_bath_thermometer,
    "Grooming Kit": draw_grooming_kit,
    "Bath Sponge": draw_bath_sponge,
    "Bath Seat": draw_bath_seat,
    "Bath Toy Set": draw_bath_toy_set,
    "Bodysuit": draw_bodysuit,
    "Sleepsuit": draw_sleepsuit,
    "Knitted Cardigan": draw_cardigan,
    "Romper": draw_romper,
    "Sleeping Bag": draw_sleeping_bag,
    "Beanie & Mittens Set": draw_beanie_and_mittens,
    "Snowsuit": draw_snowsuit,
    "Diaper Bag": draw_diaper_bag,
    "Changing Mat": draw_changing_mat,
    "Wipes Warmer": draw_wipes_warmer,
    "Diaper Pail": draw_diaper_pail,
    "Cloth Diaper Set": draw_cloth_diaper_set,
    "Changing Caddy": draw_changing_caddy,
}


def illustration(item, color, background):
    """Returns a picture of the item in the given colour; unknown items get a gift box."""
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), background)
    stage = light(background, 0.55)
    pen = Pen(image, color, stage)
    pen.circle(50, 50, 52, stage, outline=False)
    pen.ellipse(12, 89, 88, 97, dark(stage, 0.08), outline=False)
    DRAWINGS.get(item, draw_gift)(pen)
    return image.resize((WIDTH, HEIGHT), Image.LANCZOS)
