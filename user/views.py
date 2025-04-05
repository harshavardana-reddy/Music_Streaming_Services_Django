from datetime import date
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import User,Music,Album,Playlist
from django.contrib import messages
from django.core.files.storage import default_storage
import json

def model_to_dict_serializable(instance):
    """Convert a model instance to a dictionary, handling date and image fields."""
    data = model_to_dict(instance)
    for key, value in data.items():
        if isinstance(value, date):
            # Convert date objects to ISO format strings
            data[key] = value.isoformat()
        elif hasattr(value, 'url'):
            # Convert ImageFieldFile or FileFieldFile to their URL or path
            data[key] = value.url  # Use the file's URL
    return data
def index(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    return render(request, 'user/index.html',{'user':user})

def profile(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    return render(request, 'user/userprofile.html',{'user':user})

def viewalbums(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    album_list = Album.objects.all()
    for album in album_list:
        # Construct the full URL for each track's music_file
        tracks = []
        for track in album.music_tracks.all():
            tracks.append({
                'title': track.title,
                'artist': track.artist,
                'music_file': request.build_absolute_uri(track.music_file.url)  # Full URL
            })
        album.track_list_json = json.dumps(tracks)  # Serialize to JSON
    return render(request, 'user/viewalbum.html',{'albums':album_list})

def viewmusic(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    music = Music.objects.all()
    return render(request, 'user/viewmusic.html',{'music':music})

def music_player(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    music_tracks = Music.objects.all()
    return render(request, 'user/musicplayer.html',{'music_tracks':music_tracks})

def create_playlist(request):
    if request.method == 'POST':
        playlist_name = request.POST.get('playlist_name')
        track_ids = request.POST.getlist('tracks')  # Get selected track IDs

        if not playlist_name:
            messages.error(request, 'Playlist name is required.')
            return redirect('view_playlists')

        # Retrieve the user dictionary from the session
        user = request.session.get('user')
        if not user or 'user_id' not in user:
            messages.error(request, 'User not authenticated.')
            return redirect('login')

        try:
            # Create the playlist
            playlist = Playlist.objects.create(
                playlist_name=playlist_name,
                user_id=user['user_id']  # Use the user_id from the session
            )

            # Add selected tracks to the playlist
            tracks = Music.objects.filter(music_id__in=track_ids)
            playlist.music_tracks.set(tracks)

            messages.success(request, f'Playlist "{playlist_name}" created successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

        return redirect('view_playlists')

def view_playlist(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    playlists = Playlist.objects.filter(user_id=user['user_id'])
    music_tracks = Music.objects.all()
    return render(request, 'user/playlist.html', {
        'playlists': playlists,
        'music_tracks': music_tracks,
        'base_url':"{0}://{1}".format(request.scheme, request.get_host())
        
    })
    
def get_playlist_tracks(request, playlist_id):
    playlist = Playlist.objects.get(playlist_id=playlist_id)
    tracks = playlist.music_tracks.all().values('music_id', 'title', 'artist', 'music_file', 'music_image')
    return JsonResponse({
        'playlist_name': playlist.playlist_name,
        'tracks': list(tracks)
    })

def logout(request):
    del request.session['user']
    return redirect('login')

def update_profile(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        dob = request.POST.get('dob')
        profile_image = request.FILES.get('profile_image')  # Get the uploaded file

        # Fetch the user object
        user_obj = User.objects.get(user_id=user['user_id'])

        # Update user fields
        user_obj.name = name
        user_obj.email = email
        user_obj.phone = phone
        user_obj.city = city
        user_obj.state = state
        user_obj.country = country
        user_obj.pincode = pincode
        user_obj.dob = dob

        # Handle profile image update
        if profile_image:
            # Delete the old image if it exists and is not the default image
            if user_obj.profile_image and user_obj.profile_image.name != "profile_images/default.jpg":
                if default_storage.exists(user_obj.profile_image.name):
                    default_storage.delete(user_obj.profile_image.name)
            
            # Save the new image
            user_obj.profile_image = profile_image

        # Save the updated user object
        user_obj.save()
        request.session['user'] = model_to_dict_serializable(user_obj)
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'user/profile.html')

def profile(request):
    user = request.session.get('user')
    # print(user['profile_image'])
    if not user:
        return redirect('login')
    return render(request, 'user/userprofile.html',{'user':user})

def update_profile_image(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')
    
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user_obj = User.objects.get(user_id=user['user_id'])
            user_obj.profile_image = profile_image
            user_obj.save()
            request.session['user'] = model_to_dict_serializable(user_obj)
            messages.success(request, 'Profile image updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'No image selected!')
    
    return render(request, 'user/updateprofileimage.html')
# Create your views here.
