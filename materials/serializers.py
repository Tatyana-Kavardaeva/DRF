from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = SerializerMethodField()

    def get_count_lessons(self, instance):
        return Lesson.objects.filter(course=instance).count()

    def get_lessons(self, instance):
        lessons = Lesson.objects.filter(course=instance)
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = ('title', 'description', 'image', 'count_lessons', 'lessons')
