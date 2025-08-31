from django.core.management.base import BaseCommand
from ads.models import Category, City
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Загружает начальные данные (категории и города)'

    def handle(self, *args, **options):
        # Сначала удалим существующие данные
        Category.objects.all().delete()
        City.objects.all().delete()

        # Создаем категории с ручным указанием slug
        categories = [
            {'name': 'Электроника', 'slug': 'electronics', 'description': 'Техника, гаджеты, компьютеры'},
            {'name': 'Одежда', 'slug': 'clothing', 'description': 'Одежда, обувь, аксессуары'},
            {'name': 'Мебель', 'slug': 'furniture', 'description': 'Мебель для дома и офиса'},
            {'name': 'Транспорт', 'slug': 'transport', 'description': 'Автомобили, велосипеды, запчасти'},
            {'name': 'Недвижимость', 'slug': 'real-estate', 'description': 'Квартиры, дома, участки'},
            {'name': 'Работа', 'slug': 'jobs', 'description': 'Вакансии и резюме'},
            {'name': 'Услуги', 'slug': 'services', 'description': 'Различные услуги'},
        ]

        for cat_data in categories:
            category = Category.objects.create(**cat_data)
            self.stdout.write(
                self.style.SUCCESS(f'Создана категория: {category.name}')
            )

        # Создаем города с ручным указанием slug
        cities = [
            {'name': 'Москва', 'slug': 'moscow'},
            {'name': 'Санкт-Петербург', 'slug': 'saint-petersburg'},
            {'name': 'Новосибирск', 'slug': 'novosibirsk'},
            {'name': 'Екатеринбург', 'slug': 'ekaterinburg'},
            {'name': 'Казань', 'slug': 'kazan'},
            {'name': 'Нижний Новгород', 'slug': 'nizhny-novgorod'},
            {'name': 'Челябинск', 'slug': 'chelyabinsk'},
            {'name': 'Самара', 'slug': 'samara'},
            {'name': 'Омск', 'slug': 'omsk'},
            {'name': 'Ростов-на-Дону', 'slug': 'rostov-on-don'},
            {'name': 'Уфа', 'slug': 'ufa'},
            {'name': 'Красноярск', 'slug': 'krasnoyarsk'},
            {'name': 'Воронеж', 'slug': 'voronezh'},
            {'name': 'Пермь', 'slug': 'perm'},
            {'name': 'Волгоград', 'slug': 'volgograd'},
            {'name': 'Краснодар', 'slug': 'krasnodar'},
            {'name': 'Саратов', 'slug': 'saratov'},
            {'name': 'Тюмень', 'slug': 'tyumen'},
            {'name': 'Тольятти', 'slug': 'tolyatti'},
            {'name': 'Ижевск', 'slug': 'izhevsk'},
        ]

        for city_data in cities:
            city = City.objects.create(**city_data)
            self.stdout.write(
                self.style.SUCCESS(f'Создан город: {city.name}')
            )

        self.stdout.write(
            self.style.SUCCESS('Начальные данные успешно загружены!')
        )