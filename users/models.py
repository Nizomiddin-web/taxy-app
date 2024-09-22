from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(verbose_name="Ismi", max_length=255, null=True, blank=True)
    last_name = models.CharField(verbose_name="Familiyasi", max_length=255, null=True, blank=True)
    country_code = models.CharField(verbose_name="Mamlakat Kodi", max_length=5, null=True, blank=True)
    phone_number = models.CharField(verbose_name="Telefon raqami", max_length=15, unique=True, null=True, blank=True)
    verify_code = models.IntegerField(verbose_name="SMS CODE", null=True, blank=True)
    verification_status = models.BooleanField(default=False)
    # user joylashuvini saqlash uchun
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_balance(self, amount):
        self.balance += amount
        self.save()

    def subtract_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Yetarli mablag' mavjud emas!")

    def admin_show_name(self):
        if self.first_name:
            if self.last_name:
                return f"{self.first_name} {self.last_name}"
            return self.first_name
        elif self.phone_number:
            return self.phone_number
        return str(self.telegram_id)

    def __str__(self):
        return self.admin_show_name()


class MachineCheck(models.Model):
    STATUS_CHOICES = [
        ('not_submitted', 'Not Submitted'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='machine_checks/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_submitted')
    rejection_reason = models.TextField(blank=True, null=True)
    status_last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_status_display()}--{self.user}"


class FaceCheck(models.Model):
    STATUS_CHOICES = [
        ('not_submitted', 'Not Submitted'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='face_checks/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_submitted')
    rejection_reason = models.TextField(blank=True, null=True)
    status_last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_status_display()}--{self.user}"


class Amount(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('daily', 'Kunlik'),
        ('monthly', 'Oylik'),
        ('weekly', 'Haftalik'),
        ('yearly', 'Yillik'),
    ]
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.get_payment_type_display()} - {self.amount} UZS"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.ForeignKey(Amount, on_delete=models.CASCADE)  # Amount modeliga bog'lanish
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user}, Amount: {self.amount.amount} UZS, Date: {self.payment_date}"


class DemoData(models.Model):
    country_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=15, unique=True)


class SupportRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support_requests")
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="handled_requests")
    is_handled = models.BooleanField(default=False)  # So'rov ustida ishlanganligini ko'rsatadi
    is_closed = models.BooleanField(default=False)  # Chatning yopilganligini ko'rsatadi
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)  # Chat yopilgan vaqt

    def __str__(self):
        return f"Request by {self.user.phone_number} - {'Closed' if self.is_closed else 'Open'}"


class ChatLog(models.Model):
    support_request = models.ForeignKey(SupportRequest, on_delete=models.CASCADE, related_name='chat_logs')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.phone_number}: {self.message} at {self.timestamp}"
