from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.log_me_in, name='login'),
    path('logout', views.log_me_out, name='logout'),
    path('websites', views.websites, name='websites'),
    path('update_websites/<int:id>', views.update_websites, name='update_websites'),
    path('articles', views.articles, name='articles'),
]
