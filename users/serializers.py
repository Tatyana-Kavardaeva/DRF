from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'groups', 'user_permissions', 'is_active', 'is_staff', 'is_superuser')


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

