from datetime import date

from django.core.management.base import BaseCommand

from users.models import Payment, User


class Command(BaseCommand):

    def handle(self, *args, **options):

        params = dict(email="test@example.com", password="qwerty")

        user, user_status = User.objects.get_or_create(
            email=params["email"], defaults=params
        )

        if not user_status:  # если пользователь уже был найден
            self.stdout.write(
                self.style.SUCCESS(f"Пользователь с email {user.email} уже существует.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Пользователь с email {user.email} был создан.")
            )

        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("User created successfully."))

        payment_1 = Payment.objects.create(
            user=user,
            payment_date=date.today(),
            course_id=2,
            lesson=None,
            amount=1000.00,
            payment_method="cash",
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Платеж на сумму {payment_1.amount} создан для пользователя {user.email}"
            )
        )

        payment_2 = Payment.objects.create(
            user=user,
            payment_date=date.today(),
            course_id=2,
            lesson=None,
            amount=2000.00,
            payment_method="transfer",
        )

        self.stdout.write(self.style.SUCCESS("Данные о платежах успешно загружены!"))
