from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import os

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL-адрес тега")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="Цвет тега")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_ads', kwargs={'tag_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Tag.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-адрес категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_ads', kwargs={'category_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название города")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-адрес города")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while City.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='covers/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Advertisement.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('advertisement_detail', args=[str(self.slug)])

    def increment_views(self):
        """Увеличивает счетчик просмотров"""
        self.views += 1
        self.save(update_fields=['views'])

    def delete(self, *args, **kwargs):
        if self.cover and os.path.isfile(self.cover.path):
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
