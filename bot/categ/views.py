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
            word_serializer = WordSerializer(words, many=True, context={'request': request})
            place_serializer = PlaceSerializer(places, many=True, context={'request': request})
            reflection_serializer = ReflectionSerializer(reflections, many=True, context={'request': request})
            phrase_serializer = PhraseSerializer(phrases, many=True, context={'request': request})

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
        if topic_id is None:
            return Response({"error": "Не указан ID топика"}, status=400)

        phrases = self.get_phrases_for_topic(topic_id)

        if phrases is not None:
            phrases_data = []
            for phrase in phrases:
                phrase_data = {
                    "id": phrase.id,
                    "image": request.build_absolute_uri(phrase.image.url) if phrase.image else None,
                    "name": phrase.name,
                    "transcription": phrase.transcription,
                    "meaning": phrase.meaning,
                    "appropriateness": phrase.appropriateness,
                    "keywords": phrase.keywords,
                    "changeable": phrase.changeable,
                    "topic": phrase.topic.id
                }
                phrases_data.append(phrase_data)
            return Response(phrases_data)
        else:
            return Response({"error": "Категория с указанным ID не найдена"}, status=404)

    def get_phrases_for_topic(self, topic_id):
        try:
            topic = Topic.objects.get(id=topic_id)
            phrases = topic.phrases.all()
            return phrases
        except Topic.DoesNotExist:
            return None

class ReflectionsByTopicViewSet(viewsets.ViewSet):
    def list(self, request, topic_id=None):
        if topic_id is None:
            return Response({"error": "Не указан ID топика"}, status=400)

        reflections = self.get_reflections_for_topic(topic_id)

        if reflections is not None:
            reflections_data = []
            for reflection in reflections:
                reflection_data = {
                    "id": reflection.id,
                    "image": request.build_absolute_uri(reflection.image.url) if reflection.image else None,
                    "thought": reflection.thought,
                    "explanation": reflection.explanation,
                    "facts": reflection.facts,
                    "advice": reflection.advice,
                    "keywords": reflection.keywords,
                    "changeable": reflection.changeable,
                    "topic": reflection.topic.id
                }
                reflections_data.append(reflection_data)
            return Response(reflections_data)
        else:
            return Response({"error": "Категория с указанным ID не найдена"}, status=404)

    def get_reflections_for_topic(self, topic_id):
        try:
            topic = Topic.objects.get(id=topic_id)
            reflections = topic.reflections.all()
            return reflections
        except Topic.DoesNotExist:
            return None

class PlacesByTopicViewSet(viewsets.ViewSet):
    def list(self, request, topic_id=None):
        if topic_id is None:
            return Response({"error": "Не указан ID топика"}, status=400)

        places = self.get_places_for_topic(topic_id)

        if places is not None:
            places_data = []
            for place in places:
                place_data = {
                    "id": place.id,
                    "image": request.build_absolute_uri(place.image.url) if place.image else None,
                    "name": place.name,
                    "description": place.description,
                    "opening_hours": place.opening_hours,
                    "address": place.address,
                    "contacts": place.contacts,
                    "keywords": place.keywords,
                    "changeable": place.changeable,
                    "topic": place.topic.id
                }
                places_data.append(place_data)
            return Response(places_data)
        else:
            return Response({"error": "Категория с указанным ID не найдена"}, status=404)

    def get_places_for_topic(self, topic_id):
        try:
            topic = Topic.objects.get(id=topic_id)
            places = topic.places.all()
            return places
        except Topic.DoesNotExist:
            return None

class WordsToIDViewSet(viewsets.ViewSet):
    def list(self, request, topic_id=None):
        if topic_id is None:
            return Response({"error": "Не указан ID топика"}, status=400)

        words = self.get_words_for_topic(topic_id)

        if words is not None:
            words_data = []
            for word in words:
                word_data = {
                    "id": word.id,
                    "image": request.build_absolute_uri(word.image.url) if word.image else None,
                    "word": word.word,
                    "transcription": word.transcription,
                    "lexical_meaning": word.lexical_meaning,
                    "context": word.context,
                    "changeable": word.changeable,
                    "topic": word.topic.id
                }
                words_data.append(word_data)
            return Response(words_data)
        else:
            return Response({"error": "Топик с указанным ID не найден"}, status=404)

    def get_words_for_topic(self, topic_id):
        try:
            topic = Topic.objects.get(id=topic_id)
            words = topic.words.all()
            return words
        except Topic.DoesNotExist:
            return None

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # Создаем список слов, но с абсолютными URL для изображений
        words_with_absolute_image_urls = []
        for word_instance in queryset:
            word_data = {
                "id": word_instance.id,
                "image": request.build_absolute_uri(word_instance.image.url) if word_instance.image else None,
                "word": word_instance.word,
                "transcription": word_instance.transcription,
                "lexical_meaning": word_instance.lexical_meaning,
                "context": word_instance.context,
                "changeable": word_instance.changeable,
                "topic": word_instance.topic.id
            }
            words_with_absolute_image_urls.append(word_data)
        return Response(words_with_absolute_image_urls)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Создаем объект слова с абсолютным URL для изображения
        word_data = {
            "id": instance.id,
            "image": request.build_absolute_uri(instance.image.url) if instance.image else None,
            "word": instance.word,
            "transcription": instance.transcription,
            "lexical_meaning": instance.lexical_meaning,
            "context": instance.context,
            "changeable": instance.changeable,
            "topic": instance.topic.id
        }
        return Response(word_data)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        places_with_absolute_image_urls = []
        for place_instance in queryset:
            place_data = {
                "id": place_instance.id,
                "image": request.build_absolute_uri(place_instance.image.url) if place_instance.image else None,
                "name": place_instance.name,
                "description": place_instance.description,
                "opening_hours": place_instance.opening_hours,
                "address": place_instance.address,
                "contacts": place_instance.contacts,
                "keywords": place_instance.keywords,
                "changeable": place_instance.changeable,
                "topic": place_instance.topic.id
            }
            places_with_absolute_image_urls.append(place_data)
        return Response(places_with_absolute_image_urls)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        place_data = {
            "id": instance.id,
            "image": request.build_absolute_uri(instance.image.url) if instance.image else None,
            "name": instance.name,
            "description": instance.description,
            "opening_hours": instance.opening_hours,
            "address": instance.address,
            "contacts": instance.contacts,
            "keywords": instance.keywords,
            "changeable": instance.changeable,
            "topic": instance.topic.id
        }
        return Response(place_data)


class ReflectionViewSet(viewsets.ModelViewSet):
    queryset = Reflection.objects.all()
    serializer_class = ReflectionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        reflections_with_absolute_image_urls = []
        for reflection_instance in queryset:
            reflection_data = {
                "id": reflection_instance.id,
                "image": request.build_absolute_uri(reflection_instance.image.url) if reflection_instance.image else None,
                "thought": reflection_instance.thought,
                "explanation": reflection_instance.explanation,
                "facts": reflection_instance.facts,
                "advice": reflection_instance.advice,
                "keywords": reflection_instance.keywords,
                "changeable": reflection_instance.changeable,
                "topic": reflection_instance.topic.id
            }
            reflections_with_absolute_image_urls.append(reflection_data)
        return Response(reflections_with_absolute_image_urls)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        reflection_data = {
            "id": instance.id,
            "image": request.build_absolute_uri(instance.image.url) if instance.image else None,
            "thought": instance.thought,
            "explanation": instance.explanation,
            "facts": instance.facts,
            "advice": instance.advice,
            "keywords": instance.keywords,
            "changeable": instance.changeable,
            "topic": instance.topic.id
        }
        return Response(reflection_data)

class PhraseViewSet(viewsets.ModelViewSet):
    queryset = Phrase.objects.all()
    serializer_class = PhraseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        phrases_with_absolute_image_urls = []
        for phrase_instance in queryset:
            phrase_data = {
                "id": phrase_instance.id,
                "image": request.build_absolute_uri(phrase_instance.image.url) if phrase_instance.image else None,
                "name": phrase_instance.name,
                "transcription": phrase_instance.transcription,
                "meaning": phrase_instance.meaning,
                "appropriateness": phrase_instance.appropriateness,
                "keywords": phrase_instance.keywords,
                "changeable": phrase_instance.changeable,
                "topic": phrase_instance.topic.id
            }
            phrases_with_absolute_image_urls.append(phrase_data)
        return Response(phrases_with_absolute_image_urls)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        phrase_data = {
            "id": instance.id,
            "image": request.build_absolute_uri(instance.image.url) if instance.image else None,
            "name": instance.name,
            "transcription": instance.transcription,
            "meaning": instance.meaning,
            "appropriateness": instance.appropriateness,
            "keywords": instance.keywords,
            "changeable": instance.changeable,
            "topic": instance.topic.id
        }
        return Response(phrase_data)