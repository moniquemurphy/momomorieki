from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.text import slugify
from .models import Artist, Song
from .helpers import SLUG_TO_ARTIST, SLUG_TO_SONG_TITLE

# Create your views here.
class IndexView(TemplateView):
    template_name = 'mainsite/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

class ArtistsView(TemplateView):

    template_name = 'mainsite/artists.html'

    def get_context_data(self, **kwargs):
        context = super(ArtistsView, self).get_context_data(**kwargs)
        artists = Artist.objects.all().order_by('name_romaji')

        artists_and_slugs = {}

        for artist in artists:
            # Convert to lower case and replace spaces with dashes so the artists' names can be used as slugs
            slug = slugify(artist.name_romaji)
            # Create a dictionary where artists' names are mapped to their slug counterparts
            # Example: {'Hamasaki Ayumi': 'hamasaki-ayumi'}
            artists_and_slugs[artist] = slug

        context['artists_and_slugs'] = artists_and_slugs

        return context

class SongListView(TemplateView):

    template_name = 'mainsite/songlist.html'

    def get_context_data(self, **kwargs):
        context = super(SongListView, self).get_context_data(**kwargs)
        # Convert the slug hyphen to a space to look it up in the db
        lookup_name = self.kwargs['slug'].replace('-', ' ')
        context['artist'] = lookup_name
        context['artist_slug'] = self.kwargs['slug']

        # Get all the song names for the artist
        songs = Song.objects.filter(artist__name_romaji__iexact=lookup_name)

        # There are a few artists this trick won't work for. They are special and get their own constants dictionary.
        if not songs:
            lookup_name = SLUG_TO_ARTIST[self.kwargs['slug']]
            songs = Song.objects.filter(artist__name_romaji=lookup_name)

        songs_and_slugs = {}

        for song in songs:
            slug = slugify(song.title_romaji)
            songs_and_slugs[song] = slug

        context['songs_and_slugs'] = songs_and_slugs

        return context

class LyricsView(TemplateView):

    template_name = 'mainsite/lyrics.html'

    def get_context_data(self, **kwargs):
        context = super(LyricsView, self).get_context_data(**kwargs)
        artist_name = self.kwargs['artist_slug'].replace('-', ' ')
        song_title = self.kwargs['song_slug'].replace('-', ' ')
        context['artist'] = artist_name
        context['song_title'] = song_title

        lyrics = Song.objects.filter(title_romaji__iexact=song_title)

        # There are a few songs this trick won't work for. They are special and get their own constants dictionary.
        if not lyrics:
            lookup_name = SLUG_TO_SONG_TITLE[self.kwargs['song_slug']]
            lyrics = Song.objects.filter(title_romaji=lookup_name)

        context['lyrics'] = lyrics

        return context

