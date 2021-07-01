"""
All view classes
"""


from rest_framework import mixins, filters, viewsets
from rest_framework.response import Response
from django_filters import rest_framework
from django.http import HttpResponse, Http404
from django.views import View
# Create your views here.
from swift_lyrics.models import Lyric, Album, Song, Artist
from swift_lyrics.serializers.serializer import BaseAlbumSerializer, \
    AlbumDetailSerializer, AlbumCreateSerializer, SongDetailSerializer, \
    SongSerializer, LyricDetailSerializer, ArtistSerializer, ArtistDetailSerializer


class HealthCheckView(View):
    """
    Checks to see if the site is healthy.
    """
    @staticmethod
    def get(request, *args, **kwargs):
        return HttpResponse("ok")


class AlbumIndex(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """
    This view class automatically provides `list` and `retrieve` actions for Album.
    """
    queryset = Album.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AlbumDetailSerializer
        elif self.action == "create":
            return AlbumCreateSerializer
        else:
            return BaseAlbumSerializer


class SongIndex(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    """
    This view class automatically provides `list` and `retrieve`
    actions for Song.
    """
    queryset = Song.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SongDetailSerializer
        else:
            return SongSerializer


class ArtistFilter(rest_framework.FilterSet):
    """
    Filter Artist view class.
    """
    min_year = rest_framework.NumberFilter(field_name="first_year_active",
                                           lookup_expr='gte')
    max_year = rest_framework.NumberFilter(field_name="first_year_active",
                                           lookup_expr='lte')

    class Meta:
        model = Artist
        fields = ['min_year', 'max_year']


class ArtistIndex(viewsets.ModelViewSet):
    """
    This view class automatically provides `list` and `retrieve`
    actions for Artist.
    """
    queryset = Artist.objects.all()
    filter_backends = [filters.OrderingFilter,
                       rest_framework.DjangoFilterBackend]
    filterset_class = ArtistFilter
    ordering_fields = ['name', 'first_year_active']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArtistDetailSerializer
        else:
            return ArtistSerializer


class LyricIndex(viewsets.ModelViewSet):
    """
    This view class automatically provides `list` and `retrieve`
    actions for Lyric.
    """
    queryset = Lyric.objects.all()
    serializer_class = LyricDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', 'song__name', 'song__album__name']
    ordering_fields = ['text', 'song__name', 'song__album__name']

    # Need add method and auth check
    def vote_up(self, request, pk=None):
        """
        Handles vote up for lyric
        """
        print(" --- here ----------")
        lyric = self.get_object()
        lyric.vote(request.user, +1)
        serializer = self.get_serializer(lyric)
        return Response(serializer.data)

    # Need add method and auth check
    def vote_down(self, request, pk=None):
        """
        Handles vote down for lyric
        """
        lyric = self.get_object()
        lyric.vote(request.user, -1)
        serializer = self.get_serializer(lyric)
        return Response(serializer.data)
