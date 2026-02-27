from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Day(models.Model):
    days_of_week = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    ]

    day = models.CharField(max_length=10, choices=days_of_week)

    class Meta:
        verbose_name = "Day"
        verbose_name_plural = "Days"
        ordering = ['day']

    def __str__(self):
        return f"{self.get_day_display()}"
    
class Program(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='programs', verbose_name="Day")
    title = models.CharField(max_length=200, verbose_name="Program Title")
    image = models.ImageField(upload_to='programs/', blank=True, null=True, verbose_name="Program Image")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    host = models.CharField(max_length=100, blank=True, null=True, verbose_name="Main Host")
    cohost = models.CharField(max_length=100, blank=True, null=True, verbose_name="Co-Host")
    guest = models.CharField(max_length=200, blank=True, null=True, verbose_name="Guest")
    color = models.CharField(max_length=7, blank=True, null=True, verbose_name="Color (hex)", help_text="Format: #4facfe")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"
        ordering = ['day__day', 'order', 'start_time']

    def __str__(self):
        return f"{self.day.get_day_display()} - {self.title} ({self.start_time} - {self.end_time})"
    
class Category(models.Model):
   
    name = models.CharField(max_length=100, verbose_name="name")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Article Category"
        verbose_name_plural = "Article Categories"
        ordering = ['name']
   
    def __str__(self):
        return self.name
   
    def get_article_count(self):
        return self.articles.count()

class Article(models.Model):
    STATUS_CHOICES = [
        ('published', 'Published'),
        ('draft', 'Draft'),
        ('archived', 'Archived'),
    ]
   
    title = models.CharField(max_length=200, verbose_name="Title")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name="Category")
    excerpt = models.TextField(blank=False, null=False, verbose_name="Sub content")
    content = models.TextField(blank=False, null=False, verbose_name="Full Content")
    image = models.ImageField(upload_to='articles/', blank=False, null=False, verbose_name="Cover Image")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Status")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False, related_name='articles', verbose_name="Author")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-created_at']
   
    def __str__(self):
        return self.title

class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="Article")
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    is_approved = models.BooleanField(default=True, verbose_name="Approved")
    content = models.TextField(verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        verbose_name = "Article Comment"
        verbose_name_plural = "Article Comments"
        ordering = ['-created_at']
   
    def __str__(self):
        return f"Comment by {self.name} on {self.article.title}"

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nouveau'),
        ('read', 'Lu'),
        ('replied', 'Répondu'),
        ('archived', 'Archivé'),
    ]
   
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']
   
    def __str__(self):
        return f"{self.name} - {self.subject}"
   
    @property
    def full_name(self):
        return f"{self.name}"
    
class PodcastCategory(models.Model):
    CATEGORY_CHOICES = [
        ('talk', 'Talk Show'),
        ('music', 'Music & Culture'),
        ('sports', 'Sports'),
        ('interview', 'Interviews'),
        ('dj', 'DJ Mixes'),
    ]
   
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True, verbose_name="Category Name")
    icon = models.CharField(max_length=50, default="fas fa-podcast", verbose_name="FontAwesome Icon", help_text="e.g., fas fa-comments")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Podcast Category"
        verbose_name_plural = "Podcast Categories"
        ordering = ['order', 'name']
   
    def __str__(self):
        return self.get_name_display()


class PodcastShow(models.Model):
    BADGE_CHOICES = [
        ('new', 'NEW'),
        ('weekly', 'WEEKLY'),
        ('featured', 'FEATURED'),
        ('none', 'None'),
    ]
   
    title = models.CharField(max_length=200, verbose_name="Show Title")
    category = models.ForeignKey(PodcastCategory, on_delete=models.SET_NULL, null=True, related_name='shows', verbose_name="Category")
    description = models.TextField(verbose_name="Description")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL", help_text="Link to YouTube/Vimeo or embedded video")
    audio_url = models.URLField(verbose_name="Audio File URL", help_text="Link to MP3/audio file")
    guest = models.CharField(max_length=200, blank=True, null=True, verbose_name="Guest(s)")
    host = models.CharField(max_length=100, blank=True, null=True, verbose_name="Host")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    order = models.IntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Podcast Show"
        verbose_name_plural = "Podcast Shows"
        ordering = ['order', '-created_at']
   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    @property
    def image_url(self):
        """Return image URL or default image"""
        if self.image:
            return self.image.url
        return '/static/images/default-podcast.jpg'
   
    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    Summary = models.TextField(verbose_name="Summary")
    content = models.TextField(blank=True, null=True, verbose_name="Content")
    image = models.ImageField(upload_to='blogs/', blank=True, null=True, verbose_name="Image")
    date = models.DateField(default=timezone.now, verbose_name="Publication Date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ['-date', '-created_at']
   
    def __str__(self):
        return self.title
   
    @property
    def image_src(self):
        """Retourne l'URL de l'image (uploadée ou URL externe)"""
        try:
            if self.image and hasattr(self.image, 'name') and self.image.name:
                return self.image.url
        except (ValueError, AttributeError):
            pass
       
        if self.image_url:
            # Si c'est un chemin relatif (ne commence pas par http), utiliser static
            if not self.image_url.startswith('http'):
                from django.templatetags.static import static
                return static(self.image_url)
            return self.image_url
        return ''
   




class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    title = models.CharField(max_length=200, verbose_name="Title/Function")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(upload_to='teams/', blank=True, null=True, verbose_name="Photo")
    whatsapp_url = models.URLField(blank=True, null=True, verbose_name="WhatsApp")
    instagram_url = models.URLField(blank=True, null=True, verbose_name="Instagram")
    order = models.IntegerField(default=0, verbose_name="Order of Display")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['order', 'name']
   
    def __str__(self):
        return f"{self.name} - {self.title}"
   
    @property
    def image_src(self):
        """Retourne l'URL de l'image (uploadée ou URL externe)"""
        if self.image:
            return self.image.url
        return self.image_url or ''
    
class Advertisement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Ad Title")
    image = models.ImageField(upload_to='ads/', blank=True, null=True, verbose_name="Ad Image")
    image_url = models.URLField(blank=True, null=True, verbose_name="Image URL")
    link_url = models.URLField(blank=True, null=True, verbose_name="Link URL", help_text="Where ad redirects when clicked")
    position = models.IntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"
        ordering = ['position', '-created_at']
   
    def __str__(self):
        return self.title

class Community(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('new', 'New'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Cammunity Title")
    description = models.TextField(verbose_name="SubContent")
    content = models.TextField(blank=True, null=True, verbose_name="Content")
    image = models.ImageField(upload_to='Cammunity/', verbose_name="Cammunity Image")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    order = models.IntegerField(default=0, verbose_name="Order of Display")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name = "Community"
        verbose_name_plural = "Communities"
        ordering = ['title', '-created_at']
   
    def __str__(self):
        return self.title
