from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tracks/', views.circuits, name='circuits'),
    path('statistics/', views.statistics, name='statistics'),
    path('teams/', views.teams, name='teams'),
    path('teams/<slug:team_slug>/', views.team_detail, name='team_detail'),
    path('drivers/<slug:driver_slug>/', views.driver_detail, name='driver_detail'),
    path('authorize/', views.authorize, name='authorize'),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("logout/", views.logout, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)