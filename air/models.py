from django.db import models
from django.utils import timezone
from django.core.signing import TimestampSigner
from datetime import datetime, timedelta

from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager

from accounts.models import User

import re

# Create your models here.
class Article(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    content = MarkdownxField()
    tags = TaggableManager(
        blank=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    hit_count = models.IntegerField(
        default=0, 
    )
    is_answer = models.BooleanField(
        default=False,
    )

    # For answer articles

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    accepted = models.BooleanField(
        default=False,
    )

    def get_title(self):
        return self.content.split('\n')[0].replace('#', '').strip()
    
    def get_content(self):
        return ''.join(self.content.split('\n')[1:])

    def get_preview(self):
        text = ''.join(self.content.split('\n')[1:])
        preview = re.sub('\!\[\]\(.+\)', '', text)
        preview = re.sub('\#+', '', preview)
        return(preview)

    def __str__(self):
        return self.get_title()

    class Meta:
        ordering = ['-date_created']



class ArticleHitCount(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        Article,
        default=None,
        null=True,
        on_delete=models.CASCADE
    )
    date = models.DateField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

class Comment(models.Model):
    parent = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        max_length=140,
        blank=False,
        null=False,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
