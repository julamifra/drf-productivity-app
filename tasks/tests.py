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


class TaskDetailViewTests(APITestCase):
    def setUp(self):
        jul = User.objects.create_user(username='jul', password='1234')
        man = User.objects.create_user(username='man', password='4321')
        Task.objects.create(
            owner=jul, title='new title', notes='juls notes'
        )
        Task.objects.create(
            owner=man, title='another title', notes='mans notes'
        )

    def test_can_retrieve_task_using_valid_id(self):
        response = self.client.get('/tasks/1/')
        self.assertEqual(response.data['title'], 'new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_task_using_invalid_id(self):
        response = self.client.get('/tasks/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_task(self):
        self.client.login(username='jul', password='1234')
        response = self.client.put('/tasks/1/', {'title': 'another title'})
        task = Task.objects.filter(pk=1).first()
        self.assertEqual(task.title, 'another title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_task(self):
        self.client.login(username='jul', password='1234')
        response = self.client.put('/tasks/2/', {'title': 'new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)