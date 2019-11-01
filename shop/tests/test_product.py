from shop.models.cart import Cart
from shop.models.cart_item import CartItem
from shop.models.category import Category
from shop.models.company import Company
from shop.models.product import Product
from shop.models.review import Review
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestProduct(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.TEST_PRODUCTS_URL = "/api/products/"
        cls.TEST_CART_ITEMS_URL = "/api/cart_items/"
        cls.staff_tester = User.objects.create_user(
            username="Test Staff user", email="testowystaff@mail.pl", password="testuje", is_staff=True
        )

        cls.normal_user = User.objects.create_user(
            username="Test Normal User", email="testowyuser@mail.pl", password="testuje"
        )

        cls.test_category = Category.objects.create(name="Whey", description="Mmm bialeczko")

        cls.test_company = Company.objects.create(name="Test company", description="Test description")

        cls.test_cart = Cart.objects.create(user=cls.normal_user)

    def test_get_product_response_show_correct_json(self) -> None:
        self.client.force_login(self.normal_user)
        test_product = Product.objects.create(
            name="BOOOM Creatine",
            description="Best creatine ever",
            category=self.test_category,
            company=self.test_company,
            normal_price="90.30",
            quantity_in_stock=500,
        )
        test_review = Review.objects.create(user=self.normal_user, rate=5, opinion="Good enough", product=test_product)
        get_test_product = self.client.get(f"{self.TEST_PRODUCTS_URL}{test_product.pk}/")

        self.assertEqual(
            get_test_product.data,
            {
                "name": test_product.name,
                "description": test_product.description,
                "category": test_product.category.name,
                "company": test_product.company.name,
                "normal_price": test_product.normal_price,
                "is_promoted": False,
                "promotion_price": None,
                "reviews": [f"{test_review.user}, {test_review.opinion}, {test_review.rate}"],
                "is_in_stock": True,
                "quantity_in_stock": 500,
            },
        )

        self.assertEqual(get_test_product.status_code, 200)

    def test_after_updating_cart_item_quantity_in_stock_will_change_properly(self) -> None:
        self.client.force_login(self.normal_user)
        test_product = Product.objects.create(
            name="BOOOM Creatine_V2",
            description="Best creatine ever",
            category=self.test_category,
            company=self.test_company,
            normal_price="90.30",
            quantity_in_stock=500,
        )
        test_cart_item = CartItem.objects.create(product=test_product, quantity=2, cart=self.test_cart)

        put_cart_item = self.client.put(
            f"{self.TEST_CART_ITEMS_URL}{test_cart_item.pk}/",
            {"product": test_product.name, "quantity": 3, "cart": self.test_cart.pk},
        )

        filter_product = Product.objects.get(pk=test_product.pk)
        self.assertEqual(put_cart_item.status_code, 200)
        self.assertEqual(filter_product.quantity_in_stock, 499)

    def test_after_adding_cart_item_quantity_in_stock_will_change_properly(self) -> None:
        self.client.force_login(self.normal_user)
        test_product = Product.objects.create(
            name="BOOOM Creatine_V2",
            description="Best creatine ever",
            category=self.test_category,
            company=self.test_company,
            normal_price="90.30",
            quantity_in_stock=500,
        )

        post_cart_item = self.client.post(
            self.TEST_CART_ITEMS_URL, {"product": test_product.name, "quantity": 3, "cart": self.test_cart.pk}
        )
        filtered_product = Product.objects.get(pk=test_product.pk)

        self.assertEqual(post_cart_item.status_code, 201)
        self.assertEqual(filtered_product.quantity_in_stock, 497)

    def test_after_quantity_will_reach_0_change_is_in_stock_to_false(self) -> None:
        self.client.force_login(self.normal_user)
        test_product = Product.objects.create(
            name="BOOOM Creatine_V2",
            description="Best creatine ever",
            category=self.test_category,
            company=self.test_company,
            normal_price="90.30",
            quantity_in_stock=500,
        )

        post_cart_item = self.client.post(
            self.TEST_CART_ITEMS_URL,
            {"product": test_product.name, "quantity": test_product.quantity_in_stock, "cart": self.test_cart.pk},
        )

        filtered_product = Product.objects.get(pk=test_product.pk)

        self.assertEqual(post_cart_item.status_code, 201)
        self.assertEqual(filtered_product.quantity_in_stock, 0)
        self.assertEqual(filtered_product.is_in_stock, False)
