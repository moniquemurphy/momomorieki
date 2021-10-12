from django.urls import path

from .views import IndexView, ArtistsView, SongListView, LyricsView, TranslationsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('translations', TranslationsView.as_view(), name='translations'),
    path('translations/lyrics/artists', ArtistsView.as_view(), name='artists'),
    path('translations/lyrics/artists/<slug:slug>', SongListView.as_view(), name='songlist'),
    path('translations/lyrics/artists/<slug:artist_slug>/<slug:song_slug>', LyricsView.as_view(), name='lyrics')
]
