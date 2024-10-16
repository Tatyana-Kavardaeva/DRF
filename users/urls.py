from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView, PaymentRetrieveAPIView, PaymentCreateAPIView, \
    PaymentDestroyAPIView, PaymentUpdateAPIView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("payments/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment-retrieve"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path(
        "payments/<int:pk>/delete/", PaymentDestroyAPIView.as_view(), name="payment-delete"
    ),
    path(
        "payments/<int:pk>/update/", PaymentUpdateAPIView.as_view(), name="payment-update"
    ),
    # path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('login/', CustomTokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token-refresh'),
] + router.urls
