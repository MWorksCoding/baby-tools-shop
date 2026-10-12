import random
from decimal import Decimal
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from PIL import Image, ImageDraw, ImageFont

from products.models import Category, Product

CATEGORIES = [
    {
        "name": "Strollers",
        "slug": "strollers",
        "color": (189, 224, 254),
        "price": (149, 899),
        "items": ["Stroller", "Travel System", "Jogging Stroller", "Compact Buggy", "Pram", "Double Stroller"],
        "features": [
            "One-hand fold makes it easy to stow in any car boot.",
            "All-terrain wheels with suspension keep the ride smooth.",
            "The extra-large basket fits a full day's essentials.",
            "A reversible seat lets your baby face you or the world.",
            "The UPF 50+ canopy protects from sun and light rain.",
        ],
    },
    {
        "name": "Car Seats",
        "slug": "car-seats",
        "color": (205, 180, 219),
        "price": (89, 549),
        "items": ["Infant Car Seat", "Convertible Car Seat", "Rear-Facing Car Seat", "Swivel Car Seat"],
        "features": [
            "Side-impact protection keeps your little one safe on every trip.",
            "ISOFIX connectors make installation quick and secure.",
            "The adjustable headrest grows with your child.",
            "Clear indicators show when the seat is installed correctly.",
            "Breathable padding keeps your baby cool on long drives.",
        ],
    },
    {
        "name": "Feeding",
        "slug": "feeding",
        "color": (255, 200, 221),
        "price": (5, 129),
        "items": ["Baby Bottle Set", "High Chair", "Bottle Warmer", "Silicone Bib", "Suction Bowl", "Sippy Cup", "Steam Sterilizer"],
        "features": [
            "Dishwasher-safe parts make cleaning quick and easy.",
            "Made from food-safe materials you can trust.",
            "Designed to make mealtimes calmer and less messy.",
            "Easy to use with one hand while holding your baby.",
            "Compact enough for small kitchens and travel.",
        ],
    },
    {
        "name": "Nursery",
        "slug": "nursery",
        "color": (255, 223, 186),
        "price": (39, 999),
        "items": ["Crib", "Changing Table", "Rocking Chair", "Bassinet", "Toy Chest", "Dresser", "Bookshelf"],
        "features": [
            "Made from sustainably sourced, solid wood.",
            "A calm, timeless design that fits any nursery style.",
            "Rounded edges and a stable frame for peace of mind.",
            "Quick to assemble with clear step-by-step instructions.",
            "Built to last from the newborn days to the toddler years.",
        ],
    },
    {
        "name": "Toys",
        "slug": "toys",
        "color": (202, 255, 191),
        "price": (7, 89),
        "items": ["Rattle", "Plush Bunny", "Stacking Rings", "Activity Gym", "Teether", "Wooden Puzzle", "Musical Mobile", "Shape Sorter"],
        "features": [
            "Bright colours and contrasting patterns stimulate the senses.",
            "Encourages fine motor skills and hand-eye coordination.",
            "Made with non-toxic, child-safe paints and materials.",
            "Easy to wipe clean after play.",
            "Sized just right for small hands.",
        ],
    },
    {
        "name": "Bath & Care",
        "slug": "bath-care",
        "color": (160, 230, 230),
        "price": (4, 79),
        "items": ["Baby Bathtub", "Hooded Towel", "Bath Thermometer", "Grooming Kit", "Bath Sponge", "Bath Seat", "Bath Toy Set"],
        "features": [
            "Gentle on delicate newborn skin.",
            "Makes bath time safe, calm and fun.",
            "Easy to clean and quick to dry.",
            "Compact design that is easy to store and travel with.",
            "Recommended by midwives for everyday care.",
        ],
    },
    {
        "name": "Clothing",
        "slug": "clothing",
        "color": (255, 241, 168),
        "price": (9, 59),
        "items": ["Bodysuit", "Sleepsuit", "Knitted Cardigan", "Romper", "Sleeping Bag", "Beanie & Mittens Set", "Snowsuit"],
        "features": [
            "Made from 100% organic cotton that is gentle on delicate skin.",
            "Envelope shoulders and poppers make changing quick.",
            "Breathable fabric keeps your baby comfortable day and night.",
            "Machine washable and keeps its shape wash after wash.",
            "Available in sizes from newborn to 24 months.",
        ],
    },
    {
        "name": "Diapering",
        "slug": "diapering",
        "color": (222, 222, 222),
        "price": (6, 99),
        "items": ["Diaper Bag", "Changing Mat", "Wipes Warmer", "Diaper Pail", "Cloth Diaper Set", "Changing Caddy"],
        "features": [
            "Makes every diaper change quicker and easier.",
            "Thoughtfully designed by parents, for parents.",
            "Compact enough to take anywhere.",
            "Easy to clean and built for daily use.",
            "Gentle on your baby and kind to the planet.",
        ],
    },
]

BRANDS = ["Little Lamb", "Bumblebee Baby", "Pebble & Pip", "Moonbeam", "Snugglebug", "Tiny Otter", "Honeydew Kids", "Sprout & Co"]
ADJECTIVES = ["Cozy", "Classic", "Comfort", "Deluxe", "Eco", "Mini", "Pro", "Lite", "Dreamy", "Soft"]
COLORS = ["Mint", "Sand", "Sky Blue", "Blush", "Graphite", "Oat", "Sage", "Lavender"]
GENERIC_FEATURES = [
    "Free from BPA, PVC and phthalates.",
    "Tested to the latest European safety standards.",
    "Comes with a 2-year manufacturer warranty.",
    "Loved by parents and approved by little ones.",
    "Packaged in recyclable materials.",
]
CENTS = [Decimal("0.00"), Decimal("0.49"), Decimal("0.95"), Decimal("0.99")]


def placeholder_image(title, subtitle, color):
    image = Image.new("RGB", (600, 460), color)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((30, 30, 570, 430), radius=28, fill=(255, 255, 255))
    draw.ellipse((260, 70, 340, 150), fill=color)

    words, lines = title.split(), [""]
    for word in words:
        candidate = f"{lines[-1]} {word}".strip()
        if len(candidate) > 20 and lines[-1]:
            lines.append(word)
        else:
            lines[-1] = candidate

    draw.multiline_text(
        (300, 265), "\n".join(lines), font=ImageFont.load_default(size=40),
        fill=(51, 51, 51), anchor="mm", align="center", spacing=10,
    )
    draw.text((300, 395), subtitle.upper(), font=ImageFont.load_default(size=22), fill=(120, 120, 120), anchor="mm")

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Fills the database with random baby shop categories and products."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=40, help="Number of products to create (default: 40).")
        parser.add_argument("--clear", action="store_true", help="Delete all existing products (and their images) first.")
        parser.add_argument("--seed", type=int, help="Random seed, to get the same data on every run.")

    @transaction.atomic
    def handle(self, *args, **options):
        rng = random.Random(options["seed"])

        if options["clear"]:
            default_image = Product._meta.get_field("image").default
            for product in Product.objects.all():
                if product.image and product.image.name != default_image:
                    product.image.delete(save=False)
            deleted, _ = Product.objects.all().delete()
            self.stdout.write(f"Deleted {deleted} existing products.")
        elif Product.objects.exists():
            self.stdout.write(self.style.WARNING(
                "The database already contains products, nothing was created. Use --clear to replace them."
            ))
            return

        categories = []
        for data in CATEGORIES:
            category, _ = Category.objects.get_or_create(slug=data["slug"], defaults={"name": data["name"]})
            categories.append((category, data))

        used_names = set()
        for i in range(options["count"]):
            category, data = categories[i % len(categories)]

            name = None
            while name is None or name in used_names:
                name = (
                    f"{rng.choice(BRANDS)} {rng.choice(ADJECTIVES)} "
                    f"{rng.choice(data['items'])} ({rng.choice(COLORS)})"
                )
            used_names.add(name)

            features = rng.sample(data["features"], 2) + rng.sample(GENERIC_FEATURES, 1)
            low, high = data["price"]
            product = Product(
                name=name,
                description=" ".join(features),
                price=Decimal(rng.randint(low, high)) + rng.choice(CENTS),
                category=category,
            )
            product.image.save(f"{slugify(name)}.png", placeholder_image(name, category.name, data["color"]), save=False)
            product.save()

        self.stdout.write(self.style.SUCCESS(
            f"Created {options['count']} products in {len(categories)} categories."
        ))
