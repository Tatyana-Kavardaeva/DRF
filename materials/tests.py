# from rest_framework import status
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscription


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@test.pro')
        self.course = Course.objects.create(title='test', description='test', owner=self.user)
        self.lesson = Lesson.objects.create(title='test_lesson', description='test', owner=self.user,
                                            course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lessons-retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse('materials:lesson-create')
        data = {
            'title': 'lesson_new_test',
            'video': 'https://www.youtube.com/'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:lesson-update', args=(self.lesson.pk,))
        data = {
            'title': 'update_test_lesson',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), 'update_test_lesson'
        )

    def test_lesson_delete(self):
        url = reverse('materials:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse('materials:lessons-list')
        response = self.client.get(url)
        data = response.json()
        result = {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "video": self.lesson.video,
                        "title": self.lesson.title,
                        "description": self.lesson.description,
                        "image": self.lesson.image,
                        "course": self.lesson.course.pk,
                        "owner": self.lesson.owner.pk
                    }
                ]
                    }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.pro')
        self.course = Course.objects.create(title='test2', description='test', owner=self.user)

        self.client.force_authenticate(user=self.user)

    def test_is_subscription(self):
        url = reverse('users:subscription-create')
        data = {
            'course_id': self.course.pk,
        }
        print(Subscription.objects.all())
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        print(Subscription.objects.all())
        print(self.user.email)
        print(self.course.title)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
