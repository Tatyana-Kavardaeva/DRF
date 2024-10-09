from rest_framework.serializers import ValidationError

allow_links = 'youtube.com'


def validate_allow_links(value):
    if allow_links not in value.lower():
        raise ValidationError('Добавление ссылок на сторонние сайты запрещено')
