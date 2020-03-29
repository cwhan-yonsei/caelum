from django import forms
from django.forms.utils import ErrorList

from .models import Article, Comment

class ArticleCreationForm(forms.ModelForm):
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None, author=None, is_answer=None, parent=None):
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance, use_required_attribute=use_required_attribute, renderer=renderer)
        self.author = author
        self.is_answer = is_answer
        self.parent = parent

    class Meta:
        model = Article
        fields = ('content', 'tags',)

    def save(self, commit=True):
        article = super().save(commit=False)
        article.author = self.author
        if self.is_answer == True:
            article.is_answer = self.is_answer
            article.parent = self.parent
        if commit:
            article.save()
        return article

class CommentCreationForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'comment_content',
    }))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None, parant=None, author=None):
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance, use_required_attribute=use_required_attribute, renderer=renderer)
        self.parent = parant
        self.author = author

    class Meta:
        model = Comment
        fields = ('content',)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.parent = self.parent
        comment.author = self.author
        if commit:
            comment.save()
        return comment