from django.urls import path, include
from . import views
urlpatterns = [
    path('adminhome/',views.index,name="admin_dashboard"),
    path('addmusic/', views.add_music, name='addmusic'),
    path('addalbum/', views.add_album, name='addalbum'),
    path('viewmusic/', views.view_music, name='viewmusic'),
    path('viewalbum/', views.view_album, name='viewalbum'),
    path('viewusers/', views.view_users, name='viewusers'),
    path('musicplayer/', views.music_player, name='musicplayer'),
    path('editalbum/<int:album_id>/', views.edit_album, name='edit_album'),
    path('logout/',views.logout,name="adminlogout")
]