from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StatisticsTopicsViewSet, StatisticsWordsViewSet, StatisticsPlacesViewSet, StatisticsReflectionsViewSet, StatisticsPhrasesViewSet

router = DefaultRouter()

router.register(r'statistics/topics', StatisticsTopicsViewSet)
router.register(r'statistics/words', StatisticsWordsViewSet)
router.register(r'statistics/places', StatisticsPlacesViewSet)
router.register(r'statistics/reflections', StatisticsReflectionsViewSet)
router.register(r'statistics/phrases', StatisticsPhrasesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
