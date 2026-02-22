from django.urls import path
from . import views 

urlpatterns = [
    path('', views.chat, name='chat'), # Main endpoint for handling chat messages
    path('test/', views.test, name='test'), # Verifying that the backend server is running
]