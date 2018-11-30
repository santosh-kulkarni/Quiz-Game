from django.urls import path

from . import views

urlpatterns = [
    path('show-question/', views.show_question, name="show_question"),
    path('', views.first_page, name='index'),
]
