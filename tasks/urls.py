from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.TasksList.as_view()),
]