from django.contrib import admin
from blackpearl_admin.models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name', 'description')
    list_filter = ('parent',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'slug')
    prepopulated_fields = {'slug': ('brand_name',)}
    search_fields = ('brand_name',)

class VariantTypeAdmin(admin.ModelAdmin):
    list_display = ('Varient_Name',)
    search_fields = ('Varient_Name',)

class VariantValueAdmin(admin.ModelAdmin):
    list_display = ('Varient_Values', 'Varient_Type')
    search_fields = ('Varient_Values',)
    list_filter = ('Varient_Type',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_name', 'display_order', 'status')
    list_editable = ('status', 'display_order')
    search_fields = ('banner_name',)
    list_filter = ('status',)

class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_type', 'discount_value', 'start_date', 'end_date', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('discount_type', 'is_active')

class ProductvarientInline(admin.StackedInline):
    model = Product_Varients
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductvarientInline]
    list_display = ('Name', 'Product_Category', 'Product_Brand', 'trendy')
    prepopulated_fields = {'slug': ('Name',)}
    search_fields = ('Name', 'Description', 'Features')
    list_filter = ('Product_Category', 'Product_Brand', 'trendy')

class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ('coupon_code', 'discount', 'type', 'start_date', 'end_date', 'is_active')
    search_fields = ('coupon_code',)
    list_filter = ('type', 'is_active')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Varient_Type, VariantTypeAdmin)
admin.site.register(Varient_Values, VariantValueAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Product, ProductAdmin)
# admin.site.register(Product_Varients)