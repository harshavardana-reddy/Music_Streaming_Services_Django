from django.db import models
import os

from django.core.files.storage import default_storage

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    dob = models.DateField()
    profile_image = models.ImageField(default="profile_images/default.jpg")

    def save(self, *args, **kwargs):
        # Delete the old image if it exists and is not the default image
        if self.pk:
            old_user = User.objects.get(pk=self.pk)
            if old_user.profile_image and old_user.profile_image != self.profile_image:
                if os.path.isfile(old_user.profile_image.path) and old_user.profile_image.name != "profile_images/default.jpg":
                    os.remove(old_user.profile_image.path)
        
        # If no image is provided, set the default image
        if not self.profile_image:
            self.profile_image = "profile_images/default.jpg"

        # Rename the uploaded file to userid.jpg
        if self.profile_image and self.profile_image.name != "profile_images/default.jpg":
            ext = os.path.splitext(self.profile_image.name)[1]  # Get file extension
            self.profile_image.name = f"profile_images/{self.user_id}{ext}"  # Rename to userid.jpg

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user_table'

    def __str__(self):
        return self.name
    
class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album_languages = {
        "TELUGU": "TELUGU",
        "HINDI": "HINDI",
        "ENGLISH": "ENGLISH",
        "TAMIL": "TAMIL",
        "MALAYALAM": "MALAYALAM",
        "KANNADA": "KANNADA"
    }
    album_language = models.CharField(max_length=50,choices=album_languages)
    music_tracks = models.ManyToManyField('Music', related_name='albums')
    album_image = models.ImageField(upload_to="music_images/album_images/")
    
    
    
    class Meta:
        db_table = 'album_table'
    
    def __str__(self):
        return f"{self.album_name} by {self.artist}"
    
    def save(self, *args, **kwargs):
        # Save the instance first to get the primary key
        super().save(*args, **kwargs)
        
        # Rename the image file to id.jpg
        if self.album_image:
            ext = os.path.splitext(self.album_image.name)[1]  # Get the file extension
            new_name = f"{self.album_id}{ext}"
            old_path = self.album_image.path
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            
            # Rename the file
            os.rename(old_path, new_path)
            
            # Update the image field
            self.album_image.name = os.path.join(os.path.dirname(self.album_image.name), new_name)
            super().save(*args, **kwargs)


class Music(models.Model):
    music_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    music_languages = {
        "TELUGU": "TELUGU",
        "HINDI": "HINDI",
        "ENGLISH": "ENGLISH",
        "TAMIL": "TAMIL",
        "MALAYALAM": "MALAYALAM",
        "KANNADA": "KANNADA"
    }
    music_language = models.CharField(max_length=50,choices=music_languages)
    music_file = models.FileField(upload_to='music_files/')
    music_image = models.ImageField(upload_to='music_images/music_images/')
    
    class Meta:
        db_table = 'music_table'
    
    def __str__(self):
        return f"{self.title} by {self.artist}"
    
    def save(self, *args, **kwargs):
        # Save the instance first to get the primary key
        super().save(*args, **kwargs)
        
        # Rename the music file to id.mp3
        if self.music_file:
            new_name = f"{self.music_id}.mp3"  # Force the extension to .mp3
            old_path = self.music_file.path
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            
            # Rename the file
            os.rename(old_path, new_path)
            
            # Update the music_file field
            self.music_file.name = os.path.join(os.path.dirname(self.music_file.name), new_name)
            super().save(*args, **kwargs)
        
        # Rename the image file to id.jpg
        if self.music_image:
            ext = os.path.splitext(self.music_image.name)[1]  # Get the file extension
            new_name = f"{self.music_id}{ext}"
            old_path = self.music_image.path
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            
            # Rename the file
            os.rename(old_path, new_path)
            
            # Update the image field
            self.music_image.name = os.path.join(os.path.dirname(self.music_image.name), new_name)
            super().save(*args, **kwargs)
            
class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    playlist_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    music_tracks = models.ManyToManyField(Music, related_name='playlists', blank=True)

    class Meta:
        db_table = 'playlist_table'
    def __str__(self):
        return f"{self.playlist_name} (User: {self.user.username})"
    
class UserOTPTable(models.Model):
    user_email = models.EmailField(primary_key=True)
    otp = models.CharField(max_length=6)
    
    class Meta:
        db_table = 'user_otp_table'
        
    def __str__(self):
        return self.user_email
    