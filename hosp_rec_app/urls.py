from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordResetConfirmView
urlpatterns = [
    path('map', views.map_view, name='map_view'),
    path('map2', views.sym_map_view, name='sym_map_view'),
    path('', views.index, name='home'),
    path('contact',views.contact,name='contact'),
    path('search',views.search,name='search'),
    path('search_by_sym',views.search_by_sym,name='search_by_sym'),
    path('resp_received',views.response_received,name='response_sub'),
    path('preferences',views.preference,name='preferences'),
    path('schedules/', views.schedule, name='schedule'),
    path('direction/', views.direction, name='direction'),
    path('schedules/delete/<int:pk>/', views.remove, name='schedule_delete'),
    path('preferences/delete/<int:pk>/', views.pref_remove, name='preference_delete'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]






