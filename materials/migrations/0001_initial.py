# Generated by Django 5.1.1 on 2024-09-30 20:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Курс")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media/course",
                        verbose_name="Изображение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Урок")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media/course",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "video",
                    models.URLField(
                        blank=True, null=True, verbose_name="Ссылка на видео"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="materials.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
    ]
