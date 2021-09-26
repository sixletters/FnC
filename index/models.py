from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
import datetime

class Photo(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField( max_length=300)
    created = models.DateField(auto_now_add=False, default=datetime.date.today ,editable=True)
    image = models.ImageField(upload_to='photos/')
    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title

