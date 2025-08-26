from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdvertisementListView.as_view(), name='home'),
    path('my-ads/', views.UserAdvertisementListView.as_view(), name='my_ads'),
    path('category/<slug:category_slug>/', views.CategoryAdvertisementListView.as_view(), name='category_ads'),  # Новый маршрут
    path('advertisement/new/', views.AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('advertisement/<slug:slug>/', views.AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('advertisement/<slug:slug>/update/', views.AdvertisementUpdateView.as_view(), name='advertisement_update'),
    path('advertisement/<slug:slug>/delete/', views.AdvertisementDeleteView.as_view(), name='advertisement_delete'),

    path('response/<int:pk>/', views.ResponseDetailView.as_view(), name='response_detail'),
    path('response/<int:pk>/accept/', views.accept_response, name='accept_response'),
    path('response/<int:pk>/reject/', views.reject_response, name='reject_response'),
    path('advertisement/<slug:slug>/respond/', views.create_response, name='create_response'),

    path('profile/<str:username>/', views.profile_view, name='profile'),
]
