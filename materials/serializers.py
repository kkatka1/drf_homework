from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
