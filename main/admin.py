from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from main.models import *


class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1

    

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('day',)
    ordering = ('day',)

    inlines = [ProgramInline]

@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'status')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('author',)
    # exclude = ()
    summernote_fields = ('content',)
    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'author', None):
            obj.author = request.user
        obj.save()
    class Media:
        css = {
            'all': ('css/summernote_admin.css',)
        }

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'get_article_count')
    search_fields = ('name',)

admin.site.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')

admin.site.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    summernote_fields = ('content',)
    class Media:
        css = {
            'all': ('css/summernote_admin.css',)
        }

admin.site.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'order', 'is_active')
    search_fields = ('name', 'title')
    list_editable = ('order', 'is_active')

admin.site.register(PodcastCategory)
class PodcastCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'is_active', 'order')
    list_editable = ('icon', 'is_active', 'order')
    search_fields = ('name',)

admin.site.register(PodcastShow)
class PodcastShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')

admin.site.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title',)

admin.site.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')