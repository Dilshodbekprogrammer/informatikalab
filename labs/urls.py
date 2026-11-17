from django.urls import path
from . import views

app_name = 'labs'

urlpatterns = [
    path('', views.labs_index_view, name='index'),
    path('algorithms/', views.algorithms_lab_view, name='algorithms'),
    path('data/', views.data_lab_view, name='data_lab'),
    path('scratch/', views.scratch_lab_view, name='scratch'),
    path('crypto/', views.crypto_lab_view, name='crypto'),
    path('network/', views.network_lab_view, name='network'),
    path('sorting/', views.sorting_lab_view, name='sorting'),
    path('logic/', views.logic_lab_view, name='logic'),
    path('python/', views.python_lab_view, name='python'),
    path('api/save/', views.save_experiment_api, name='save_experiment_api'),
]
