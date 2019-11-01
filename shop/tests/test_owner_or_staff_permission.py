from shop.models.category import Category
from shop.models.company import Company
from shop.models.product import Product
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from shop.models.review import Review


class TestIsOwnerOrStaffPermission(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.TEST_URL = "/api/reviews/"

        cls.staff_tester = User.objects.create_user(
            username="Test Staff user", email="testowystaff@mail.pl", password="testuje", is_staff=True
        )

        cls.normal_user_owner = User.objects.create_user(
            username="Test Normal User", email="testowyuser@mail.pl", password="testuje"
        )

        cls.normal_user_not_owner = User.objects.create_user(
            username="Test Normal User1", email="testowyuse1r@mail.pl", password="testuje"
        )

        cls.test_category = Category.objects.create(name="Whey", description="Mmm bialeczko")

        cls.test_company = Company.objects.create(name="Test company", description="Test description")

        cls.test_product = Product.objects.create(
            name="Best Creatine",
            description="Best creatine ever",
            category=cls.test_category,
            company=cls.test_company,
            normal_price="90.30",
            quantity_in_stock=500,
        )

    def test_normal_user_can_use_post(self) -> None:
        self.client.force_login(self.normal_user_owner)

        post_review = self.client.post(
            f"{self.TEST_URL}", {"rate": 5, "opinion": "Great!", "product": self.test_product.name}
        )

        self.assertEqual(post_review.status_code, 201)

    def test_staff_user_can_use_post(self) -> None:
        self.client.force_login(self.staff_tester)

        post_review = self.client.post(
            f"{self.TEST_URL}", {"rate": 5, "opinion": "Great!", "product": self.test_product.name}
        )

        self.assertEqual(post_review.status_code, 201)

    def test_not_owner_cant_perform_not_safe_method(self) -> None:
        self.client.force_login(self.normal_user_not_owner)

        test_review = Review.objects.create(
            user=self.normal_user_owner, rate=5, opinion="Good enough", product=self.test_product
        )

        update_review = self.client.put(f"{self.TEST_URL}{test_review.pk}/", {})
        self.assertEqual(update_review.status_code, 403)

    def test_owner_can_perform_not_safe_method(self) -> None:
        self.client.force_login(self.normal_user_owner)

        test_review = Review.objects.create(
            user=self.normal_user_owner, rate=5, opinion="Good enough", product=self.test_product
        )

        delete_review = self.client.delete(f"{self.TEST_URL}{test_review.pk}/")
        self.assertEqual(delete_review.status_code, 204)

    def test_staff_user_can_perform_not_safe_method_on_someone_else_object(self) -> None:
        self.client.force_login(self.staff_tester)

        test_review = Review.objects.create(
            user=self.normal_user_owner, rate=5, opinion="Good enough", product=self.test_product
        )

        delete_review = self.client.delete(f"{self.TEST_URL}{test_review.pk}/")
        self.assertEqual(delete_review.status_code, 204)
