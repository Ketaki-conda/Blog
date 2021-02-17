from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime,date
# Create your models here.

class IpModel(models.Model):
    ip=models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Topic(models.Model):
    topic_name = models.CharField(max_length = 255)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.topic_name

class Post(models.Model):
    title=models.CharField(max_length=255)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to ='images/',blank=True,null=True)
    body=models.TextField()
    post_date=models.DateField(auto_now_add=True)
    likes=models.ManyToManyField(IpModel,related_name="post_likes",blank=True)
    isFeatured = models.BooleanField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,default = 1)

    def __str__(self):
      return self.title + " - " + str(self.author)

    def get_absolute_url(self):
        return reverse('home')

    def number_of_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post= models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    body=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

