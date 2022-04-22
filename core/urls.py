from . import views
from django.urls import path

urlpatterns = [
    path("", views.home_view, name='home'),
    path("login/", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),
    path('logout/', views.logout, name='logout'),
    path("tasks/new/", views.createTask.as_view(), name='create_task'),
    path('tasks/list/', views.listTasks.as_view(), name='list_tasks'),
    path('tasks/edit/<int:pk>/', views.updateTask.as_view(), name='edit_task'),
    path('tasks/view/<int:pk>/', views.detailTask.as_view(), name='view_task'),
    path('tasks/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path("tasks/pay/<int:pk>/", views.pay_task, name="pay_task"),
]
