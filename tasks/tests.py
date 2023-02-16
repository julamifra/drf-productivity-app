from django.contrib.auth.models import User
from .models import Task
from rest_framework import status
from rest_framework.test import APITestCase


class TaskListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='jul', password='1234')

    def test_can_list_tasks(self):
        jul = User.objects.get(username='jul')
        Task.objects.create(owner=jul, title='new title')
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_task(self):
        self.client.login(username='jul', password='1234')
        response = self.client.post('/tasks/', {'title': 'new title'})
        count = Task.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_task(self):
        response = self.client.post('/tasks/', {'title': 'new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)