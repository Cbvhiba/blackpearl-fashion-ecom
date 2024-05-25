from django.db import models
from blackpearl_web_py.utils import unique_slug_generator,BaseModel
from django_lifecycle import LifecycleModelMixin, hook,LifecycleModel,\
    BEFORE_CREATE,AFTER_CREATE,AFTER_UPDATE,BEFORE_SAVE
from django.utils.text import slugify
import os
from ckeditor.fields import RichTextField


# Create your models here.

class Category(BaseModel):
    Category_Name = models.CharField(max_length=255)
    Category_img = models.FileField(upload_to='category') 
    Parent = models.ForeignKey('Category',on_delete=models.CASCADE,null=True,blank=True)
    Description = models.TextField(blank=True,null=True)
    slug = models.SlugField(blank=True)
    class Meta:
        db_table = "Category"
    def __str__(self) -> str:
        return self.Category_Name
    
    @hook(BEFORE_SAVE)
    def before_create(self):
        self.slug = unique_slug_generator(self,self.Category_Name)

class Brand(BaseModel):
    brand = models.CharField(max_length=100)
    icon = models.FileField(upload_to='brand/icon')
    slug = models.SlugField(blank=True)
    def __str__(self) -> str:
        return self.brand
    
    @hook(BEFORE_CREATE)
    def before_create(self):
        self.slug = unique_slug_generator(self,self.brand)

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

class Product(BaseModel):
    Name = models.CharField(max_length=250)
    Varient_Type = models.ManyToManyField(Varient_Type,blank=True)
    Product_Category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    Product_Brand = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    Description = models.TextField(blank = True, null = True)
    Features = models.TextField(blank = True, null = True)
    Related_Products = models.ManyToManyField('Product',blank=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL,null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True,null=True)
    class Meta:
        db_table = "Products"
    def __str__(self) -> str:
        return self.Name
    
    @hook(BEFORE_CREATE)
    def before_create(self):
        self.slug = unique_slug_generator(self,self.Name)
    
# # pre_save.connect(pre_save_receiver_product, sender = Product)
    
# """
# <<<<<<<<<<<<<<<end of slugify product>>>>>>>>>>>>>>>>>>>>
# """

class Product_Varients(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product varients")
    Varient_Values = models.ManyToManyField(Varient_Values,blank=True,related_name='values')
    Images = models.ImageField(upload_to='Products')
    discount_Prize = models.FloatField(default=0)
    Display_Prize = models.DecimalField(max_digits=12,decimal_places=2)
    Product_stock = models.PositiveIntegerField(blank=True,null=True)
    SKU_code = models.CharField(max_length=255)
    # Product_Offers = models.ManyToManyField(Offers,blank=True)
    
    slug = models.SlugField(max_length=255, blank=True,null=True)

    
    class Meta:
        db_table = "Product_Varients"
        
    @hook(AFTER_CREATE)
    def set_slug(self):
        slug = f'{self.product.Name} ' + '-'.join([i.Varient_Values for i in self.Varient_Values.all()]) + f'_{self.uid}'
        self.slug = slugify(slug)
        self.save()
    
    def discount(self):
        if self.discount_Prize > 0:
            discounted_price = self.Display_Prize - self.Display_Prize * self.discount_Prize / 100
            return discounted_price
    
# class Item_Images(models.Model):
#     Product_Owner = models.ForeignKey(Product_Varients,on_delete=models.CASCADE)
#     Images = models.FileField(upload_to='Products')
#     class Meta:
#         db_table = 'Item_images'

#     def filename(self):
#         return os.path.basename(self.Images.name)
    