from django.urls import path, include
from . import views

urlpatterns = [
    path('userhome/',views.index,name='user_dashboard'),
    path('profile/',views.profile,name='profile'),
    path('viewalbums/',views.viewalbums,name='albums'),
    path('viewmusic/',views.viewmusic,name='musics'),
    path('musicplayer/',views.music_player,name='usermusicplayer'),
    path('createplaylist/',views.create_playlist,name='create_playlist'),
    path('viewplaylists/',views.view_playlist,name='view_playlists'),
    path('get_playlist_tracks/<int:playlist_id>/', views.get_playlist_tracks, name='get_playlist_tracks'),
    path('userprofile/',views.profile,name='userprofile'),
    path('update_profile_image',views.update_profile_image,name="update_profile_image"),
    path('update_profile',views.update_profile,name="update_profile"),
    path('logout/',views.logout,name='userlogout'),
]