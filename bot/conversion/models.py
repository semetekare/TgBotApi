from django.db import models
from django.db.models import Sum
from categ.models import Topic

class StatisticsTopics(models.Model):
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE, primary_key=True, related_name='statistics', verbose_name='Категория, к которой принадлежит статистика', unique=True)
    counTransitions = models.IntegerField(verbose_name='Количество переходов')
    popularity = models.FloatField(verbose_name='Популярность', editable=False)  # Нельзя редактировать напрямую

    def save(self, *args, **kwargs):
        total_transitions = StatisticsTopics.objects.aggregate(total=Sum('counTransitions'))['total']
        if total_transitions:
            self.popularity = (self.counTransitions / total_transitions) * 100
        else:
            self.popularity = 0
        super().save(*args, **kwargs)

class StatisticsWords(models.Model):
    word_id = models.IntegerField(primary_key=True, verbose_name='ID слова к которой принадлежит статистика', unique=True)
    counTransitions = models.IntegerField(verbose_name='Количество переходов')
    popularity = models.FloatField(verbose_name='Популярность', editable=False)

    def save(self, *args, **kwargs):
        total_transitions = StatisticsWords.objects.aggregate(total=Sum('counTransitions'))['total']
        if total_transitions:
            self.popularity = (self.counTransitions / total_transitions) * 100
        else:
            self.popularity = 0
        super().save(*args, **kwargs)

class StatisticsPlaces(models.Model):
    places_id = models.IntegerField(primary_key=True, verbose_name='ID места к которому принадлежит статистика', unique=True)
    counTransitions = models.IntegerField(verbose_name='Количество переходов')
    popularity = models.FloatField(verbose_name='Популярность', editable=False)

    def save(self, *args, **kwargs):
        total_transitions = StatisticsPlaces.objects.aggregate(total=Sum('counTransitions'))['total']
        if total_transitions:
            self.popularity = (self.counTransitions / total_transitions) * 100
        else:
            self.popularity = 0
        super().save(*args, **kwargs)

class StatisticsReflections(models.Model):
    reflections_id = models.IntegerField(primary_key=True, verbose_name='ID размышления к которому принадлежит статистика', unique=True)
    counTransitions = models.IntegerField(verbose_name='Количество переходов')
    popularity = models.FloatField(verbose_name='Популярность', editable=False)

    def save(self, *args, **kwargs):
        total_transitions = StatisticsReflections.objects.aggregate(total=Sum('counTransitions'))['total']
        if total_transitions:
            self.popularity = (self.counTransitions / total_transitions) * 100
        else:
            self.popularity = 0
        super().save(*args, **kwargs)

class StatisticsPhrases(models.Model):
    phrases_id = models.IntegerField(primary_key=True, verbose_name='ID фразы к которой принадлежит статистика', unique=True)
    counTransitions = models.IntegerField(verbose_name='Количество переходов')
    popularity = models.FloatField(verbose_name='Популярность', editable=False)

    def save(self, *args, **kwargs):
        total_transitions = StatisticsPhrases.objects.aggregate(total=Sum('counTransitions'))['total']
        if total_transitions:
            self.popularity = (self.counTransitions / total_transitions) * 100
        else:
            self.popularity = 0
        super().save(*args, **kwargs)
