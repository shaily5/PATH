from django.contrib import admin
from .models import CustomUser
from .models import Post

admin.site.register(CustomUser)
admin.site.register(Post)

