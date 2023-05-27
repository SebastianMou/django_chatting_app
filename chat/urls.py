from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    
    path('inbox/', views.inbox, name='inbox'),
    path('directs/<str:username>/', views.directs, name='directs'),
    path('send_message_ajax/', views.send_message_ajax, name='send_message_ajax'),
    path('get_messages_ajax/<str:username>/', views.get_messages_ajax, name='get_messages_ajax'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<str:username>', views.profile, name='profile'),
]