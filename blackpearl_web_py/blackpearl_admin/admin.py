from django.contrib import admin
from blackpearl_admin.models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Varient_Type)
admin.site.register(Varient_Values)

class ProductvarientAdmin(admin.StackedInline):
    model = Product_Varients

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductvarientAdmin]

admin.site.register(Product, ProductAdmin)
# admin.site.register(Product_Varients)