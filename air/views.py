from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date

from .models import *
from .forms import *

# Create your views here.
@login_required
def index(request):
    user = request.user
    articles = Article.objects.filter(is_answer=False).all()
    context = {
        'user': user,
        'articles': articles,
    }
    return render(request, 'air/index.html', context)


@login_required
def article(request, pk):
    user = request.user
    article = get_object_or_404(Article, pk=pk)

    if article.is_answer == True:  # answer -> redirect to question
        question = article.parent
        return redirect('air:article', pk=question.pk)
    else:  # question
        answers = article.answers
        form = CommentCreationForm()
        context = {
            'user': user,
            'article': article,
            'answers': answers,
            'form': form,
        }
        try:
            return render(request, 'air/article.html', context)
        finally:
            hit_logs = ArticleHitCount.objects.filter(
                user=user,
                article=article,
                date__lte=date.today(),
                date__gte=date.today()
            )
            if hit_logs.count() == 0:
                hits = ArticleHitCount(user=user, article=article)
                hits.save()
                article.hit_count += 1
                article.save()


@login_required
def question(request):
    user = request.user
    if request.method == 'POST':
        form = ArticleCreationForm(
            request.POST,
            author=user,
            is_answer=False,
        )
        if form.is_valid():
            article = form.save()
            return redirect('air:article', pk=article.pk)

    elif request.method == 'GET':
        form = ArticleCreationForm()
        context = {
            'user': user,
            'form': form,
        }
        return render(request, 'air/question.html', context)


@login_required
def answer(request, pk):
    user = request.user
    question = Article.objects.get(pk=pk)

    if request.method == 'POST':
        form = ArticleCreationForm(
            request.POST,
            author=user,
            is_answer=True,
            parent=question,
        )
        if form.is_valid():
            article = form.save()
            return redirect('air:article', pk=article.pk)

    elif request.method == 'GET':
        form = ArticleCreationForm()
        context = {
            'user': user,
            'form': form,
            'question': question,  # nec?
        }
        return render(request, 'air/answer.html', context)

# edit article
@login_required
def edit_article(request, pk):
     user = request.user
     article = Article.objects.get(pk=pk)

     if request.method == 'POST':
          form = ArticleCreationForm(request.POST)
          if form.is_valid():
               article.content = form.cleaned_data['content']
               article.tags = form.cleaned_data['tags']
               article.save()
               return redirect('air:article', pk=article.pk)

     elif request.method == "GET":
          if article.author == user:
               if article.is_answer:
                    form = ArticleCreationForm(instance=article)
                    context = {
                         'user': user,
                         'form': form,
                         'question': article.parent,
                    }
                    return render(request, 'air/answer.html', context)
               else:
                    form = ArticleCreationForm(instance=article)
                    context = {
                         'user': user,
                         'form': form,
                    }
                    return render(request, 'air/question.html', context)
          else:
               context = {
                    'title': "Error :(",
                    'content': "You don't have authorization to finish that action.",
                    'confirm': 'back',
                    }
               return render(request, 'accounts/message.html', context)


@login_required
def del_article(request, pk):
    if request.method == 'POST':
        article = Article.objects.get(pk=pk)
        if (article.author == request.user) or request.user.is_admin:
            article.delete()
            return redirect('air:index')
        else:
            context = {
                'title': "Error :(",
                'content': "You don't have authorization to finish that action.",
                'confirm': 'back',
            }
            return render(request, 'accounts/message.html', context)


@login_required
def comment(request, pk):
    if request.method == 'POST':
        user = request.user
        article = Article.objects.get(pk=pk)
        form = CommentCreationForm(
            request.POST,
            parant=article,
            author=user,
        )
        if form.is_valid():
            comment = form.save()
            return redirect('air:article',  pk=article.pk)

@login_required
def del_comment(request, pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=pk)
        if (comment.author == request.user) or request.user.is_admin:
            pk = comment.parent.pk
            comment.delete()
            return redirect('air:article',  pk=pk)
        else:
            context = {
                'title': "Error :(",
                'content': "You don't have authorization to finish that action.",
                'confirm': 'back',
            }
            return render(request, 'accounts/message.html', context)
