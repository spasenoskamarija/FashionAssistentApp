from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('wardrobe/', views.wardrobe, name='wardrobe'),
    path('wardrobe/delete/<int:item_id>/', views.delete_clothing, name='delete_clothing'),

    path("suggest_outfit/", views.suggest_outfit, name="suggest_outfit"),
    path('delete-outfit/<int:outfit_id>/', views.delete_outfit, name='delete_outfit'),
    path('toggle-favorite/<int:outfit_id>/', views.toggle_favorite, name='toggle_favorite'),

]
