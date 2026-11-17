from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('classrooms/', views.classrooms_list_view, name='classrooms'),
    path('classrooms/<int:class_id>/', views.classroom_detail_view, name='classroom_detail'),
    path('classrooms/<int:class_id>/add-student/', views.classroom_add_student_view, name='classroom_add_student'),
    
    # Admin: foydalanuvchilar boshqaruvi
    path('users/', views.users_list_view, name='users_list'),
    path('users/add-teacher/', views.add_teacher_view, name='add_teacher'),
    path('users/add-student/', views.add_student_view, name='add_student'),
    path('users/<int:user_id>/edit/', views.edit_user_view, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
]
