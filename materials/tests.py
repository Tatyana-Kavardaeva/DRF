from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


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
        self.assertEqual(data.get('title'), self.lesson.title)

    def test_lesson_create_with_video(self):
        """ Проверяем создание урока с валидным видео """

        url = reverse('materials:lesson-create')
        data = {
            'title': 'lesson_new_test',
            'video': 'https://youtube.com/'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_create_with_invalid_video(self):
        """ Проверяем создание урока с невалидным видео """

        url = reverse('materials:lesson-create')
        data = {
            'title': 'lesson_new_test',
            'video': 'https://yandex.ru'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'video': ['Добавление ссылок на сторонние сайты запрещено']})

    def test_lesson_create_without_video(self):
        """ Проверяем создание урока без видео """

        url = reverse('materials:lesson-create')
        data = {'title': 'lesson_new_test'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse('materials:lesson-update', args=(self.lesson.pk,))
        data = {'title': 'update_test_lesson'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'update_test_lesson')

    def test_lesson_delete(self):
        url = reverse('materials:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.pro')
        self.course = Course.objects.create(title='test', description='test', owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.user_two = User.objects.create(email='test2@test2.pro')

    def test_course_retrieve(self):
        """ Проверяем получение курса по id авторизованным пользователем с подпиской на курс """
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(data.get('is_subscribed'))

    def test_course_retrieve_without_subscription(self):
        """ Проверяем получение курса по id авторизованным пользователем без подписки на курс """
        self.client.force_authenticate(user=self.user_two)
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(data, {"detail": "You do not have permission to perform this action."})

    def test_course_retrieve_without_authentication(self):
        """ Проверяем получение курса по id неавторизованным пользователем """
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data, {"detail": "Authentication credentials were not provided."})


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.pro')
        self.course = Course.objects.create(title='test2', description='test', owner=self.user)

    def test_is_subscription_create(self):
        """ Проверяем подписку на курс авторизованным пользователем """
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:subscription-create')
        data = {'course_id': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_is_subscription_delete(self):
        """ Проверяем отписку от курса """
        self.client.force_authenticate(user=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('materials:subscription-create')
        data = {'course_id': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка удалена'})

    def test_is_subscription_without_authentication(self):
        """ Проверяем подписку на курс неавторизованным пользователем """
        url = reverse('materials:subscription-create')
        data = {'course_id': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "Authentication credentials were not provided."})

    def test_is_subscription_without_course(self):
        """ Проверяем подписку на несуществующий курс """
        self.client.force_authenticate(user=self.user)
        url = reverse('materials:subscription-create')
        data = {'course_id': self.course.pk + 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {"detail": "No Course matches the given query."})
