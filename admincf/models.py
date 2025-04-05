from django.db import models

class adminmusic(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'admin_table'
    
    def __str__(self):
        return self.username

# Create your models here.
