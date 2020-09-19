from django.urls import path, re_path
from . import views
urlpatterns = [
	path('', views.home),
	re_path('^chat/$', views.chat),
	path('chat/<str:receiver_name>/', views.chat),
	path('login/', views.login),
	path('signup/', views.signup),
	path('showUsername/', views.show_username),
]