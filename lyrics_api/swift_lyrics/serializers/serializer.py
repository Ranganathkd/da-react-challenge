"""
Serializers
"""
from rest_framework import serializers
from swift_lyrics.models import Lyric, Song, Album, Artist


class ArtistSerializer(serializers.ModelSerializer):
    """
    Class to serialize Artist.
    """

    class Meta:
        model = Artist
        fields = ['id', 'name', 'first_year_active']


class BaseAlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    year = serializers.IntegerField(required=True)

    class Meta:
        model = Album
        fields = ['id', 'name', 'year', 'artist']


class BaseSongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ['id', 'name']


class LyricSerializer(serializers.ModelSerializer):
    """
    Class to serialize Lyric.
    """
    class Meta:
        model = Lyric
        fields = ['id', 'text', 'votes']


class AlbumDetailSerializer(BaseAlbumSerializer):
    """
    Serialize list Album.
    """
    songs = BaseSongSerializer(many=True, read_only=True)

    class Meta(BaseAlbumSerializer.Meta):
        fields = BaseAlbumSerializer.Meta.fields + ['songs']


class SongSerializer(BaseSongSerializer):
    """
    Class to serialize Song.
    """
    album = BaseAlbumSerializer()

    class Meta(BaseSongSerializer.Meta):
        fields = BaseSongSerializer.Meta.fields + ['album']


class SongDetailSerializer(SongSerializer):
    """
    Serialize list Song.
    """
    lyrics = LyricSerializer(many=True, read_only=True)

    class Meta(SongSerializer.Meta):
        fields = SongSerializer.Meta.fields + ['lyrics']


class LyricDetailSerializer(LyricSerializer):
    """
    Serialize list Lyric.
    """
    song = BaseSongSerializer(read_only=True)
    album = BaseAlbumSerializer(source='song.album', read_only=True)

    def validate(self, data):
        song_id = self.initial_data.get('song', dict()).get('id', None)
        album_id = self.initial_data.get('album', dict()).get('id', None)
        print("album_id ==============", album_id)
        if not album_id:
            raise serializers.ValidationError("album.id is required")
        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            raise serializers.ValidationError(
                f"There is not album with the id={album_id}. Try another one.")

        if song_id:
            song = Song.objects.get(id=song_id)
            data['song'] = song
        else:

            song = self.initial_data.get('song', dict())
            song_name = song.get('name', None)

            if song_name:
                song = Song.objects.filter(name=song_name).first()
                if song is None:
                    song = Song(name=song_name, album=album)
                    song.save()
                data['song'] = song

        return super().validate(data)

    def create(self, validated_data):
        lyric = Lyric(**validated_data)
        lyric.save()
        return lyric

    class Meta(LyricSerializer.Meta):
        fields = LyricSerializer.Meta.fields + ['song', 'album']

class AlbumArtistSerializer(serializers.ModelSerializer):
    """
    Class to serialize album.
    """
    class Meta:
        model = Album
        fields = ['id', 'name']


class ArtistDetailSerializer(ArtistSerializer):
    """
    Serialize list albums.
    """
    albums = AlbumArtistSerializer(many=True, read_only=True)

    class Meta(ArtistSerializer.Meta):
        fields = ArtistSerializer.Meta.fields + ['albums']


class AlbumCreateSerializer(BaseAlbumSerializer):
    """
    Serializer to create endpoint for documentation.
    """

    artist_name = serializers.CharField(max_length=200, write_only=True)

    class Meta(BaseAlbumSerializer.Meta):
        fields = ['id', 'name', 'year', 'artist_name']

    def create(self, data):
        artist_name = data.pop("artist_name")
        artist, _ = Artist.objects.get_or_create(name=artist_name)
        data["artist"] = artist
        album = Album.objects.create(**data)
        return album
