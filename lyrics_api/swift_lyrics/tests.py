"""
Unit tests
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from swift_lyrics.models import Artist, Lyric
# Create your tests here.


class AlbumTests(APITestCase):

    def test_create_without_year_fails(self):
        data = {
            'name': 'Thriller',
            'artist_name': 'Michael Jackson'
        }
        response = self.client.post(reverse('album-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ArtistTest(APITestCase):

    def test_list(self):
        response = self.client.get(reverse('artist-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # make sure that each artist includes id, name and first_year_active
        # in response but not albums
        for result in response.data['results']:
            self.assertIn('id', result)
            self.assertIn('name', result)
            self.assertIn('first_year_active', result)

    def test_detail(self):
        artist = Artist.objects.first()
        response = self.client.get(reverse('artist-detail', args=[artist.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item = response.data
        self.assertIn('id', item)
        self.assertIn('name', item)
        self.assertIn('first_year_active', item)
        self.assertIn('albums', item)

class LyricTests(APITestCase):

    def test_list(self):
        count = Lyric.objects.count()
        response = self.client.get(reverse('lyric-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], count)

    def test_vote_up(self):
        lyric = Lyric.objects.first()
        count = lyric.votes
        response = self.client.post(reverse('lyric-vote-up', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(lyric.votes, count + 1)

    def test_vote_down(self):
        lyric = Lyric.objects.first()
        count = lyric.votes
        response = self.client.post(reverse('lyric-vote-down', args=[lyric.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lyric = Lyric.objects.get(pk=lyric.pk)
        self.assertEqual(lyric.votes, count - 1)