from django.contrib import admin

from game_site_api.models import User, ProfilePic, Post, PostPic, PostComent


admin.site.register(User)
admin.site.register(ProfilePic)
admin.site.register(Post)
admin.site.register(PostPic)
admin.site.register(PostComent)

