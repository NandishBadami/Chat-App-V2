from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chat-app/<str:username>', views.chat_app, name='chat_app'),
    path('get_messages/<str:username>', views.get_messages, name='get_messages')
]