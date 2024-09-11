from django.contrib import admin
from blackpearl_admin.models import *
from blackpearl_admin.forms import *
from django.utils.html import format_html

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    list_display = ('name', 'image_thumbnail', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('parent',)

    def image_thumbnail(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="50" height="50" />', obj.images.url)
        return 'No Image'
    
    image_thumbnail.short_description = 'Image'

class BrandAdmin(admin.ModelAdmin):
    form = BrandForm
    list_display = ('name', 'image_thumbnail', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def image_thumbnail(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" />', obj.icon.url)
        return 'No Image'
    
    image_thumbnail.short_description = 'Image'

class VariantTypeAdmin(admin.ModelAdmin):
    list_display = ('Varient_Name',)
    search_fields = ('Varient_Name',)

class VariantValueAdmin(admin.ModelAdmin):
    list_display = ('uid','Varient_Values', 'Varient_Type')
    search_fields = ('Varient_Values',)
    list_filter = ('Varient_Type',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BannerAdmin(admin.ModelAdmin):
    form = BannerForm
    list_display = ('banner_name', 'image_thumbnail', 'display_order', 'status')
    list_editable = ('status', 'display_order')
    search_fields = ('banner_name',)
    list_filter = ('status',)

    def image_thumbnail(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="50" height="50" />', obj.images.url)
        return 'No Image'
    
    image_thumbnail.short_description = 'Image'

class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_type', 'discount_value', 'start_date', 'end_date', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('discount_type', 'is_active')

class ProductvarientInline(admin.StackedInline):
    model = Product_Varients
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductvarientInline]
    list_display = ('Name', 'Product_Category', 'Product_Brand', 'average_rating', 'trendy')
    prepopulated_fields = {'slug': ('Name',)}
    search_fields = ('Name', 'Description', 'Features')
    list_filter = ('Product_Category', 'Product_Brand', 'trendy')

class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ('coupon_code', 'discount', 'type', 'start_date', 'end_date', 'is_active')
    search_fields = ('coupon_code',)
    list_filter = ('type', 'is_active')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('product', 'rating', 'created_at')
    search_fields = ('user__username', 'product__Name', 'comment')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Varient_Type, VariantTypeAdmin)
admin.site.register(Varient_Values, VariantValueAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CouponCode, CouponCodeAdmin)
admin.site.register(Review, ReviewAdmin)