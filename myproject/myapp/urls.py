from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.player_list, name='player_list'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('search/', views.player_search, name='player_search'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
    path('player/new/', views.player_create, name='player_create'),
    path('player/<int:pk>/edit/', views.player_update, name='player_update'),
    path('player/<int:pk>/delete/', views.player_delete, name='player_delete'),
    path('player/<int:pk>/upload_cover/', views.upload_cover_image, name='upload_cover_image'),
]
