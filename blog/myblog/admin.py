from django.contrib import admin
from .models import Post, Comment,IpModel,Topic
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(IpModel)
