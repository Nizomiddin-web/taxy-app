from decimal import Decimal

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status, generics, serializers, views
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, MachineCheck, FaceCheck, Payment, Amount, SupportRequest, ChatLog

# Create your views here.
from .serializers import UserSerializer, MachineCheckSerializer, FaceCheckSerializer, PaymentSerializer, \
    AmountSerializer, SupportRequestSerializer, ChatLogSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'telegram_id'

    def create(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')

        user, created = User.objects.get_or_create(telegram_id=telegram_id)
        if not created:
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Balans qo'shish uchun endpoint
    @action(detail=True, methods=['post'])
    def add_balance(self, request, telegram_id=None):
        user = self.get_object()
        amount = request.data.get('amount', 0)
        try:
            amount = Decimal(amount)
            user.add_balance(amount)
            return Response({'message': 'Balans muvaffaqiyatli qo\'shildi', 'balance': user.balance},
                            status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Noto\'g\'ri miqdor'}, status=status.HTTP_400_BAD_REQUEST)

    # Balans ayirish uchun endpoint
    @action(detail=True, methods=['post'])
    def subtract_balance(self, request, telegram_id=None):
        user = self.get_object()
        amount = request.data.get('amount', 0)
        try:
            amount = Decimal(amount)
            if user.balance >= amount:
                user.subtract_balance(amount)
                return Response({'message': 'Balans muvaffaqiyatli kamaytirildi', 'balance': user.balance},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Balans yetarli emas'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Noto\'g\'ri miqdor'}, status=status.HTTP_400_BAD_REQUEST)


class UserPhoneListView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone_number'


class MachineCheckView(viewsets.ModelViewSet):
    serializer_class = MachineCheckSerializer
    queryset = MachineCheck.objects.all()


class FaceCheckView(viewsets.ModelViewSet):
    queryset = FaceCheck.objects.all()
    serializer_class = FaceCheckSerializer


class VerifyUserView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        phone_number = request.data.get('phone_number')

        try:
            user = User.objects.get(telegram_id=telegram_id)
            if user.phone_number == phone_number:
                user.verification_status = 'verified'
                user.save()
                return Response({'status': 'success', 'message': 'User verified successfully!'})
            return Response({'status': 'failed', 'message': 'Phone number mismatch'},
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'status': 'failed', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class MachineCheckUpdateView(generics.GenericAPIView):
    serializer_class = MachineCheckSerializer

    def get_machine_check_by_user(self, telegram_id):
        """Helper method to retrieve MachineCheck by User's telegram_id."""
        user = get_object_or_404(User, telegram_id=telegram_id)
        return get_object_or_404(MachineCheck, user=user), user

    def put(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        machine_check, user = self.get_machine_check_by_user(telegram_id)

        # Remove 'user' field from request data if it exists
        data = request.data.copy()
        if 'user' in data:
            data.pop('user')

        serializer = self.get_serializer(machine_check, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)  # Save with the user object
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        machine_check, user = self.get_machine_check_by_user(telegram_id)

        # Remove 'user' field from request data if it exists
        data = request.data.copy()
        if 'user' in data:
            data.pop('user')

        serializer = self.get_serializer(machine_check, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)  # Save with the user object
        return Response(serializer.data, status=status.HTTP_200_OK)


class MachineCheckRetrieveView(generics.GenericAPIView):
    serializer_class = MachineCheckSerializer

    def get(self, request, telegram_id, *args, **kwargs):
        # Get the user by telegram_id
        user = get_object_or_404(User, telegram_id=telegram_id)
        # Get the MachineCheck associated with the user
        machine_check = get_object_or_404(MachineCheck, user=user)

        # Serialize the MachineCheck and return the response
        serializer = self.get_serializer(machine_check)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FaceCheckRetrieveView(generics.GenericAPIView):
    serializer_class = FaceCheckSerializer

    def get(self, request, telegram_id, *args, **kwargs):
        # Get the user by telegram_id
        user = get_object_or_404(User, telegram_id=telegram_id)
        # Get the MachineCheck associated with the user
        machine_check = get_object_or_404(FaceCheck, user=user)

        # Serialize the MachineCheck and return the response
        serializer = self.get_serializer(machine_check)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FaceCheckUpdateView(generics.GenericAPIView):
    serializer_class = FaceCheckSerializer

    def get_machine_check_by_user(self, telegram_id):
        """Helper method to retrieve MachineCheck by User's telegram_id."""
        user = get_object_or_404(User, telegram_id=telegram_id)
        return get_object_or_404(FaceCheck, user=user), user

    def put(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        machine_check, user = self.get_machine_check_by_user(telegram_id)

        # Remove 'user' field from request data if it exists
        data = request.data.copy()
        if 'user' in data:
            data.pop('user')

        serializer = self.get_serializer(machine_check, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)  # Save with the user object
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        machine_check, user = self.get_machine_check_by_user(telegram_id)

        # Remove 'user' field from request data if it exists
        data = request.data.copy()
        if 'user' in data:
            data.pop('user')

        serializer = self.get_serializer(machine_check, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)  # Save with the user object
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Response
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AmountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amount.objects.all()
    serializer_class = AmountSerializer

    def list(self, request, *args, **kwargs):
        # URL'dan `payment_type` parametrini olamiz
        payment_type = request.query_params.get('type', None)

        if payment_type:
            # Agar type berilgan bo'lsa, filtrlaymiz
            queryset = self.queryset.filter(payment_type=payment_type)
        else:
            # Agar type berilmagan bo'lsa, barcha amountlar qaytariladi
            queryset = self.queryset.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LastTenPayments(APIView):
    def get(self, request, telegram_id):
        # So'nggi 10 ta to'lovni olish
        payments = Payment.objects.filter(user__telegram_id=telegram_id).order_by('-payment_date')[:10]

        # Serializer orqali ma'lumotni yuborish
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class ChatLogCreateAPIView(APIView):
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        support_request_id = request.data.get('support_request_id')
        message = request.data.get('message')

        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        try:
            support_request = SupportRequest.objects.get(id=support_request_id, is_closed=False)
        except SupportRequest.DoesNotExist:
            return Response({"detail": "Muloqot topilmadi yoki so'rov yopilgan."}, status=status.HTTP_404_NOT_FOUND)

        chat_log = ChatLog.objects.create(
            support_request=support_request,
            sender=user,
            message=message
        )

        serializer = ChatLogSerializer(chat_log)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SupportRequestCloseAPIView(APIView):
    def post(self, request):
        # Telegram ID ni olish
        id = request.data.get('support_request_id')
        if not id:
            return Response({"detail": "Telegram ID taqdim etilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            support_request = SupportRequest.objects.get(id=id)
        except:
            return Response({"detail": "Yopiladigan faol so'rov topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        if not support_request:
            return Response({"detail": "Yopiladigan faol so'rov topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        # Chatni yopish
        support_request.is_closed = True
        support_request.closed_at = timezone.now()  # Chatni yopilgan vaqtini belgilash
        support_request.save()

        return Response({"detail": "Muloqot yopildi."}, status=status.HTTP_200_OK)


class SupportRequestCreateAPIView(APIView):
    def post(self, request):
        # POST so'rovdan user_id ni olish
        telegram_id = request.data.get('telegram_id')

        try:
            user = User.objects.get(telegram_id=telegram_id)  # User ni ID bo'yicha olish
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        # Foydalanuvchining hali yopilmagan so'rovi borligini tekshirish
        existing_request = SupportRequest.objects.filter(user=user, is_closed=False).first()

        if existing_request:
            return Response({"detail": "Sizning ochiq so'rovingiz mavjud."}, status=status.HTTP_400_BAD_REQUEST)

        # Yangi support so'rovi yaratish
        support_request = SupportRequest.objects.create(user=user)
        serializer = SupportRequestSerializer(support_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SupportRequestUpdateAPIView(APIView):
    def patch(self, request, pk):
        try:
            support_request = SupportRequest.objects.get(pk=pk)  # So'rovni ID bo'yicha olish
        except SupportRequest.DoesNotExist:
            return Response({"detail": "So'rov topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        # Adminning ID'sini olish (auth yoki POST orqali keladi)
        admin_id = request.data.get('admin_id')
        try:
            admin_user = User.objects.get(telegram_id=admin_id)
        except User.DoesNotExist:
            return Response({"detail": "Admin topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        # Adminni so'rovga qo'shish va is_handled ni yangilash
        support_request.admin = admin_user
        support_request.is_handled = True
        support_request.save()

        return Response({"detail": "So'rov muvaffaqiyatli yangilandi, admin qo'shildi."}, status=status.HTTP_200_OK)


class SupportRequestListAPIView(ListAPIView):
    queryset = SupportRequest.objects.filter(is_closed=False)
    serializer_class = SupportRequestSerializer


class ChatLogListAPIView(ListAPIView):
    serializer_class = ChatLogSerializer

    def get_queryset(self):
        support_request_id = self.kwargs['support_request_id']
        return ChatLog.objects.filter(support_request_id=support_request_id)


class ActiveSupportRequestAPIView(APIView):
    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        try:
            # Foydalanuvchini Telegram ID orqali topish
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        # Faol muloqot so'rovini topish (admin yoki user bo'lishi mumkin)
        support_request = SupportRequest.objects.filter(
            (Q(user=user) | Q(admin=user)),  # User yoki admin sifatida
            is_closed=False  # Muloqot hali yopilmagan
        ).first()
        if support_request:
            return Response(SupportRequestSerializer(support_request).data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Faol muloqot topilmadi."}, status=status.HTTP_404_NOT_FOUND)
