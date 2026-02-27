from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib import messages
from datetime import date, datetime, timedelta, time
from .utils import get_youtube_embed_url
import json

# Create your views here.

def get_current_program(request):
    """API endpoint to get the current live program based on current time"""
    try:
        current_time = datetime.now().time()
        current_day = date.today().isoweekday()
        
        # Get all active programs for today
        programs = Program.objects.filter(
            day__day=current_day,
            is_active=True
        ).order_by('start_time')
        
        # Find the program that is currently playing
        current_program = None
        for program in programs:
            if program.start_time <= current_time <= program.end_time:
                current_program = program
                break
        
        # If no program is currently playing, get the next upcoming program
        if not current_program:
            next_program = programs.filter(start_time__gt=current_time).first()
            if next_program:
                return JsonResponse({
                    'status': 'upcoming',
                    'title': next_program.title,
                    'host': next_program.host,
                    'start_time': next_program.start_time.strftime('%H:%M'),
                    'end_time': next_program.end_time.strftime('%H:%M'),
                    'description': next_program.description or '',
                    'image': next_program.image.url if next_program.image else None,
                })
            else:
                # Get first program of the day
                first_program = programs.first()
                if first_program:
                    return JsonResponse({
                        'status': 'later',
                        'title': first_program.title,
                        'host': first_program.host,
                        'start_time': first_program.start_time.strftime('%H:%M'),
                        'end_time': first_program.end_time.strftime('%H:%M'),
                        'description': first_program.description or '',
                        'image': first_program.image.url if first_program.image else None,
                    })
        
        if current_program:
            return JsonResponse({
                'status': 'live',
                'title': current_program.title,
                'host': current_program.host,
                'cohost': current_program.cohost,
                'start_time': current_program.start_time.strftime('%H:%M'),
                'end_time': current_program.end_time.strftime('%H:%M'),
                'description': current_program.description or '',
                'image': current_program.image.url if current_program.image else None,
                'guest': current_program.guest,
                'color': current_program.color,
            })
        else:
            return JsonResponse({
                'status': 'no_program',
                'message': 'No programs available'
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
def home(request):
    template_name="index.html"
    program = Program.objects.filter(day__day=date.today().isoweekday(), is_active=True).order_by('start_time')
    article = Article.objects.filter(status='published').order_by('-created_at')[:3]
    podcasts = PodcastShow.objects.filter(is_active=True).order_by('-created_at')[:4]
    
    # Get current program
    current_time = datetime.now().time()
    current_program = None
    program_status = 'no_program'
    
    for prog in program:
        if prog.start_time <= current_time <= prog.end_time:
            current_program = prog
            program_status = 'live'
            break
    
    # If no current program, get next upcoming
    if not current_program:
        next_prog = program.filter(start_time__gt=current_time).first()
        if next_prog:
            current_program = next_prog
            program_status = 'upcoming'
        else:
            # Get first program of the day
            first_prog = program.first()
            if first_prog:
                current_program = first_prog
                program_status = 'later'
    
    # Convert video URLs to embed format
    for podcast in podcasts:
        if podcast.video_url:
            podcast.embed_video_url = get_youtube_embed_url(podcast.video_url)
        else:
            podcast.embed_video_url = None
    context = {
        "programs": program,
        "articles": article,
        "podcasts": podcasts,
        "current_program": current_program,
        "program_status": program_status,
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
    selected_category = request.GET.get('category', None)
    podcasts = PodcastShow.objects.filter(is_active=True).order_by('-created_at')
    if selected_category:
        podcasts = PodcastShow.objects.filter(category=selected_category, is_active=True).order_by('-created_at')
    
    # Convert video URLs to embed format
    for podcast in podcasts:
        if podcast.video_url:
            podcast.embed_video_url = get_youtube_embed_url(podcast.video_url)
        else:
            podcast.embed_video_url = None
    
    podcategories = PodcastCategory.objects.all()
    context = {
        "podcasts": podcasts,
        "podcategories": podcategories,
        "selected_category": selected_category,
    }
    return render(request, template_name, context)
def community(request):
    template_name="community.html"
    return render(request, template_name)
def news(request):
    template_name="news.html"
    categories = Category.objects.all()
    selected_category = request.GET.get('category', None)
    
    articles = Article.objects.filter(status='published').order_by('-created_at')
    if selected_category:
        articles = articles.filter(category__name__iexact=selected_category)
    
    context = {
        "categories": categories,
        "articles": articles,
        "selected_category": selected_category,
    }
    return render(request, template_name, context)
def article_detail(request, pk):
    template_name = "article_detail.html"
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        content = request.POST['content']
        ArticleComment.objects.create(name=name, email=email, content=content, article_id=pk)
        messages.success(request, "Your comment has been submitted and is awaiting approval.")
        return redirect('article_detail', pk=pk)
    article = get_object_or_404(Article, pk=pk, status='published')
    comment = ArticleComment.objects.filter(article=article, is_approved=True).order_by('-created_at')
    article.views += 1
    article.save()
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(pk=article.pk).order_by('-created_at')[:6]

    trending_articles = Article.objects.filter(
        status='published'
    ).order_by('-views')[:5]

    context = {
        "article": article,
        "comments": comment,
        "related_articles": related_articles,
        "trending_articles": trending_articles,
    }
    return render(request, template_name, context)

def community(request):
    communities = Community.objects.filter(is_active=True)
    return render(request, 'community.html', {
        'podcasts': communities,  # keeps 'podcasts' so your template loop works
    })

def community_detail(request, pk):
    template_name = "community_detail.html"
    community = get_object_or_404(Community, pk=pk, is_active=True)
    context = {
        "community": community,
    }
    return render(request, template_name, context)

