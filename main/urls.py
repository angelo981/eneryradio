from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('talent', views.talent, name="talent"),
    path('contact', views.contact, name="contact"),
    path('team', views.team, name="team"),
    path('blogs', views.blogs, name="blogs"),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('podcast', views.podcast, name="podcast"),
    path('community', views.community, name="community"),
    path('news', views.news, name="news"),
    path('community_detail/<int:pk>/', views.community_detail, name='community_detail'),
    path('api/current-program/', views.get_current_program, name='get_current_program'),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )