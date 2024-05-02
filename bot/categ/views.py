from rest_framework import viewsets
from rest_framework.response import Response

from .models import Topic, Word, Place, Reflection, Phrase
from .serializers import TopicSerializer, WordSerializer, PlaceSerializer, ReflectionSerializer, PhraseSerializer


class TopicWithRelatedObjectsViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            # Получаем объект топика по его ID
            topic = Topic.objects.get(pk=pk)

            # Сериализуем данные о топике
            topic_serializer = TopicSerializer(topic)

            # Получаем все связанные объекты: слова, места, размышления, фразы
            words = topic.words.all()
            places = topic.places.all()
            reflections = topic.reflections.all()
            phrases = topic.phrases.all()

            # Сериализуем связанные объекты
            word_serializer = WordSerializer(words, many=True)
            place_serializer = PlaceSerializer(places, many=True)
            reflection_serializer = ReflectionSerializer(reflections, many=True)
            phrase_serializer = PhraseSerializer(phrases, many=True)

            # Собираем все данные в один ответ
            response_data = {
                'topic': topic_serializer.data,
                'words': word_serializer.data,
                'places': place_serializer.data,
                'reflections': reflection_serializer.data,
                'phrases': phrase_serializer.data
            }

            return Response(response_data)

        except Topic.DoesNotExist:
            # Возвращаем ошибку 404, если топик с указанным ID не найден
            return Response({"error": "Топик с указанным ID не найден"}, status=404)

class PhrasesByTopicViewSet(viewsets.ViewSet):
    def list(self, request, topic_id=None):
        # Проверяем, был ли предоставлен ID топика в запросе
        if topic_id is None:
            return Response({"error": "Не указан ID топика"}, status=400)

        # Получаем все фразы для указанного топика
        phrases = self.get_phrases_for_topic(topic_id)

        # Проверяем, были ли найдены фразы для указанного топика
        if phrases is not None:
            # Сериализуем найденные фразы и возвращаем их в ответе
            serializer = PhraseSerializer(phrases, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Категория с указанным ID не найдена"}, status=404)

    def get_phrases_for_topic(self, topic_id):
        try:
            # Получаем объект топика по его ID
            topic = Topic.objects.get(id=topic_id)
            # Получаем все фразы, привязанные к этому топику
            phrases = topic.phrases.all()
            return phrases
        except Topic.DoesNotExist:
            # Возвращаем None, если топик с указанным ID не найден
            return None

class ReflectionsByTopicViewSet(viewsets.ViewSet):
    def list(self, request, topic_id=None):
        # Проверяем, был ли предоставлен ID топика в запросе
        if topic_id is None:
            return Response({"error": "Не указан ID топика"}, status=400)

        # Получаем все размышления для указанного топика
        reflections = self.get_reflections_for_topic(topic_id)

        # Проверяем, были ли найдены размышления для указанного топика
        if reflections is not None:
            # Сериализуем найденные размышления и возвращаем их в ответе
            serializer = ReflectionSerializer(reflections, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Категория с указанным ID не найдена"}, status=404)

    def get_reflections_for_topic(self, topic_id):
        try:
            # Получаем объект топика по его ID
            topic = Topic.objects.get(id=topic_id)
            # Получаем все размышления, привязанные к этому топику
            reflections = topic.reflections.all()
            return reflections
        except Topic.DoesNotExist:
            # Возвращаем None, если топик с указанным ID не найден
            return None

class PlacesByTopicViewSet(viewsets.ViewSet):
    def list(self, request, topic_id=None):
        if topic_id is None:
            return Response({"error": "Не указан ID топика"}, status=400)

        places = self.get_places_for_topic(topic_id)

        if places is not None:
            serializer = PlaceSerializer(places, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Категория с указанным ID не найдена"}, status=404)

    def get_places_for_topic(self, topic_id):
        try:
            # Получаем объект топика по его ID
            topic = Topic.objects.get(id=topic_id)
            # Получаем все места, привязанные к этому топику
            places = topic.places.all()
            return places
        except Topic.DoesNotExist:
            return None

class WordsToIDViewSet(viewsets.ViewSet):
    def list(self, request, topic_id=None):
        # ID топика в запросе?
        if topic_id is None:
            return Response({"error": "Не указан ID топика"}, status=400)

        # слова для топика
        words = self.get_words_for_topic(topic_id)

        if words is not None:
            serializer = WordSerializer(words, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Топик с указанным ID не найден"}, status=404)

    def get_words_for_topic(self, topic_id):
        try:
            # Получаем объект топика по его ID
            topic = Topic.objects.get(id=topic_id)
            # Получаем все слова, привязанные к этому топику
            words = topic.words.all()
            return words
        except Topic.DoesNotExist:
            # Возвращаем None, если топик с указанным ID не найден
            return None

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class ReflectionViewSet(viewsets.ModelViewSet):
    queryset = Reflection.objects.all()
    serializer_class = ReflectionSerializer


class PhraseViewSet(viewsets.ModelViewSet):
    queryset = Phrase.objects.all()
    serializer_class = PhraseSerializer
