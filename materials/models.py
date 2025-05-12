from django.conf import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/preview/course",
        verbose_name="Превью",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="укажите описание курса"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="укажите название урока"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        blank=True,
        null=True,
        related_name="lessons",
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="укажите описание урока"
    )
    preview = models.ImageField(
        upload_to="materials/preview/lesson",
        verbose_name="Картинка",
        blank=True,
        null=True,
    )
    link_to_video = models.URLField(
        max_length=200,
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="укажите ссылку на видео материал",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user_subscriptions",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="course_subscriptions",
    )

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"
