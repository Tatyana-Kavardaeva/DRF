from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import validate_allow_links


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_allow_links])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_count_lessons(self, instance):
        return Lesson.objects.filter(course=instance).count()

    def get_lessons(self, instance):
        lessons = Lesson.objects.filter(course=instance)
        return LessonSerializer(lessons, many=True).data

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=instance).exists()

    class Meta:
        model = Course
        fields = ('pk', 'title', 'description', 'count_lessons', 'lessons', 'owner', 'subscription')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
