from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-record/', views.add_record, name='add_record'),
    path('record/<str:pk>/', views.customer_record, name='record'),
    path('update-record/<str:pk>/', views.update_record, name='update'),
    path('delete-record/<str:pk>/', views.delete_record, name='delete'),

    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

]
