from django.contrib import admin
from .models import Artist, Song

# Register your models here.
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
	list_display = ('name_romaji', 'name_original')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
	list_display = ('title_romaji', 'artist')