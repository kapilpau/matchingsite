from django.urls import path, include

from matchingapp import views

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('administrator/', views.index, name='administrator'),
    path('login/', views.login, name='login'),
]
