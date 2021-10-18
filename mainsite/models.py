from django.db import models

class Artist(models.Model):
    name_original = models.TextField()
    name_romaji = models.TextField()

    def __str__(self):
        return self.name_romaji

class Song(models.Model):
    title_original = models.TextField()
    title_translated = models.TextField()
    title_romaji = models.TextField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    lyrics_original = models.TextField()
    lyrics_translated = models.TextField()
    lyrics_romaji = models.TextField()

    def __str__(self):
        return self.title_romaji