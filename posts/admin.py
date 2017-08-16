from django.contrib import admin

# Register your models here.
from posts.models import Post, Offer, Item

admin.site.register(Item)
admin.site.register(Post)
admin.site.register(Offer)