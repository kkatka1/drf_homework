from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            title="course_test", description="Очень хороший курс"
        )
        self.lesson = Lesson.objects.create(
            title="lesson_test", description="Очень хороший урок", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "title": "Django",
            "description": "Django lesson description",
            "course": self.course.pk,
            "link_to_video": "http://youtube.com/watch?v=dQw4w9uHyq",
        }
        response = self.client.post(url, data)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_lesson = Lesson.objects.last()
        self.assertEqual(new_lesson.owner, self.user)

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "title": "Django",
            "description": "Django lesson description",
            "course": self.course.pk,
            "link_to_video": "http://youtube.com/watch?v=dQw4w9uHyq",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Django")

    def test_lesson_delete(self):
        url = reverse("materials:lesson-destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

class SubscriptionViewTests(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create(email="admin@sky.pro")

        # Создаем тестовый курс
        self.course = Course.objects.create(
            title="course_test", description="Очень хороший курс", owner=self.user
        )

    def test_subscribe_to_course(self):
        """Тестирование добавления подписки на курс"""
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": self.course.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Подписка добавлена.")

        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe_from_course(self):
        """Тестирование удаления подписки с курса"""
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": self.course.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Подписка удалена.")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscribe_to_nonexistent_course(self):
        """Тестирование добавления подписки на несуществующий курс"""
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": 1000000})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user(self):
        """Тестирование доступа неаутентифицированного пользователя"""
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": self.course.pk})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)