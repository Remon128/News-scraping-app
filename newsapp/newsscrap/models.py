from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.forms import CharField

# Create your models here.

# Website name - Website link - Created at - Last scraped at

class Website(models.Model):
    
    websiteName = models.CharField(max_length=1000)
    websiteLink = models.URLField(max_length=8000)
    createdAt   = models.DateField()
    lastScrappedAt = models.TimeField()

    def __str__(self):
        return 'website'


class Article(models.Model):

    website_ID   = models.ForeignKey(Website, on_delete=models.CASCADE, null=True)
    articleTitle = models.CharField(max_length=1000)
    articleDesc  = models.TextField(max_length=5000) 
    articleDOM   = models.TextField(max_length=10000) 
    articleLink  = models.URLField(max_length=1000)

    def __str__(self):
        return 'article'