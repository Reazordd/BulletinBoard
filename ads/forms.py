from django import forms
from .models import Advertisement, Response, City, Category  # Добавляем импорт Category

class AdvertisementForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Выберите город"
    )
    category = forms.ModelChoiceField(  # Добавляем поле категории
        queryset=Category.objects.all(),
        empty_label="Выберите категорию"
    )

    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'price', 'city', 'category', 'cover']  # Добавляем category
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'cover': 'Обложка объявления',
            'category': 'Категория',  # Добавляем метку
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