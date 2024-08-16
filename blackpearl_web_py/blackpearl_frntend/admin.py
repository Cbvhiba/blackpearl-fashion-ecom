from django.contrib import admin
from blackpearl_frntend.models import *

# Register your models here.

@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'first_name', 'last_name', 'is_active', 'registered_date')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    list_filter = ('is_active', 'gender')
    ordering = ('-registered_date',)
    readonly_fields = ('registered_date',)
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'phone', 'gender', 'profile_picture', 'is_active', 'total_orders', 'total_order_amount', 'password')}),
        ('Date Information', {'fields': ('registered_date',)}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('password',)
        return self.readonly_fields