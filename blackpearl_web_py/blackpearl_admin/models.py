from django.db import models
from blackpearl_web_py.utils import unique_slug_generator,BaseModel
from django_lifecycle import LifecycleModelMixin, hook,LifecycleModel,\
    BEFORE_CREATE,AFTER_CREATE,AFTER_UPDATE,BEFORE_SAVE
from django.utils.text import slugify
import os
from ckeditor.fields import RichTextField
import string
import random
from django.core.exceptions import ValidationError
from django.db.models import Avg
from blackpearl_frntend.models import CustomerUser

# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=255)
    images = models.FileField(upload_to='category') 
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        db_table = "Category"

    def __str__(self) -> str:
        return self.name
    
    @hook(BEFORE_SAVE)
    def before_save(self):
        if not self.slug:
            self.slug = unique_slug_generator(self,self.name)

class Brand(BaseModel):
    name = models.CharField(max_length=100)
    icon = models.FileField(upload_to='brand/icon')
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self) -> str:
        return self.name
    
    @hook(BEFORE_CREATE)
    def before_create(self):
        if not self.slug:
            self.slug = unique_slug_generator(self,self.name)


class Varient_Type(BaseModel):
    Varient_Name = models.CharField(max_length=255)

    class Meta:
        db_table = "Varient_Type"

    def __str__(self) -> str:
        return self.Varient_Name

class Varient_Values(BaseModel):
    Varient_Values = models.CharField(max_length=255)
    Varient_Type = models.ForeignKey(Varient_Type,on_delete=models.CASCADE)
    Varient_Image = models.FileField(upload_to='values',blank = True,null=True)
    
    class Meta:
        db_table = "Varient_Values"

    def __str__(self) -> str:
        return self.Varient_Values
    
class Tag(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Tags'

    def __str__(self) -> str:
        return self.name


class Banner(BaseModel):
    banner_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    banner_url = models.CharField(max_length=255)
    # banner_display_order = models.IntegerField()
    images = models.FileField(upload_to='banners', blank=True, null=True)
    app_banner_image = models.FileField(upload_to='banners_app', blank=True, null=True)
    # is_intermediate = models.BooleanField(default=False)

    class Meta:
        db_table = 'banner'
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'


class Offer(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(
        max_length=15,
        choices=(
            ('amount', 'Amount'),
            ('percentage', 'Percentage'),
            ('b2g1', 'Buy Two Get One Free'),
        ),
        default='amount'
    )
    discount_value = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "offers"

    def __str__(self) -> str:
        return self.title

    def apply_discount(self, price, quantity):
        if self.discount_type == 'percentage':
            return price - (price * self.discount_value / 100)
        elif self.discount_type == 'amount':
            return price - self.discount_value
        elif self.discount_type == 'b2g1':
            # Calculate price for Buy 2 Get 1 Free offer
            # For every 3 items, the price of 1 item is free
            number_of_free_items = quantity // 3
            items_to_pay_for = quantity - number_of_free_items
            return price * items_to_pay_for
        return price


class Product(BaseModel):
    Name = models.CharField(max_length=250)
    Varient_Type = models.ManyToManyField(Varient_Type,blank=True)
    Product_Category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    Product_Brand = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    Description = RichTextField()
    product_details = RichTextField(blank=True,null=True)
    about_his_item = RichTextField()
    Related_Products = models.ManyToManyField('self',blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True,null=True)
    trendy = models.BooleanField(default=False)
    average_rating = models.FloatField(default=0.0)

    class Meta:
        db_table = "Products"

    def update_rating(self):
        # Update the average rating based on related reviews
        self.average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
        self.save()

    def __str__(self) -> str:
        return self.Name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.Name)
        super().save(*args, **kwargs)
# # pre_save.connect(pre_save_receiver_product, sender = Product)
    
# """
# <<<<<<<<<<<<<<<end of slugify product>>>>>>>>>>>>>>>>>>>>
# """

class Product_Varients(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product varients")
    product_information = RichTextField(blank=True,null=True)
    varient_values = models.ManyToManyField(Varient_Values,blank=True,related_name='values')
    images = models.ImageField(upload_to='Products')
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    display_prize = models.DecimalField(max_digits=12,decimal_places=2)
    product_stock = models.PositiveIntegerField(blank=True,null=True)
    SKU_code = models.CharField(max_length=255)
    offers = models.ManyToManyField(Offer,blank=True)
    slug = models.SlugField(max_length=255, blank=True,null=True)

    class Meta:
        db_table = "Product_Varients"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{self.product.Name} ' + '-'.join([i.value for i in self.varient_values.all()]) + f'_{self.pk}'
            self.slug = slugify(slug)
        super().save(*args, **kwargs)
    
    def get_price_with_discount(self):
        if self.discount_percent > 0:
            discounted_price = self.display_prize * (1 - self.discount_percent / 100)
            return discounted_price
        return self.display_prize
    
    def get_price_with_offers(self,quantity):
        price_with_discount = self.get_price_with_discount()
        total_price = price_with_discount * quantity

        for offer in self.offers.filter(is_active=True):
            if offer.discount_type == 'b2g1':
                total_price = offer.apply_discount(price_with_discount, quantity)
            else:
                total_price = offer.apply_discount(total_price, quantity)

        return total_price


class CouponCode(models.Model):
    coupon_code = models.CharField(max_length=100, blank=True, unique=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    discount = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    type = models.CharField(
        max_length=15,
        choices=(
            ('amount', 'Amount'),
            ('percentage', 'Percentage'),
        ),
        default='amount'
    )
    user_count = models.PositiveIntegerField(null=True, blank=True)
    min_amount = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.coupon_code:
            self.coupon_code = self.generate_unique_coupon_code()
        super().save(*args, **kwargs)

    def generate_unique_coupon_code(self):
        letters = string.ascii_letters
        numbers = '0123456789'
        characters = letters + numbers
        while True:
            code = ''.join(random.choice(characters) for _ in range(12))
            if not CouponCode.objects.filter(coupon_code=code).exists():
                return code

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('End date must be after start date.')

    def apply_coupon(self, price):
        if self.type == 'percentage':
            return price - (price * self.discount / 100)
        elif self.type == 'amount':
            return price - self.discount
        return price
    
    def __str__(self):
        return self.coupon_code


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)  
    rating = models.PositiveIntegerField()  # Rating out of 5 or 10
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.Name}'
    

class Log(models.Model):
    user = models.CharField(max_length=100)
    activity = models.TextField()
    date = models.DateTimeField(auto_now_add=True,null=True)

    