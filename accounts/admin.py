from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from .models import CustomUser, Transaction


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'full_name', 'email', 'account_number', 'status', 'is_staff']
    list_filter = ['status', 'is_staff', 'is_superuser']
    search_fields = ['username', 'full_name', 'email', 'account_number']
    list_editable = ['status']
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'account_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Status', {'fields': ('status',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'full_name', 'email',
                       'account_number', 'status', 'is_staff', 'is_superuser'),
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'transaction_type_colored', 'amount_display', 'description_short', 'entered_by']
    list_filter = ['transaction_type', 'date', 'user']
    search_fields = ['description', 'user__username', 'user__full_name']
    date_hierarchy = 'date'
    autocomplete_fields = ['user', 'entered_by']
    list_select_related = ['user', 'entered_by']

    def transaction_type_colored(self, obj):
        if obj.transaction_type == 'debit':
            return mark_safe('<span style="color:#dc3545;font-weight:bold;">Debit</span>')
        return mark_safe('<span style="color:#28a745;font-weight:bold;">Credit</span>')
    transaction_type_colored.short_description = 'Type'

    def amount_display(self, obj):
        return '{:,.2f}'.format(obj.amount)
    amount_display.short_description = 'Amount'

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
