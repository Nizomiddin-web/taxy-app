
# Custom filter: foydalanuvchi telegram ID bo'yicha filtrlash
from django.contrib import admin

from users.models import User


class UserTelegramIDFilter(admin.SimpleListFilter):
    title = 'Foydalanuvchi Telegram ID'
    parameter_name = 'user_telegram_id'

    def lookups(self, request, model_admin):
        return [(user.telegram_id, user.phone_number) for user in User.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(support_request__user__telegram_id=self.value())
        return queryset


# Custom filter: admin telegram ID bo'yicha filtrlash
class AdminTelegramIDFilter(admin.SimpleListFilter):
    title = 'Admin Telegram ID'
    parameter_name = 'admin_telegram_id'

    def lookups(self, request, model_admin):
        return [(admin.telegram_id, admin.phone_number) for admin in User.objects.filter()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(support_request__admin__telegram_id=self.value())
        return queryset
