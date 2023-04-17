from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):
    """ Квартира. """

    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True
    )
    description = models.TextField(
        'Текст объявления',
        blank=True
    )
    price = models.IntegerField(
        'Цена квартиры',
        db_index=True
    )
    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True
    )
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное'
    )
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4'
    )
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж'
    )
    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True
    )
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True
    )
    has_balcony = models.NullBooleanField(
        'Наличие балкона',
        db_index=True
    )
    active = models.BooleanField(
        'Активно-ли объявление',
        db_index=True
    )
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True
    )
    new_building = models.BooleanField(
        'Новостройка',
        choices=(
            (True, 'Новостройка'),
            (False, 'Старый дом'),
            (None, 'Не заполнено')
        ),
        null=True,
        blank=True
    )
    liked_by = models.ManyToManyField(
        User,
        related_name='liked_flats',
        verbose_name='Кто поставил лайк',
        blank=True
    )

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def display_owners_phonenumber(self):
        for owner in self.owners.all():
            return owner.owner_pure_phonenumber

    display_owners_phonenumber.short_description = 'Номер владельца'


class Complaint(models.Model):
    """ Жалоба. """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complaints',
        verbose_name='Автор жалобы'
    )
    flat = models.ForeignKey(
        Flat,
        on_delete=models.CASCADE,
        related_name='complaints',
        verbose_name='Квартира, на которую пожаловались'
    )
    text = models.TextField(
        'Текст жалобы',
        max_length=500
    )

    def __str__(self):
        return f'Жалоба от {self.author.username} (id: {self.author.id})'

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'


class Owner(models.Model):
    """ Собственник. """

    name = models.CharField(
        'ФИО владельца',
        max_length=200,
        db_index=True
    )
    owners_phonenumber = models.CharField(
        'Номер владельца',
        max_length=20
    )
    owner_pure_phonenumber = PhoneNumberField(
        'Нормализованный номер владельца',
        max_length=12,
        blank=True
    )
    flats = models.ManyToManyField(
        Flat,
        related_name='owners',
        verbose_name='Квартиры собственника',
        db_index=True
    )

    def __str__(self):
        return f'{self.name} (id: {self.id})'

    class Meta:
        verbose_name = 'Собственник'
        verbose_name_plural = 'Собственники'
