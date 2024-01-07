"""
URL configuration for StudentPulse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from pulse.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base, name='base'),
    path('randomUser/', user, name='user'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('user_profile/', user_profile, name='user_profile'),
    path('create_lesson/', create_lesson, name='create_lesson'),
    path('lesson/<int:pk>/', lesson_detail, name='lesson_detail'),
    path('lesson/<int:pk>/create_review/', create_review, name='create_review'),
    path('custom_logout/', custom_logout, name='custom_logout'),
    path('lesson/<int:pk>/edit/', edit_lesson, name='edit_lesson'),
    path('lesson/<int:pk>/delete/', delete_lesson, name='delete_lesson'),
    path('review/<int:pk>/edit/', edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', delete_review, name='delete_review'),

]
