from rest_framework import routers
from django.urls import path, include

from .views import (TopicViewSet, WordViewSet, PlaceViewSet, ReflectionViewSet, PhraseViewSet, WordsToIDViewSet,
                    PlacesByTopicViewSet, ReflectionsByTopicViewSet, PhrasesByTopicViewSet, TopicWithRelatedObjectsViewSet)

router = routers.SimpleRouter()
router.register(r'topics', TopicViewSet)
router.register(r'words', WordViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'reflections', ReflectionViewSet)
router.register(r'phrases', PhraseViewSet)
router.register(r'topicWithRelatedObjects', TopicWithRelatedObjectsViewSet, basename='topic-with-related-objects')


urlpatterns = [
    path('', include(router.urls)),
    path('wordsByTopic/<int:topic_id>/', WordsToIDViewSet.as_view({'get': 'list'}), name='words-by-topic'),
    path('placesByTopic/<int:topic_id>/', PlacesByTopicViewSet.as_view({'get': 'list'}), name='places-by-topic'),
    path('reflectionsByTopic/<int:topic_id>', ReflectionsByTopicViewSet.as_view({'get': 'list'}),
         name='reflections-by-topic'),
    path('phrasesByTopic/<int:topic_id>', PhrasesByTopicViewSet.as_view({'get': 'list'}), name='phrases-by-topic'),
]
