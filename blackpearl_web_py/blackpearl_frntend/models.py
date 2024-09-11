from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_CREATE
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from blackpearl_admin.models import *
from django.contrib.auth.hashers import make_password, check_password

def username_from_email(email):
    """Generate a username from the email address."""
    if email:
        return email.split('@')[0]
    return 'NA'

class CustomerUser(LifecycleModelMixin, models.Model):
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=13, blank=True, null=True, unique=True)
    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=(
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
            ('Prefer not to say', 'Prefer not to say'),
        )
    )
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True) 
    profile_picture = models.ImageField(upload_to='customer_profiles/', blank=True, null=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    total_orders = models.IntegerField(default=0)
    total_order_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    class Meta:
        db_table = "customer"
        unique_together = ['username', 'phone', 'email']
        verbose_name = "Customer User"
        verbose_name_plural = "Customer Users"

    def __str__(self):
        return self.username or self.email
    
    def set_password(self, raw_password):
        """Hash the password before saving it."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the given password matches the hashed password."""
        return check_password(raw_password, self.password)
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.last_login:
            # Set last_login if it hasn't been set before (if the user already exists)
            self.last_login = timezone.now()
        super().save(*args, **kwargs)

    @hook(BEFORE_CREATE)
    def set_username(self):
        if not self.username and self.email:
            self.username = username_from_email(self.email)
        if not self.username:
            self.username = 'NA'

    def clean(self):
        """Ensure that the email is unique if provided."""
        if self.email and CustomerUser.objects.exclude(pk=self.pk).filter(email=self.email).exists():
            raise ValidationError(f"Email '{self.email}' is already in use.")
        if self.phone and CustomerUser.objects.exclude(pk=self.pk).filter(phone=self.phone).exists():
            raise ValidationError(f"Phone number '{self.phone}' is already in use.")


class Cart(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    product = models.ForeignKey('blackpearl_admin.Product_Varients', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Default to 1 if not specified
    display_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2)
    pro_price_with_dis = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'
        unique_together = ['user', 'product']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product}"

    def get_total_price(self):
        """Calculate total price considering the offer price."""
        return self.pro_price_with_dis if self.pro_price_with_dis else self.display_price


class TotalCart(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    total_display_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_pro_price_with_dis = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_quantity = models.PositiveIntegerField(default=0)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'total_cart'
        verbose_name = 'Total Cart'
        verbose_name_plural = 'Total Carts'

    def __str__(self):
        return f"Total Cart for {self.user.username}"


class CustomerLog(models.Model):
    user = models.CharField(max_length=100)
    activity = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

