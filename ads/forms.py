from django import forms
from .models import Advertisement, Response, City

class AdvertisementForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Выберите город"
    )

    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'price', 'city', 'cover']  # Добавляем cover
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'cover': 'Обложка объявления',  # Добавляем метку для поля
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите ваш отклик здесь...'
            }),
        }