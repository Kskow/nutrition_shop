from shop.models.category import Category
from shop.models.company import Company
from shop.models.product import Product
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class IsStaffPermission(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.TEST_URL = "/api/products/"

        cls.staff_tester = User.objects.create_user(
            username="Test Staff user", email="testowystaff@mail.pl", password="testuje", is_staff=True
        )

        cls.normal_user = User.objects.create_user(
            username="Test Normal User", email="testowyuser@mail.pl", password="testuje"
        )

        cls.test_category = Category.objects.create(name="Whey", description="Mmm bialeczko")

        cls.test_company = Company.objects.create(name="Test company", description="Test description")

        cls.test_product_1 = Product.objects.create(
            name="Test Product",
            description="Test description",
            category=cls.test_category,
            company=cls.test_company,
            quantity_in_stock=500,
            normal_price="90.30",
        )

        cls.test_product_2 = Product.objects.create(
            name="Test Product_2",
            description="Test description",
            category=cls.test_category,
            company=cls.test_company,
            quantity_in_stock=500,
            normal_price="90.30",
        )

    def test_staff_user_is_able_to_perform_post(self) -> None:
        self.client.force_login(self.staff_tester)
        add_nutrition = self.client.post(
            self.TEST_URL,
            {
                "name": "Test nutrition",
                "description": "Test description",
                "category": self.test_category.name,
                "company": self.test_company.name,
                "quantity_in_stock": 500,
                "normal_price": "90.30",
            },
        )

        self.assertEqual(add_nutrition.status_code, 201)

    def test_no_staff_user_is_not_able_to_perform_post(self) -> None:
        self.client.force_login(self.normal_user)
        add_nutrition = self.client.post(
            self.TEST_URL,
            {
                "name": "Test nutrition",
                "description": "Test description",
                "category": self.test_category.name,
                "company": self.test_company.name,
                "quantity_in_stock": 500,
                "normal_price": "90.30",
            },
        )
        self.assertEqual(add_nutrition.status_code, 403)

    def test_normal_user_is_able_to_get_all(self) -> None:
        self.client.force_login(self.normal_user)

        get_all_nutritions = self.client.get(self.TEST_URL)

        self.assertEqual(len(get_all_nutritions.data), 2)
        self.assertEqual(get_all_nutritions.status_code, 200)

    def test_normal_user_is_able_to_retrieve_single(self) -> None:
        self.client.force_login(self.normal_user)
        test_product = Product.objects.create(
            name="Test Product_D",
            description="Test description",
            category=self.test_category,
            company=self.test_company,
            normal_price="90.30",
            quantity_in_stock=500,
        )

        get_test_product = self.client.get(f"{self.TEST_URL}{test_product.pk}/")

        self.assertEqual(get_test_product.status_code, 200)

    def test_normal_user_cant_update(self) -> None:
        self.client.force_login(self.normal_user)
        test_product = Product.objects.create(
            name="Test Product_Y",
            description="Test description",
            category=self.test_category,
            company=self.test_company,
            normal_price="90.30",
            quantity_in_stock=500,
        )

        put_to_product = self.client.put(f"{self.TEST_URL}{test_product.pk}/", {})

        self.assertEqual(put_to_product.status_code, 403)

    def test_normal_user_cant_delete(self) -> None:
        self.client.force_login(self.normal_user)
        test_product = Product.objects.create(
            name="Test Product_X",
            description="Test description",
            category=self.test_category,
            company=self.test_company,
            normal_price="90.30",
            quantity_in_stock=500,
        )

        product_to_delete = self.client.delete(f"{self.TEST_URL}{test_product.pk}/")

        self.assertEqual(product_to_delete.status_code, 403)
