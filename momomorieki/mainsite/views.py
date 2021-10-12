from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.text import slugify
from django.db.models.functions import Lower
from .models import Artist, Song
from .helpers import SLUG_TO_ARTIST, SLUG_TO_SONG_TITLE

class IndexView(TemplateView):

    template_name = 'mainsite/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

class TranslationsView(TemplateView):
    template_name = 'mainsite/translations.html'

class LanguageView(TemplateView):
    template_name = 'mainsite/language.html'

class ArtView(TemplateView):
    template_name = 'mainsite/art.html'

class GardenView(TemplateView):
    template_name = 'mainsite/garden.html'

class LinksView(TemplateView):
    template_name = 'mainsite/links.html'

class ArtistsView(TemplateView):

    template_name = 'mainsite/artists.html'

    def get_context_data(self, **kwargs):
        context = super(ArtistsView, self).get_context_data(**kwargs)
        artists = Artist.objects.all().order_by(Lower('name_romaji'))

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
        songs = Song.objects.filter(artist__name_romaji__iexact=lookup_name).order_by(Lower('title_romaji'))

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

        # Prep the artist name in romaji and the song title for display
        if self.kwargs['artist_slug'] in SLUG_TO_ARTIST:
            context['artist'] = SLUG_TO_ARTIST[self.kwargs['artist_slug']]
        else:
            context['artist'] = artist_name.title()

        if self.kwargs['song_slug'] in SLUG_TO_SONG_TITLE:
            context['song_title'] = SLUG_TO_SONG_TITLE[self.kwargs['song_slug']]
        else:
            context['song_title'] = song_title.title()

        print(context['artist'])
        print(context['song_title'])

        lyrics_query = Song.objects.filter(title_romaji__iexact=context['song_title']).filter(artist__name_romaji__iexact=context['artist'])
        lyrics = lyrics_query[0]

        context['lyrics'] = lyrics
        context['artist_slug'] = self.kwargs['artist_slug']

        return context

