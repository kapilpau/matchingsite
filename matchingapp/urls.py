from django.conf.urls import url
from django.urls import path
import django.views.static
from matchingapp import views
from matchingsite import settings

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    path('profile/', views.userProfile, name='profile'),
    path('profile/updateProfile/', views.updateProfile, name='updateProfile'),
    path('profile/uploadNewProfileImage/', views.uploadNewProfileImage, name='uploadNewProfileImage'),
    path('profile/<int:prof>/', views.profile, name='profile'),
    path('administrator/', views.admin, name='administrator'),
    path('administrator/hobbies/', views.getHobbies, name='hobbyList'),
    path('administrator/addHobby/', views.addHobby, name='addHobby'),
    path('administrator/deleteHobby/', views.deleteHobby, name='deleteHobby'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('getUsers/', views.getUsers, name='getUsers'),
    path('requestMatch/', views.requestMatch, name='getUsers'),
    path('matches/', views.matches, name='matches'),
    path('manageRequest/', views.manageRequest, name='matches'),
    path('deleteMatch/', views.deleteMatch, name='matches'),
    path('cancelRequest/', views.cancelRequest, name='matches'),
    path('messages/', views.messages, name='matches'),
    path('messages/<int:id>/', views.conversation, name='matches'),
    path('findConvo/<int:id>/', views.convoRedirect, name='convoRedirect'),
    path('findGroupChat/', views.findGroupChat, name='findGroupChat'),
    path('static/<str:appname>/<str:foldername>/<str:filename>', views.static, name='static'),
    path('media/<str:foldername>/<str:filename>', views.media, name='media'),
    path('media/favicon.ico', views.favicon, name='favicon'),
    path('saveNewPassword/', views.saveNewPassword, name='saveNewPassword')
]
