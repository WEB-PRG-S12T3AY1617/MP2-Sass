from django.db import models
from users.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0)
    use = models.IntegerField(default=0) # For School or For Office
    course = models.CharField(max_length=8, null=True)
    picture = models.ImageField(upload_to='items/%Y/%m/%d/', default='items/default_item.jpg')

class Post(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)
    tags = models.TextField()

class Offer(models.Model):
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    offerFrom = models.ForeignKey(User, on_delete=models.CASCADE)
    offerPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='offerPost', null=True, blank=True)
    offerCash = models.PositiveIntegerField(default=0)
    message = models.TextField()
    date_offered = models.DateTimeField(auto_now=True)