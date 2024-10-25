from django.urls import path

from .views import cut_detail

urlpatterns = [
    # path("", shops_near_me, name="shops-near-me"),
    path("<str:id>/", cut_detail, name="cut-detail"),
]
