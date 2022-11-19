from django.contrib import admin
from .models import FollowersCount, Profile, Post, LikePost,FollowersCount,Orgsettings,Jobs

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Orgsettings)
admin.site.register(Jobs)

