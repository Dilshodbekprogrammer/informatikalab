from django.urls import path
from . import views

app_name = 'methods'

urlpatterns = [
    path('', views.methods_list_view, name='list'),
    path('<slug:slug>/', views.method_detail_view, name='detail'),
]
