from django.urls import path
from . import views

urlpatterns = [
    path('process_number/', views.process_number, name='process_number'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('check_task_status/', views.check_task_status, name='check_task_status'),
    path('add/', views.add_task, name='add_task'),
    path('nginx_caller/', views.nginx_caller, name='nginx_caller'),
]
