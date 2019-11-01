import decimal

from shop.models.cart import Cart
from shop.models.cart_item import CartItem
from shop.models.category import Category
from shop.models.company import Company
from shop.models.product import Product
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from shop.utils.cart import has_user_active_cart, get_active_cart_or_create


class TestCartItem(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.TEST_URL_CART = "/api/carts/"
        cls.TEST_URL_CART_ITEM = "/api/cart_items/"

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
            quantity_in_stock=500,
            normal_price="5.50",
        )

        cls.test_product_2 = Product.objects.create(
            name="Uga Buga 2",
            description="Best whey ever seen",
            category=cls.test_category,
            company=cls.test_company,
            quantity_in_stock=500,
            normal_price="10.50",
        )

        cls.test_cart = Cart.objects.create(user=cls.normal_user)

    def test_cart_total_quantity_is_properly(self) -> None:
        self.client.force_login(self.normal_user)
        CartItem.objects.create(product=self.test_product_1, quantity=2, cart=self.test_cart)

        CartItem.objects.create(product=self.test_product_2, quantity=1, cart=self.test_cart)

        get_test_cart = self.client.get(f"{self.TEST_URL_CART}{self.test_cart.pk}/")
        self.assertEqual(get_test_cart.data["total_quantity"], 3)
        self.assertEqual(get_test_cart.status_code, 200)

    def test_cart_total_price_is_properly(self) -> None:
        self.client.force_login(self.normal_user)
        CartItem.objects.create(product=self.test_product_1, quantity=2, cart=self.test_cart)

        CartItem.objects.create(product=self.test_product_2, quantity=1, cart=self.test_cart)

        get_test_cart = self.client.get(f"{self.TEST_URL_CART}{self.test_cart.pk}/")
        self.assertEqual(get_test_cart.data["total_price"], decimal.Decimal("21.50"))
        self.assertEqual(get_test_cart.status_code, 200)

    def test_user_has_not_active_cart(self) -> None:
        has_active = has_user_active_cart(self.normal_user)

        self.assertFalse(has_active)

    def test_user_has_got_active_cart(self) -> None:
        Cart.objects.create(user=self.normal_user, is_active=True)

        has_active = has_user_active_cart(self.normal_user)

        self.assertTrue(has_active)

    def test_create_cart_if_needed(self) -> None:
        test_user = User.objects.create_user(username="Test User", email="testowy2user@mail.pl", password="testuje")
        self.client.force_login(test_user)

        cart = get_active_cart_or_create(test_user)

        self.assertEqual(Cart.objects.get(user=test_user), cart)

    def test_cart_created_correctly_after_adding_first_item_to_cart_with_user_which_does_not_have_any_cart(self):
        test_user = User.objects.create_user(username="Test Us3r", email="testowy3user@mail.pl", password="testuje")
        self.client.force_login(test_user)

        self.client.post(self.TEST_URL_CART_ITEM, {"product": self.test_product_1.name, "quantity": 1})
        actual_user_carts = Cart.objects.filter(user=test_user)

        self.assertEqual(len(actual_user_carts), 1)
