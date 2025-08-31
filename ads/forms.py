from django import forms
from .models import Advertisement, Response, City, Category, Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
        labels = {
            'name': 'Название тега',
            'color': 'Цвет тега',
        }

class AdvertisementForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Выберите город",
        required=False,
        label="Город из списка"
    )
    new_city = forms.CharField(
        max_length=100,
        required=False,
        label="Или введите новый город",
        widget=forms.TextInput(attrs={'placeholder': 'Введите название города'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберите категорию"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Теги"
    )

    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'price', 'city', 'new_city', 'category', 'cover', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'cover': 'Обложка объявления',
            'category': 'Категория',
        }

    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        new_city = cleaned_data.get('new_city')

        if not city and not new_city:
            raise forms.ValidationError("Выберите город из списка или введите новый")

        if city and new_city:
            raise forms.ValidationError("Выберите только один вариант: город из списка или новый город")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        new_city = self.cleaned_data.get('new_city')
        if new_city:
            # Создаем новый город или находим существующий
            city, created = City.objects.get_or_create(
                name=new_city.strip(),
                defaults={'name': new_city.strip()}
            )
            instance.city = city

        if commit:
            instance.save()
            self.save_m2m()

        return instance

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