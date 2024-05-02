from django.shortcuts import render

from rest_framework import mixins, status, viewsets

from .models import StatisticsTopics, StatisticsWords, StatisticsPlaces, StatisticsReflections, StatisticsPhrases
from .serializers import StatisticsTopicsSerializer, StatisticsWordsSerializer, StatisticsPlacesSerializer, \
    StatisticsReflectionsSerializer, StatisticsPhrasesSerializer


class StatisticsTopicsViewSet(viewsets.ModelViewSet):
    queryset = StatisticsTopics.objects.all()
    serializer_class = StatisticsTopicsSerializer


class StatisticsWordsViewSet(viewsets.ModelViewSet):
    queryset = StatisticsWords.objects.all()
    serializer_class = StatisticsWordsSerializer


class StatisticsPlacesViewSet(viewsets.ModelViewSet):
    queryset = StatisticsPlaces.objects.all()
    serializer_class = StatisticsPlacesSerializer


class StatisticsReflectionsViewSet(viewsets.ModelViewSet):
    queryset = StatisticsReflections.objects.all()
    serializer_class = StatisticsReflectionsSerializer


class StatisticsPhrasesViewSet(viewsets.ModelViewSet):
    queryset = StatisticsPhrases.objects.all()
    serializer_class = StatisticsPhrasesSerializer
