from django.urls import path
from . import views
from .views_auth import CustomLoginView, CustomSignupView, CustomLogoutView

urlpatterns = [
    path('', views.AdvertisementListView.as_view(), name='home'),
    path('my-ads/', views.UserAdvertisementListView.as_view(), name='my_ads'),
    path('admin-ads/', views.AdminAdvertisementListView.as_view(), name='admin_ads'),  # ✅ новый маршрут

    path('category/<slug:category_slug>/', views.CategoryAdvertisementListView.as_view(), name='category_ads'),
    path('tag/<slug:tag_slug>/', views.TagAdvertisementListView.as_view(), name='tag_ads'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tag/add/', views.TagCreateView.as_view(), name='add_tag'),
    path('cities/', views.CityListView.as_view(), name='city_list'),

    path('advertisement/new/', views.AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('advertisement/<slug:slug>/', views.AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('advertisement/<slug:slug>/update/', views.AdvertisementUpdateView.as_view(), name='advertisement_update'),
    path('advertisement/<slug:slug>/delete/', views.AdvertisementDeleteView.as_view(), name='advertisement_delete'),

    path('response/<int:pk>/', views.ResponseDetailView.as_view(), name='response_detail'),
    path('response/<int:pk>/accept/', views.ResponseAcceptView.as_view(), name='accept_response'),
    path('response/<int:pk>/reject/', views.ResponseRejectView.as_view(), name='reject_response'),
    path('advertisement/<slug:slug>/respond/', views.ResponseCreateView.as_view(), name='create_response'),

    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),

    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='account_logout'),
]
