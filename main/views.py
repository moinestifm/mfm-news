from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from .models import News, Category, Comment
from .forms import CommentForm
from better_profanity import profanity

def clean_comment(comment):
    cleaned_comment = profanity.censor(comment)
    return cleaned_comment

def home(request):
    first_news = News.objects.filter(is_featured=True).first()

    if not first_news:
        first_news = News.objects.first()

    three_news = News.objects.exclude(id=first_news.id).all()[:3]
    three_categories = Category.objects.all()[:3]

    return render(request, 'home.html', {
        'first_news': first_news,
        'three_news': three_news,
        'three_categories': three_categories
    })

def all_news(request):
    all_news = News.objects.all()
    return render(request, 'all-news.html', {
        'all_news': all_news
    })

def article(request, id):
    news = News.objects.get(pk=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']

            cleaned_comment = clean_comment(comment)

            time_limit = now() - timedelta(minutes=5)
            recent_comments = Comment.objects.filter(email=email, news=news, created_at__gt=time_limit)
            if recent_comments.exists():
                messages.error(request, "You have recently submitted a comment. Please wait before posting another.")
                return redirect('article', id=id)

            Comment.objects.create(
                news=news,
                name=name,
                email=email,
                comment=cleaned_comment,
                status=False
            )
            messages.success(request, 'Comment sent!')

        else:
            messages.error(request, 'There was an error in sending your comment.')

    else:
        form = CommentForm()

    category = Category.objects.get(id=news.category.id)
    rel_news = News.objects.filter(category=category).exclude(id=id)
    comments = Comment.objects.filter(news=news, status=True).order_by('-id')

    return render(request, 'article.html', {
        'news': news,
        'related_news': rel_news,
        'comments': comments,
        'form': form 
    })

def all_category(request):
    cats = Category.objects.all()
    return render(request, 'category.html', {
        'cats': cats
    })

def category(request, id):
    category = Category.objects.get(id=id)
    news = News.objects.filter(category=category)
    return render(request, 'category-news.html', {
        'all_news': news,
        'category': category
    })
