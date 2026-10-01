from django.contrib import admin
from django.urls import path
from .views import home, login_user, logout_user, get_dealer_reviews, get_all_dealers, get_dealer_by_id, get_dealers_by_state, get_all_car_makes, analyze_review, review_dealer

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("djangoapp/login", login_user),
    path("djangoapp/logout", logout_user),
    path("dealer/<int:dealer_id>/reviews", get_dealer_reviews),
    path("fetchDealers", get_all_dealers),
    path("dealer/<int:dealer_id>", get_dealer_by_id),
    path("fetchDealers/<str:state>", get_dealers_by_state),
    path("carmakes", get_all_car_makes),
    path("analyze/<str:review_text>", analyze_review),
    path("dealer/<int:dealer_id>/review", review_dealer),
]