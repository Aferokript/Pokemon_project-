from django.db import models  # noqa F401


class Pokemon(models.Model):
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    title_ru = models.CharField(
        max_length=30,
        verbose_name='Название ру'
    )
    title_en = models.CharField(
        max_length=30,
        verbose_name='Название ен'
    )
    title_jp = models.CharField(
        max_length=30,
        verbose_name='Название яп'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolution',
        verbose_name='предыдущая эволюция'
    )
    element_type = models.ManyToManyField(
        'PokemonElementType',
        blank=True,
        related_name='pokemons',
        verbose_name='Стихии'

    )

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='Покемон'
    )
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Появился в'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Исчез в'
    )
    lat = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Широта'
    )
    lon = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Долгота'
    )
    level = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Уровень'
    )
    health = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Здоровье'
    )
    strength = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Сила'
    )
    defense = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Защита'
    )
    stamina = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Стамина'
    )

class PokemonElementType(models.Model):
    title = models.CharField(max_length=1000)
    strong_against = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name='Силен против'
    )
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='Изображение'
    )



    def __str__(self):
        return self.title
