from django.db import models
from django.utils import timezone
from django.core.signing import TimestampSigner
from datetime import datetime, timedelta

from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager

# Create your models here.
class Article(models.Model):
    content = MarkdownxField()
    tags = TaggableManager(
        blank=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    view_count = models.IntegerField(
        default=0, 
    )
    question = models.BooleanField(
        blank=False,
        null=False,
    )

    # For answer articles

    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
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
    ip = models.CharField(
        max_length=16,
        default=None,
        null=True
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
    )
    contnent = models.CharField(
        max_length=160,
        blank=False,
        null=False,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
