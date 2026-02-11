from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from datetime import date, datetime, timedelta

# Create your views here.
def home(request):
    template_name="index.html"
    program = Program.objects.filter(day__day=date.today().isoweekday(), is_active=True).order_by('start_time')
    article = Article.objects.filter(status='published').order_by('-date')[:3]
    podcast = PodcastShow.objects.filter(is_active=True).order_by('-created_at')[:4]
    context = {
        "programs": program,
        "articles": article,
        "podcasts": podcast,
    }
    return render(request, template_name, context)

def about(request):
    template_name="about.html"
    return render(request, template_name)
def talent(request):
    template_name="talent.html"
    return render(request, template_name)
def contact(request):
    template_name="contact.html"
    if request.method == "POST":
        subject = request.POST['subject']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        ContactMessage.objects.create(name=name, email=email, phone=phone, message=message, subject=subject)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    return render(request, template_name)
def team(request):
    template_name="team.html"
    team = Team.objects.filter(is_active=True).order_by('order')
    context = {
        "team": team,
    }
    return render(request, template_name, context)
def blogs(request):
    template_name="blogs.html"    
    return render(request, template_name)

def podcast(request):
    template_name="podcast.html"
    podcasts = PodcastShow.objects.filter(is_active=True).order_by('-created_at')
    podcategories = PodcastCategory.objects.all()
    context = {
        "podcasts": podcasts,
        "podcategories": podcategories,
    }
    return render(request, template_name, context)
def community(request):
    template_name="community.html"
    return render(request, template_name)
def news(request):
    template_name="news.html"
    categories = Category.objects.all()
    articles = Article.objects.filter(status='published').order_by('-date')
    context = {
        "categories": categories,
        "articles": articles,
    }
    return render(request, template_name, context)
def article_detail(request, pk):
    template_name = "article_detail.html"
    article = get_object_or_404(Article, pk=pk, status='published')
    article.views += 1
    article.save()
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(pk=article.pk).order_by('-date')[:6]

    trending_articles = Article.objects.filter(
        status='published'
    ).order_by('-views')[:5]

    context = {
        "article": article,
        "related_articles": related_articles,
        "trending_articles": trending_articles,
    }
    return render(request, template_name, context)

def community(request):
    communities = Community.objects.filter(is_active=True)
    return render(request, 'community.html', {
        'podcasts': communities,  # keeps 'podcasts' so your template loop works
    })
