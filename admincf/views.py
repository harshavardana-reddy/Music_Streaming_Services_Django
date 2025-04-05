import json
from django.shortcuts import render,redirect,get_object_or_404
from admincf.models import adminmusic
from user.models import Music,Album
from django.contrib import messages
from django.core.serializers import serialize

def index(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    return render(request, 'admincf/index.html',{'admin':admin['username']})

def add_music(request):
    # Define music languages
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    music_languages = {
        "TELUGU": "TELUGU",
        "HINDI": "HINDI",
        "ENGLISH": "ENGLISH",
        "TAMIL": "TAMIL",
        "MALAYALAM": "MALAYALAM",
        "KANNADA": "KANNADA"
    }

    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        music_file = request.FILES.get('music_file')  # Get the uploaded music file
        music_image = request.FILES.get('music_image')  # Get the uploaded image file
        music_language = request.POST.get('music_language')  # Get the selected music language

        
        # Validate form data
        if not title or not artist or not music_file or not music_image or not music_language:
            messages.error(request, 'All fields are required.')
            return redirect('addmusic')

        # Create and save the Music instance
        try:
            music = Music(
                title=title,
                artist=artist,
                music_file=music_file,
                music_image=music_image,
                music_language=music_language  # Add the language field
            )
            music.save()  # Save the instance to the database
            messages.success(request, 'Music added successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

        return redirect('addmusic')

    return render(request, 'admincf/addmusic.html', {'music_languages': music_languages})

def add_album(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    album_languages = {
        "TELUGU": "TELUGU",
        "HINDI": "HINDI",
        "ENGLISH": "ENGLISH",
        "TAMIL": "TAMIL",
        "MALAYALAM": "MALAYALAM",
        "KANNADA": "KANNADA"
    }
    if request.method == 'POST':
        # Get form data
        album_name = request.POST.get('album_name')
        artist = request.POST.get('artist')
        music_track_ids = request.POST.get('music_tracks', '').split(',')
        album_image = request.FILES.get('album_image')  # Get the uploaded image file
        album_language = request.POST.get('album_language')
        
        # Validate form data
        if not album_name or not artist or not album_image:
            messages.error(request, 'Album name, artist, and image are required.')
            return redirect('addalbum')

        # Create the album
        album = Album(
            album_name=album_name,
            artist=artist,
            album_image=album_image,  # Save the uploaded image
            album_language=album_language
        )
        album.save()
        # Add selected music tracks to the album
        for track_id in music_track_ids:
            if track_id:  # Ensure the track_id is not empty
                try:
                    music_track = Music.objects.get(music_id=track_id)
                    album.music_tracks.add(music_track)
                except Music.DoesNotExist:
                    messages.warning(request, f'Music track with ID {track_id} does not exist.')

        messages.success(request, 'Album added successfully!')
        return redirect('addalbum')

    # Fetch all music tracks for the form
    music_tracks = Music.objects.all()
    return render(request, 'admincf/addalbum.html', {
    'music_tracks': music_tracks,
    'album_languages': album_languages
    })

def view_music(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    music_list = Music.objects.all()
    return render(request, 'admincf/viewmusic.html',{'music_list': music_list})

from django.template.defaultfilters import filesizeformat

def view_album(request):
    admin = request.session.get('admin')
    if not admin:
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
    return render(request, 'admincf/viewalbum.html', {'album_list': album_list})

def view_users(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    return render(request, 'admincf/viewusers.html')


def music_player(request):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    # Fetch all music tracks from the database
    music_tracks = Music.objects.all()
    return render(request, 'admincf/musicplayer.html', {'music_tracks': music_tracks})

def edit_album(request, album_id):
    admin = request.session.get('admin')
    if not admin:
        return redirect('login')
    album = get_object_or_404(Album, album_id=album_id)
    all_tracks = Music.objects.all()  # Fetch all tracks for the "Add Track" dropdown

    if request.method == 'POST':
        
        # Handle adding a track
        if 'add_track' in request.POST:
            track_ids = request.POST.get('track_ids')  # Get the selected track IDs
            if track_ids:
                track_ids = track_ids.split(',')  # Split the comma-separated IDs
                for track_id in track_ids:
                    track = get_object_or_404(Music, music_id=track_id)
                    album.music_tracks.add(track)
                messages.success(request, 'Tracks added to the album.')
            else:
                messages.error(request, 'No tracks selected.')

        # Handle deleting a track
        elif 'delete_track' in request.POST:
            track_id = request.POST.get('track_id')
            track = get_object_or_404(Music, music_id=track_id)
            album.music_tracks.remove(track)
            messages.success(request, f'Track "{track.title}" removed from the album.')

        return redirect('edit_album', album_id=album_id)

    return render(request, 'admincf/editalbum.html', {
        'album': album,
        'all_tracks': all_tracks,
    })

def logout(request):
    del request.session['admin']
    return redirect('login')
# Create your views here.
