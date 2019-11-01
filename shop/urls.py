from django.urls import path
from shop.views.cart import CartViewSet
from shop.views.cart_item import CartItemViewSet
from shop.views.category import CategoryViewSet
from shop.views.company import CompanyViewSet
from shop.views.health_check import health_check
from shop.views.product import ProductViewSet
from shop.views.review import ReviewViewSet
from shop.views.user import UserViewSet
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title="Shop API")

router = routers.SimpleRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"carts", CartViewSet)
router.register(r"cart_items", CartItemViewSet)
router.register(r"companies", CompanyViewSet)
router.register(r"products", ProductViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"users", UserViewSet)


urlpatterns = [path("health_check", health_check, name="health_check"), path(r"docs/", schema_view)]

urlpatterns += router.urls
