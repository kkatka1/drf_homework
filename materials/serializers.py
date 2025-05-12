from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Course, Lesson, Subscription
from .validators import validate_links


class LessonSerializer(ModelSerializer):
    link_to_video = serializers.CharField(validators=[validate_links])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Метод для получения информации о подписке текущего пользователя на курс.
        Возвращает True, если пользователь подписан, иначе False
        """
        user = self.context.get("request").user
        if not user.is_authenticated:  # Если пользователь не авторизован
            return False
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = "__all__"
