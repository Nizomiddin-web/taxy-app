import csv

from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.utils.html import format_html
from reportlab.pdfgen import canvas

from .filter import UserTelegramIDFilter, AdminTelegramIDFilter
from .models import User, DemoData, MachineCheck, FaceCheck, Amount, Payment, ChatLog, SupportRequest

admin.site.site_header = "Imkaan Taxi Dashboard"
admin.site.site_title = "Imkaan's Admin"
admin.site.index_title = "Welcome to Imkaan Taxi's Admin Panel"


# PDF formatida foydalanuvchilar hisobotini eksport qilish
@admin.action(description='Foydalanuvchi hisobotini PDF formatida eksport qilish')
def export_users_to_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="foydalanuvchilar_hisoboti.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Foydalanuvchilar Hisoboti")

    y = 700
    p.drawString(100, y, "Telegram ID | Ismi | Familiyasi | Telefon Raqami | Balansi | Ro'yxatga olingan vaqti")

    for user in queryset:
        y -= 20
        p.drawString(100, y,
                     f"{user.telegram_id} | {user.first_name} | {user.last_name} | {user.country_code}{user.phone_number} | {user.balance} | {user.created_at}")

    p.showPage()
    p.save()
    return response


# Foydalanuvchilar hisobotini CSV formatda eksport qilish
@admin.action(description='Foydalanuvchi hisobotini CSV formatida eksport qilish')
def export_users_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="foydalanuvchilar_hisoboti.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Telegram ID', 'Ismi', 'Familiyasi', 'Mamlakat Kodi', 'Telefon Raqami', 'Balansi', 'Verifikatsiya', 'IsAdmin',
         'Ro\'yxatga olingan vaqti'])

    for user in queryset:
        writer.writerow(
            [user.telegram_id, user.first_name, user.last_name, user.country_code, user.phone_number, user.balance,
             user.verification_status, user.is_admin, user.created_at])

    return response


# SupportRequest hisobotini CSV formatida eksport qilish
@admin.action(description='Tekshiruvlarni CSV formatda eksport qilish')
def export_support_requests_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tekshiruvlar_hisoboti.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Foydalanuvchi', 'Admin', 'Yaratilgan vaqti', 'Yopilgan vaqti', 'Holati'])

    for request in queryset:
        writer.writerow(
            [request.id, request.user.phone_number, request.admin.phone_number if request.admin else 'Noma\'lum',
             request.created_at, request.closed_at, 'Yopilgan' if request.is_closed else 'Ochiq'])

    return response


# To'lovlar hisobotini CSV formatida eksport qilish
@admin.action(description='To\'lovlarni CSV formatida eksport qilish')
def export_payments_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tolovlar_hisoboti.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Foydalanuvchi', 'To\'lov Turi', 'Miqdor', 'To\'lov vaqti'])

    for payment in queryset:
        writer.writerow([payment.id, payment.user.phone_number, payment.amount.payment_type, payment.amount.amount,
                         payment.payment_date])

    return response


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['row_number', 'telegram_id', 'first_name', 'last_name', 'country_code', 'phone_number', 'balance',
                    'verification_status', 'is_admin']
    search_fields = ['telegram_id', 'first_name', 'last_name', 'phone_number']
    list_filter = ['verification_status', 'is_admin']
    list_display_links = ['telegram_id', 'first_name']
    list_per_page = 20
    actions = [export_users_to_csv, export_users_to_pdf]

    def row_number(self, obj):
        # obj.id ni ishlatish o'rniga, queryset orqali indekslash
        return list(self.model.objects.all()).index(obj) + 1

        # Sarlavhani o'zgartirish (ro'yxat ustunining nomi)

    row_number.short_description = '№'


@admin.register(DemoData)
class DemoDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'country_code', 'phone_number']


@admin.register(MachineCheck)
class MachineCheckAdmin(admin.ModelAdmin):
    list_display = ['row_number', 'user', 'status', 'rejection_reason', 'status_last_updated']
    list_filter = ['status']
    list_display_links = ['user']
    search_fields = ('user__first_name', 'user__last_name', 'user__phone_number', 'user__telegram_id')
    list_per_page = 20

    def row_number(self, obj):
        # obj.id ni ishlatish o'rniga, queryset orqali indekslash
        return list(self.model.objects.all()).index(obj) + 1

        # Sarlavhani o'zgartirish (ro'yxat ustunining nomi)

    row_number.short_description = '№'


@admin.register(FaceCheck)
class FaceCheckAdmin(admin.ModelAdmin):
    list_display = ['row_number', 'user', 'status', 'rejection_reason', 'status_last_updated']
    list_filter = ['status']
    list_display_links = ['user']
    search_fields = ('user__first_name', 'user__last_name', 'user__phone_number', 'user__telegram_id')
    list_per_page = 20

    def row_number(self, obj):
        # obj.id ni ishlatish o'rniga, queryset orqali indekslash
        return list(self.model.objects.all()).index(obj) + 1

        # Sarlavhani o'zgartirish (ro'yxat ustunining nomi)

    row_number.short_description = '№'


@admin.register(Amount)
class AmountAdmin(admin.ModelAdmin):
    list_display = ('row_number', 'payment_type', 'amount')
    list_filter = ('payment_type',)
    search_fields = ('payment_type',)
    list_display_links = ['payment_type']
    list_per_page = 20

    def row_number(self, obj):
        # obj.id ni ishlatish o'rniga, queryset orqali indekslash
        return list(self.model.objects.all()).index(obj) + 1

    # Sarlavhani o'zgartirish (ro'yxat ustunining nomi)
    row_number.short_description = '№'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('row_number', 'user', 'amount', 'payment_date')
    list_display_links = ['row_number', 'user']
    search_fields = ('user__first_name', 'user__last_name', 'user__phone_number', 'user__telegram_id')
    list_filter = ['payment_date']
    list_per_page = 20
    actions = [export_payments_to_csv]

    def row_number(self, obj):
        # obj.id ni ishlatish o'rniga, queryset orqali indekslash
        return list(self.model.objects.all()).index(obj) + 1

    # Sarlavhani o'zgartirish (ro'yxat ustunining nomi)
    row_number.short_description = '№'


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin', 'is_handled', 'is_closed', 'created_at')
    list_filter = ('is_handled', 'is_closed', 'created_at')
    search_fields = ('user__phone_number', 'admin__phone_number', 'user__telegram_id')
    list_per_page = 20
    actions = [export_support_requests_to_csv]


@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('support_request', 'sender', 'message', 'timestamp')
    list_filter = ('timestamp',UserTelegramIDFilter,AdminTelegramIDFilter)
    search_fields = (
        'support_request__user__telegram_id', 'support_request__admin__telegram_id', 'sender__telegram_id', 'message')
    list_per_page = 20
