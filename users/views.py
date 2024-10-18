from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from rest_framework.permissions import AllowAny
from users.servicees import create_stripe_sessions, create_stripe_price, create_stripe_product

from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data.get('email'))
        print(user.email, user.last_login)
        if user.is_authenticated:
            user.last_login = timezone.now().date()
            user.save()
            print(user.last_login)
        return response


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        else:
            return [IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        if payment.course or payment.lesson:
            product = payment.course if payment.course else payment.lesson
            product_id = create_stripe_product(product)
            price = create_stripe_price(payment.amount, product_id)
            session_id, payment_link = create_stripe_sessions(price)

            payment.session_id = session_id
            payment.link = payment_link
            payment.save()
        else:
            raise ValidationError("Выберите курс или урок для оплаты")


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payment_method', 'course', 'lesson']
    ordering_fields = ['payment_date']


class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateAPIView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyAPIView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

