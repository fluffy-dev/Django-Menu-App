from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.index_view, name='main_page'),
    path('about/', views.about_view, name='about_page'),
    path('services/', views.services_view, name='services_page'),
    path(
        'services/<slug:service_slug>/',
        views.service_detail_view,
        name='service_detail_page'
    ),
]