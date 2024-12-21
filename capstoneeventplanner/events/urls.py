from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_event, name='create_event'),
    path('edit/<int:pk>/', views.edit_event, name='edit_event'),
    path('delete/<int:pk>/', views.delete_event, name='delete_event'),
]
