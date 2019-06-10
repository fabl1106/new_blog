from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from tagging.fields import TagField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, db_index=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return ('post:post_list_with_')

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, db_index=True)
    text = RichTextUploadingField(blank=True)

    material = models.FileField(upload_to='material/%Y/%m/%d', blank=True)
    tag = TagField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post:main')