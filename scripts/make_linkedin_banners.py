"""
Generate LinkedIn banner images from the FocusPsychology postcard artwork.
Produces:
  images/linkedin-banner-company.png   (1128 x 191  - company page cover)
  images/linkedin-banner-personal.png  (1584 x 396  - personal profile cover)

Both keep the bottom-left "safe zone" clear of important detail, since
LinkedIn overlays the company logo / profile photo there.
"""

from PIL import Image, ImageDraw
import math

PALETTE = {
    "navy": (6, 37, 75),
    "royal": (31, 72, 255),
    "royal_dark": (22, 54, 196),
    "teal": (0, 151, 178),
    "cyan": (12, 192, 223),
    "periwinkle": (81, 112, 255),
    "purple": (140, 82, 255),
    "poster_bg": (12, 105, 150),
    "light": (56, 182, 255),
}

PORTRAIT_PATH = "assets/img/hero-portrait.png"


def diagonal_gradient(size, c1, c2, grid=120):
    """Cheap smooth diagonal gradient: compute on a small grid, upscale."""
    w, h = size
    small = Image.new("RGB", (grid, grid))
    px = small.load()
    for y in range(grid):
        for x in range(grid):
            t = (x + y) / (2 * (grid - 1))
            r = round(c1[0] + (c2[0] - c1[0]) * t)
            g = round(c1[1] + (c2[1] - c1[1]) * t)
            b = round(c1[2] + (c2[2] - c1[2]) * t)
            px[x, y] = (r, g, b)
    return small.resize((w, h), Image.BICUBIC)


def draw_circle_cluster(draw, circles):
    """circles: list of (cx, cy, r, fill, outline_w)"""
    for cx, cy, r, fill in circles:
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=fill,
            outline=(0, 0, 0),
            width=max(2, r // 14),
        )


def make_banner(out_path, width, height, safe_w, safe_h, portrait_h_ratio, circle_plan, diamond=None):
    img = diagonal_gradient((width, height), PALETTE["navy"], PALETTE["poster_bg"])
    draw = ImageDraw.Draw(img)

    # decorative circle cluster bridging the safe zone and the portrait
    draw_circle_cluster(draw, circle_plan)

    if diamond:
        cx, cy, s, fill, angle = diamond
        square = Image.new("RGBA", (s * 3, s * 3), (0, 0, 0, 0))
        sd = ImageDraw.Draw(square)
        pad = s
        sd.rectangle([pad, pad, pad + s, pad + s], fill=fill, outline=(0, 0, 0), width=max(2, s // 10))
        square = square.rotate(angle, resample=Image.BICUBIC, expand=True)
        img.paste(square, (cx - square.width // 2, cy - square.height // 2), square)

    # portrait, framed, on the right
    portrait = Image.open(PORTRAIT_PATH).convert("RGBA")
    target_h = int(height * portrait_h_ratio)
    target_w = int(portrait.width * (target_h / portrait.height))
    portrait = portrait.resize((target_w, target_h), Image.LANCZOS)

    margin_right = int(height * 0.08)
    px = width - margin_right - target_w
    py = (height - target_h) // 2

    # soft shadow behind the framed portrait for separation from the gradient
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle(
        [px + 6, py + 8, px + target_w + 6, py + target_h + 8], fill=(0, 0, 0, 110)
    )
    shadow = shadow.filter(__import__("PIL.ImageFilter", fromlist=["ImageFilter"]).GaussianBlur(12))
    img = Image.alpha_composite(img.convert("RGBA"), shadow)

    img.paste(portrait, (px, py), portrait)

    img = img.convert("RGB")
    img.save(out_path, optimize=True)
    print(out_path, img.size)


# ---------------- Company page banner: 1128 x 191 ----------------
# Logo box overlaps roughly the bottom-left ~140x140, so keep x<230 / y>90 clear.
make_banner(
    out_path="images/linkedin-banner-company.png",
    width=1128,
    height=191,
    safe_w=230,
    safe_h=100,
    portrait_h_ratio=0.86,
    circle_plan=[
        (330, 60, 26, PALETTE["periwinkle"]),
        (390, 120, 34, PALETTE["navy"]),
        (460, 70, 22, PALETTE["cyan"]),
        (540, 130, 30, PALETTE["teal"]),
        (610, 55, 18, PALETTE["royal"]),
    ],
    diamond=(470, 40, 16, PALETTE["purple"], 22),
)

# ---------------- Personal profile banner: 1584 x 396 ----------------
# Profile photo overlaps roughly a 220px circle bottom-left, so keep
# x<430 / y>210 relatively clear.
make_banner(
    out_path="images/linkedin-banner-personal.png",
    width=1584,
    height=396,
    safe_w=430,
    safe_h=210,
    portrait_h_ratio=0.82,
    circle_plan=[
        (560, 120, 46, PALETTE["periwinkle"]),
        (660, 230, 60, PALETTE["navy"]),
        (770, 110, 40, PALETTE["cyan"]),
        (880, 240, 52, PALETTE["teal"]),
        (960, 100, 32, PALETTE["royal"]),
        (700, 60, 20, PALETTE["light"]),
    ],
    diamond=(800, 70, 26, PALETTE["purple"], 22),
)
