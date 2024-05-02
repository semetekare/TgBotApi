from rest_framework import serializers
from .models import StatisticsTopics, StatisticsWords, StatisticsPlaces, StatisticsReflections, StatisticsPhrases

class StatisticsTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsTopics
        fields = '__all__'

class StatisticsWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsWords
        fields = '__all__'

class StatisticsPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsPlaces
        fields = '__all__'

class StatisticsReflectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsReflections
        fields = '__all__'

class StatisticsPhrasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsPhrases
        fields = '__all__'