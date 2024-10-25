from django.urls import path

from .views import handle_oauth, initiate_oauth

urlpatterns = [
    # path("", shops_near_me, name="shops-near-me"),
    path("", initiate_oauth, name="auth"),
    path("authenticate", handle_oauth, name="handle-auth"),
]
