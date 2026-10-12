import shutil
import tempfile
from io import StringIO

from django.core.files.storage import default_storage
from django.core.management import call_command
from django.test import TestCase, override_settings

from .management.commands.seed_products import CATEGORIES
from .management.illustrations import DRAWINGS
from .models import Product

MEDIA_ROOT = tempfile.mkdtemp()


def seed(**options):
    call_command("seed_products", stdout=StringIO(), **options)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class SeedProductsCommandTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_creates_products_with_category_and_image(self):
        seed(count=10, seed=1)

        self.assertEqual(Product.objects.count(), 10)
        for product in Product.objects.all():
            self.assertIsNotNone(product.category)
            self.assertTrue(product.image.storage.exists(product.image.name))

    def test_every_item_has_a_drawing(self):
        for data in CATEGORIES:
            for item in data["items"]:
                self.assertIn(item, DRAWINGS)

    def test_creates_default_image(self):
        seed(count=1)
        default_image = Product._meta.get_field("image").default
        self.assertTrue(default_storage.exists(default_image))

    def test_does_not_duplicate_without_clear(self):
        seed(count=5)
        seed(count=5)
        self.assertEqual(Product.objects.count(), 5)

    def test_clear_replaces_products(self):
        seed(count=5)
        seed(count=8, clear=True)
        self.assertEqual(Product.objects.count(), 8)

    def test_product_pages_render(self):
        seed(count=8)
        product = Product.objects.first()

        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get(f"/categories/{product.category.slug}").status_code, 200)
        self.assertEqual(self.client.get(f"/{product.category.slug}/{product.id}").status_code, 200)
