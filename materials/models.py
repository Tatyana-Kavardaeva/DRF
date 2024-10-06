from django.db import models
from config import settings


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Курс")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(
        upload_to="media/course", verbose_name="Изображение", blank=True, null=True
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Курс"
    )
    title = models.CharField(max_length=100, verbose_name="Урок")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(
        upload_to="media/course", verbose_name="Изображение", blank=True, null=True
    )
    video = models.URLField(
        max_length=200, verbose_name="Ссылка на видео", blank=True, null=True
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Владелец')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
