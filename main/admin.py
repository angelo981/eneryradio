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

@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    list_display = ('description_preview', 'location', 'date', 'image', 'created_at')
    list_filter = ('date',)
    search_fields = ('Summary', 'location', 'content')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('title',)
    fieldsets = (
        ('Story details', {
            'fields': ('Summary', 'location', 'date'),
        }),
        ('Photo', {
            'fields': ('image',),
        }),
        ('Full story', {
            'fields': ('content',),
            'classes': ('collapse',),
        }),
        ('Record details', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    summernote_fields = ('content',)

    @admin.display(description='Description')
    def description_preview(self, obj):
        return obj.Summary[:120]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'Summary' and formfield:
            formfield.label = 'Description'
        return formfield

    def save_model(self, request, obj, form, change):
        if not obj.title:
            obj.title = obj.Summary[:200]
        super().save_model(request, obj, form, change)

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

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'position')
    list_editable = ('is_active', 'position')
    search_fields = ('title',)

admin.site.register(Advertisement, AdvertisementAdmin)

@admin.register(Community)
class CommunityAdmin(SummernoteModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'content')
    ordering = ('order', 'title')
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('description',)
    fieldsets = (
        ('Community details', {
            'fields': ('title', 'content', 'image'),
        }),
        ('Display settings', {
            'fields': ('is_active', 'order'),
        }),
        ('Record details', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    summernote_fields = ('content',)