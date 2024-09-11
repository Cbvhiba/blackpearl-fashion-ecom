from django import forms
from django.core.exceptions import ValidationError
from .models import *

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'

    def clean_images(self):
        image = self.cleaned_data.get('images')
        if image:
            # Check image dimensions
            from PIL import Image
            img = Image.open(image)
            width, height = img.size
            if width != 1366 or height != 800:
                raise ValidationError("Image dimensions must be 1366x800 pixels.")
        return image
    

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

    def clean_images(self):
        image = self.cleaned_data.get('icon')
        if image:
            # Check image dimensions
            from PIL import Image
            img = Image.open(image)
            width, height = img.size
            if width != 150 or height != 150:
                raise ValidationError("Image dimensions must be 150x150 pixels.")
        return image


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def clean_images(self):
        image = self.cleaned_data.get('images')
        if image:
            # Check image dimensions
            from PIL import Image
            img = Image.open(image)
            width, height = img.size
            if width != 500 or height != 400:
                raise ValidationError("Image dimensions must be 500x400 pixels.")
        return image