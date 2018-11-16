from django.urls import path, include

from matchingapp import views

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/updateProfile/', views.updateProfile, name='updateProfile'),
    path('profile/uploadNewProfileImage/', views.uploadNewProfileImage, name='uploadNewProfileImage'),
    path('administrator/', views.admin, name='administrator'),
    path('administrator/hobbies/', views.getHobbies, name='hobbyList'),
    path('administrator/addHobby/', views.addHobby, name='addHobby'),
    path('administrator/deleteHobby/', views.deleteHobby, name='deleteHobby'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('getUsers/', views.getUsers, name='getUsers'),
]
