from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.projects_index_view, name='index'),
    path('<int:project_id>/', views.project_detail_view, name='detail'),
    path('<int:project_id>/assign/', views.assign_project_view, name='assign'),
    path('assignment/<int:assignment_id>/', views.assignment_detail_view, name='assignment_detail'),
    path('assignment/<int:assignment_id>/group/create/', views.group_create_view, name='group_create'),
    path('assignment/<int:assignment_id>/step/<int:step_id>/submit/', views.submit_lesson_step_view, name='submit_step'),
]
