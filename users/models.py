from django.contrib.auth.models import AbstractUser
from django.db import models
from materials.models import Course, Lesson
from config.settings import AUTH_USER_MODEL
from materials.models import Course, Lesson


class User(AbstractUser):

    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="укажите телефон",
    )

    city = models.CharField(
        max_length=200, blank=True, verbose_name="Город", help_text="Укажите город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        null=True,
        blank=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"



class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        related_name="payments",
    )
    payment_date = models.DateField(verbose_name="Дата оплаты")

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        blank=True,
        null=True,
        related_name="payments",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Урок",
        blank=True,
        null=True,
        related_name="payments",
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")

    payment_method = models.CharField(
        max_length=150, choices=PAYMENT_METHODS, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.user.email} - {self.amount} руб."
