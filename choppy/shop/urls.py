from django.urls import path

from .views import shop_profile, shops_near_me

urlpatterns = [
    path("", shops_near_me, name="shops-near-me"),
    path("shop/<str:id>", shop_profile, name="shop-profile"),
]
