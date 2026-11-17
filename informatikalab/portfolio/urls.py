from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio_index_view, name='index'),
    path('submission/<int:submission_id>/', views.submission_detail_view, name='submission_detail'),
    path('version/<int:version_id>/download/', views.download_submission_file, name='download_file'),
    path('version/<int:version_id>/feedback/', views.add_teacher_feedback_view, name='add_feedback'),
    path('submission/<int:submission_id>/reflection/', views.save_reflection_view, name='save_reflection'),
    path('submission/<int:submission_id>/compare/', views.compare_versions_view, name='compare_versions'),
]
