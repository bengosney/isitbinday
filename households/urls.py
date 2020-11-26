# Django
from django.urls import include, path

# Third Party
from rest_framework import routers

# Locals
from . import api, views

router = routers.DefaultRouter()
router.register("household", api.householdViewSet)
router.register("member", api.memberViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("households/household/", views.householdListView.as_view(), name="households_household_list"),
    path("households/household/create/", views.householdCreateView.as_view(), name="households_household_create"),
    path("households/household/detail/<int:pk>/", views.householdDetailView.as_view(), name="households_household_detail"),
    path("households/household/update/<int:pk>/", views.householdUpdateView.as_view(), name="households_household_update"),
    path("households/member/", views.memberListView.as_view(), name="households_member_list"),
    path("households/member/create/", views.memberCreateView.as_view(), name="households_member_create"),
    path("households/member/detail/<int:pk>/", views.memberDetailView.as_view(), name="households_member_detail"),
    path("households/member/update/<int:pk>/", views.memberUpdateView.as_view(), name="households_member_update"),
)
