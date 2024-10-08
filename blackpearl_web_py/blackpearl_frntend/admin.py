from django.contrib import admin
from blackpearl_frntend.models import *

# Register your models here.


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
    

class CustomerLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'date')
    list_filter = ('activity',)
    search_fields = ('user', 'activity')
    ordering = ('-date',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'pro_price_with_dis')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__id')

    def product(self, obj):
        return obj.product

    ordering = ('-added_date',) 

admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(CustomerLog, CustomerLogAdmin)
admin.site.register(Cart, CartAdmin)