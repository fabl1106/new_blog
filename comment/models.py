from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
class Comment(models.Model):
    """
    1. 작성자
    2. 어떤 모델과의 관계가 있는지
    3. +작성자 x, ㅁ델과의 관계가 없을 떄

    """
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='my_comments')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    text = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add = True)