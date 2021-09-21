from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class shortUrl(models.Model):
     original_url = models.URLField(blank=False)
     short_query = models.CharField(blank=False, max_length=8)
     visits = models.IntegerField(default=0) #how many times we have visited the website
     user = models.ForeignKey(User, on_delete=models.CASCADE) # 1 user can have many urls, thats why foreign key

