from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('advertisement_detail', args=[str(self.id)])

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

