from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_allow_links


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_allow_links])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = serializers.SerializerMethodField(read_only=True)

    def get_count_lessons(self, instance):
        return Lesson.objects.filter(course=instance).count()

    def get_lessons(self, instance):
        lessons = Lesson.objects.filter(course=instance)
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = ('pk', 'title', 'description', 'image', 'count_lessons', 'lessons', 'owner')
