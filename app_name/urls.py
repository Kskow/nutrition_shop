from django.urls import path
from app_name.views import health_check
from rest_framework import routers


router = routers.SimpleRouter()

urlpatterns = [path("health_check", health_check, name="health_check")]

urlpatterns += router.urls
