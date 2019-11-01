from decimal import Decimal

from shop.models.cart import Cart
from shop.models.cart_item import CartItem
from shop.models.category import Category
from shop.models.company import Company
from shop.models.product import Product
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestCartItem(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.TEST_URL = "/api/cart_items/"

        cls.normal_user = User.objects.create_user(
            username="Test Normal User", email="testowyuser@mail.pl", password="testuje"
        )

        cls.test_category = Category.objects.create(name="Whey", description="Mmm bialeczko")

        cls.test_company = Company.objects.create(name="Test company", description="Test description")

        cls.test_product_1 = Product.objects.create(
            name="BOOOM Creatine",
            description="Best whey ever",
            category=cls.test_category,
            company=cls.test_company,
            normal_price="5.50",
            quantity_in_stock=500,
        )

        cls.test_cart = Cart.objects.create(user=cls.normal_user, is_active=True)

    def test_cart_item_total_quantity_is_properly(self) -> None:
        self.client.force_login(self.normal_user)
        test_cart_item = CartItem.objects.create(product=self.test_product_1, quantity=2, cart=self.test_cart)

        get_test_cart_item = self.client.get(f"{self.TEST_URL}{test_cart_item.pk}/")

        self.assertEqual(
            get_test_cart_item.data,
            {
                "cart": self.test_cart.pk,
                "product": test_cart_item.product.name,
                "quantity": test_cart_item.quantity,
                "price": Decimal("11.00"),
            },
        )

        self.assertEqual(get_test_cart_item.status_code, 200)

    def test_cant_create_cart_item_when_quantity_will_be_lower_than_zero_after_add(self) -> None:
        post_cart_item = self.client.post(
            self.TEST_URL,
            {
                "product": self.test_product_1.name,
                "quantity": self.test_product_1.quantity_in_stock + 1,
                "cart": self.test_cart.pk,
            },
        )

        self.assertEqual(str(post_cart_item.data[0]), "You can order only 500")
        self.assertEqual(post_cart_item.status_code, 400)

    def test_cant_add_product_to_cart_item_when_is_stock_is_equal_false(self) -> None:
        self.test_product_1.is_in_stock = False
        self.test_product_1.save()

        post_cart_item = self.client.post(
            self.TEST_URL, {"product": self.test_product_1.name, "quantity": 1, "cart": self.test_cart.pk}
        )

        self.assertEqual(str(post_cart_item.data[0]), "Product is not available now!")
        self.assertEqual(post_cart_item.status_code, 400)
