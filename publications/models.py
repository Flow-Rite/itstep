from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Валідатор для обмеження розміру та типу зображень
def validate_image(image):
    # Перевіряємо, чи файл не є None
    if not image:
        return  # Якщо файл не передано, просто повертаємо

    file_size = image.size  # Оновлено для роботи з файлом
    limit_mb = 5  # Обмеження на розмір в 5 MB
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Максимальний розмір файлу {limit_mb}MB")

    valid_image_types = ['image/jpeg', 'image/png']

    # Перевірка, чи є атрибут content_type і чи файл має правильний тип
    if hasattr(image, 'content_type') and image.content_type not in valid_image_types:
        raise ValidationError("Дозволені лише JPEG або PNG зображення")


# Модель для виду публікації (книга, стаття тощо)
class PublicationType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Модель для публікації
class Publication(models.Model):
    # Поле для назви книги з обмеженням на максимальну кількість символів
    title = models.CharField(max_length=255, unique=False)

    # Поле для автора книги з обмеженням на кількість символів
    author = models.CharField(max_length=255)

    annotation = models.TextField()

    # Поле для року видання з обмеженням на мінімальне і максимальне значення
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000),  # Найраніше допустимий рік
            MaxValueValidator(datetime.now().year)  # Поточний рік як максимальне значення
        ]
    )

    # Поле для кількості сторінок з обмеженням на мінімум і максимум
    page_count = models.IntegerField(
        validators=[
            MinValueValidator(1),  # Мінімум 1 сторінка
            MaxValueValidator(10000)  # Максимум 10 000 сторінок
        ]
    )

    # Тип публікації через ForeignKey з іншим класом
    publication_type = models.ForeignKey('PublicationType', on_delete=models.CASCADE)

    # Поле для обкладинки книги з валідацією розміру і типу файлу
    cover_image = models.ImageField(
        upload_to='covers/', blank=True, null=True, validators=[validate_image]
    )

    # Поле для збереження користувача, що створив публікацію
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Поле для автоматичного додавання дати створення публікації
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

