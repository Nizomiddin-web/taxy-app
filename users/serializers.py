# serializers.py
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import User, MachineCheck, FaceCheck, Payment, Amount, ChatLog, SupportRequest, DemoData


class DemoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoData
        fields = ['id', 'country_code', 'phone_number']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['telegram_id', 'first_name', 'last_name', 'country_code', 'phone_number', 'verify_code',
                  'verification_status', 'balance', 'is_admin']


class MachineCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineCheck
        fields = ['id', 'user', 'image', 'status', 'rejection_reason', 'status_last_updated']


class FaceCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceCheck
        fields = ['id', 'user', 'image', 'status', 'rejection_reason', 'status_last_updated']


class PaymentSerializer(serializers.ModelSerializer):
    payment_type = serializers.CharField(source='amount.get_payment_type_display', read_only=True)
    amount_value = serializers.DecimalField(source='amount.amount', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Payment
        fields = ['user', 'amount', 'payment_date', 'payment_type', 'amount_value']

    # Save methodda balans qo'shish
    def create(self, validated_data):
        # To'lovni saqlaymiz
        payment = Payment.objects.create(**validated_data)

        # Foydalanuvchining balansini yangilash
        user = payment.user
        amount = payment.amount.amount  # Amount modelidagi qiymatni olamiz
        user.add_balance(amount)  # Foydalanuvchi balansiga qo'shamiz

        return payment


class AmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amount
        fields = ['id', 'payment_type', 'amount']


class ChatLogSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username',
                                            read_only=True)  # Yuboruvchi foydalanuvchining ismi

    class Meta:
        model = ChatLog
        fields = ['support_request', 'sender', 'message', 'timestamp', 'sender_username']
        read_only_fields = ['timestamp', 'sender_username']  # Ushbu ma'lumotlar avtomatik to'ldiriladi


class SupportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = ['id', 'user', 'admin', 'is_handled', 'is_closed', 'created_at']
        read_only_fields = ['id', 'created_at']
