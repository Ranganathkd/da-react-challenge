"""
Models
"""

from django.db import models
from voting.models import Vote


class Artist(models.Model):
    """
    Artist Model.
    """
    name = models.CharField(max_length=128, unique=True)
    first_year_active = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    """
    Album Model
    """
    name = models.TextField(
        blank=False,
        db_index=True,
        unique=True,
        help_text="Album name - can alternatively use 'id' field set to id of existing album when creating new lyrics")
    year = models.PositiveIntegerField(null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, related_name="albums")

    # objects = models.Manager()
    def __str__(self):
        return self.name


class Song(models.Model):
    """
    Song Model
    """
    name = models.TextField(
        blank=False,
        db_index=True,
        unique=True,
        help_text="Song name - can alternatively use 'id' field set to id of existing song when creating new lyrics")

    album = models.ForeignKey(
        Album,
        related_name='songs',
        null=True,
        on_delete=models.CASCADE,
        help_text="Album")

    # objects = models.Manager()
    def __str__(self):
        return self.name


class Lyric(models.Model):
    """
    Lyric Model
    """
    text = models.TextField(
        blank=False,
        db_index=True,
        help_text="Lyrics from a song/album")

    song = models.ForeignKey(
        Song,
        related_name='lyrics',
        null=True,
        on_delete=models.CASCADE,
        help_text="Song")

    votes = models.IntegerField(
        default=0
    )

    # objects = models.Manager()
    def save(self, **kwargs):
        super().save(**kwargs)

    def vote(self, user, score):
        Vote.objects.record_vote(self, user, score)
        self.votes = Vote.objects.get_score(self)['score']
        self.save()