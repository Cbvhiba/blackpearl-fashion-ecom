from django.db import models
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_CREATE
from django.utils.text import slugify
from django.core.exceptions import ValidationError

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
    password = models.CharField(max_length=128, blank=True, null=True)  # Extended length for hashed passwords
    is_active = models.BooleanField(default=True)
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

