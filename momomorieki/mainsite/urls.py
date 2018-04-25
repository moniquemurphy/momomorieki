from django.urls import path

from .views import IndexView, ArtistsView, SongListView, LyricsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('artists', ArtistsView.as_view(), name='artists'),
    path('artists/<slug:slug>', SongListView.as_view(), name='songlist'),
    path('artists/<slug:artist_slug>/<slug:song_slug>', LyricsView.as_view(), name='lyrics')
]
