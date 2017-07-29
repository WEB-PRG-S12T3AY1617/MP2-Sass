from django.db import models

# Create your models here.
class User(models.Model):
    choices = ((0, 'Student'), (1, 'Faculty Member'))
    name = models.CharField(null=False, max_length=150)
    email = models.EmailField(null=False, max_length=150)
    contact_num = models.CharField(null=True, max_length=150)
    password = models.CharField(null=False, max_length=150)
    salt = models.CharField(null=False, max_length=255)
    type = models.IntegerField(choices=choices, default=0)
    picture = models.ImageField(upload_to='users/%Y/%m/%d/', default='users/default_profile.png')
    date_created = models.DateTimeField(auto_now=True)