from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Website)
admin.site.register(models.Article)