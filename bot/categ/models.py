from django.db import models
from rest_framework import serializers


class Topic(models.Model):
    CHANGEABLE_CHOICES = (
        (0, 'нет'),
        (1, 'разрешено'),
        (2, 'только админ'),
    )

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    popularity = models.IntegerField(
        default=0,
        verbose_name='Популярность'
    )

    changeable = models.IntegerField(
        choices=CHANGEABLE_CHOICES,
        default=0,
        verbose_name='Разрешено ли редактирование',
        help_text='0 - нет, 1 - разрешено, 2 - только админ'
    )

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topic'


class Word(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='words',
                              verbose_name='Категория, к которой принадлежат слова')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение слова')
    word = models.CharField(max_length=255, verbose_name='Слово на кириллице')
    transcription = models.CharField(max_length=255, verbose_name='Транскрипция')
    lexical_meaning = models.JSONField(verbose_name='Лексическое значение')
    context = models.JSONField(verbose_name='Чаще всего используемый контекст')
    changeable = models.IntegerField(
        choices=Topic.CHANGEABLE_CHOICES,
        default=0,
        verbose_name='Разрешено ли редактирование',
        help_text='0 - нет, 1 - разрешено, 2 - только админ'
    )

    class Meta:
        verbose_name = 'Word'
        verbose_name_plural = 'Word'


class Place(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='places',
                              verbose_name='Категория, к которой принадлежат места')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение заведения')
    name = models.CharField(max_length=255, verbose_name='Название заведения')
    description = models.CharField(max_length=255, verbose_name='Описание заведения')
    opening_hours = models.CharField(max_length=255, verbose_name='Режим работы')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    contacts = models.JSONField(verbose_name='Контакты заведения, соцсети и т. д.')
    keywords = models.JSONField(null=True, blank=True, verbose_name='Ключевые слова')
    changeable = models.IntegerField(
        choices=Topic.CHANGEABLE_CHOICES,
        default=0,
        verbose_name='Разрешено ли редактирование',
        help_text='0 - нет, 1 - разрешено, 2 - только админ'
    )

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Place'


class Reflection(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='reflections',
                              verbose_name='Категория, к которой принадлежат размышления')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    thought = models.CharField(max_length=255, verbose_name='Вопрос или утверждение')
    explanation = models.CharField(max_length=255, verbose_name='Раскрытие темы')
    facts = models.JSONField(null=True, blank=True, verbose_name='Факты')
    advice = models.JSONField(null=True, blank=True, verbose_name='Советы')
    keywords = models.JSONField(null=True, blank=True, verbose_name='Ключевые слова')
    changeable = models.IntegerField(
        choices=Topic.CHANGEABLE_CHOICES,
        default=0,
        verbose_name='Разрешено ли редактирование',
        help_text='0 - нет, 1 - разрешено, 2 - только админ'
    )

    class Meta:
        verbose_name = 'Reflection'
        verbose_name_plural = 'Reflection'


class Phrase(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='phrases',
                              verbose_name='Категория, к которой принадлежат фразы')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    name = models.CharField(max_length=255, verbose_name='Фраза')
    transcription = models.CharField(max_length=255, verbose_name='Транскрипция')
    meaning = models.JSONField(verbose_name='Значения')
    appropriateness = models.CharField(max_length=255, verbose_name='В каких ситуациях уместно использование этой фразы')
    keywords = models.JSONField(null=True, blank=True, verbose_name='Ключевые слова')
    changeable = models.IntegerField(
        choices=Topic.CHANGEABLE_CHOICES,
        default=0,
        verbose_name='Разрешено ли редактирование',
        help_text='0 - нет, 1 - разрешено, 2 - только админ'
    )

    class Meta:
        verbose_name = 'Phrase'
        verbose_name_plural = 'Phrase'
