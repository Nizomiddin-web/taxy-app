from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserPhoneListView, MachineCheckView, FaceCheckView, MachineCheckUpdateView, \
    FaceCheckUpdateView, MachineCheckRetrieveView, FaceCheckRetrieveView, PaymentViewSet, AmountViewSet, \
    LastTenPayments, SupportRequestCreateAPIView, ChatLogCreateAPIView, SupportRequestListAPIView, ChatLogListAPIView, \
    SupportRequestUpdateAPIView, ActiveSupportRequestAPIView, SupportRequestCloseAPIView, DemoDataByPhoneView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'machine-check', MachineCheckView)
router.register(r'face-check', FaceCheckView)
router.register(r'payments', PaymentViewSet)
router.register(r'amounts', AmountViewSet, basename='amount')

urlpatterns = [
    path('api/verify-phone/<int:phone_number>/', UserPhoneListView.as_view(), name='verify_phone'),
    path('api/payments-history/<int:telegram_id>/', LastTenPayments.as_view(), name='payments-history'),
    path('api/machine-check/update/', MachineCheckUpdateView.as_view(), name='machine-check-update'),
    path('api/machine-check/get/<int:telegram_id>/', MachineCheckRetrieveView.as_view(), name='machine-check-get'),
    path('api/face-check/get/<int:telegram_id>/', FaceCheckRetrieveView.as_view(), name='face-check-get'),
    path('api/face-check/update/', FaceCheckUpdateView.as_view(), name='face-check-update'),

    #Chat uchun api
    path('api/support/create/', SupportRequestCreateAPIView.as_view(), name='support-request-create'),
    path('api/support-requests/active/', ActiveSupportRequestAPIView.as_view(), name='support-request-active'),
    path('api/support-requests/close/', SupportRequestCloseAPIView.as_view(), name='support-request-close'),
    path('api/support-request/<int:pk>/update/', SupportRequestUpdateAPIView.as_view(), name='support-request-update'),
    path('api/support/list/', SupportRequestListAPIView.as_view(), name='support-request-list'),
    path('api/chatlog/create/', ChatLogCreateAPIView.as_view(), name='chatlog-create'),
    path('api/chatlog/<int:support_request_id>/', ChatLogListAPIView.as_view(), name='chatlog-list'),

    # `phone_number` parametri URLda qabul qilinadi
    path('api/demo-data/<str:country_code>/<str:phone_number>/', DemoDataByPhoneView.as_view(), name='demo-data-by-phone'),

    path('api/', include(router.urls)),
]
