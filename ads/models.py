from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify  # Добавляем импорт
import os  # Добавляем импорт

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Добавляем поле slug
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='covers/%Y/%m/%d/', blank=True, null=True)  # Добавляем поле для обложки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматически создаем slug из заголовка
        if not self.slug:
            self.slug = slugify(self.title)
            # Убеждаемся, что slug уникален
            original_slug = self.slug
            counter = 1
            while Advertisement.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('advertisement_detail', args=[str(self.slug)])  # Меняем на slug

    def delete(self, *args, **kwargs):
        # Удаляем файл обложки при удалении объявления
        if self.cover:
            if os.path.isfile(self.cover.path):
                os.remove(self.cover.path)
        super().delete(*args, **kwargs)

class Response(models.Model):
    RESPONSE_STATUS = [
        ('new', 'Новый'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    ]

    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='responses')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_responses')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_responses')
    text = models.TextField()
    status = models.CharField(max_length=10, choices=RESPONSE_STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отклик на {self.advertisement.title} от {self.sender.username}"

    def get_absolute_url(self):
        return reverse('response_detail', args=[str(self.id)])
