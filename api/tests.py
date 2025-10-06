from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.utils import timezone

from members.models import Member
from posts.models import Post


class PostApiTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_posts_returns_data(self):
        member = Member.objects.create_user(username='demo', password='Pass1234_', email='demo@example.com')
        Post.objects.create(title='Test', content='Content', pub_date=timezone.now(), member=member)

        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data.__len__(), 0)

    def test_authenticated_user_can_save_post(self):
        member = Member.objects.create_user(username='tester', password='Pass1234_', email='tester@example.com')
        post = Post.objects.create(title='Another', content='Post body', pub_date=timezone.now(), member=member)
        self.client.force_authenticate(user=member)
        url = reverse('post-save', args=[post.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        saved_url = reverse('saved-post-list')
        saved_response = self.client.get(saved_url)
        self.assertEqual(saved_response.status_code, status.HTTP_200_OK)
        self.assertEqual(saved_response.data[0]['post']['id'], post.pk)
