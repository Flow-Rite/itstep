from django.urls import path
from . import views

urlpatterns = [
    path('', views.publication_list, name='publication_list'),
    path('<int:pk>/', views.publication_detail, name='publication_detail'),
    path('new/', views.publication_create, name='publication_create'),
    path('<int:pk>/edit/', views.publication_edit, name='publication_edit'),
    path('<int:pk>/delete/', views.publication_delete, name='publication_delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='profile'),
]
