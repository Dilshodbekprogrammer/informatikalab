from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('', views.lessons_list_view, name='list'),
    path('student/', views.student_lessons_view, name='student_lessons'),
    path('create/', views.lesson_create_view, name='create'),
    path('<int:lesson_id>/', views.lesson_detail_view, name='detail'),
    path('<int:lesson_id>/edit/', views.lesson_edit_view, name='edit'),
    path('<int:lesson_id>/duplicate/', views.lesson_duplicate_view, name='duplicate'),
    path('<int:lesson_id>/print/', views.lesson_print_view, name='print'),
]
