from django.db.models.deletion import CASCADE
from category.models import Category
from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.



class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to='media/products')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    #get details url
    def get_url(self):
        return reverse('store:product-detail',args=[self.category.slug,self.slug])

#variation manage for different color and size store in different store in  template

class VariationManger(models.Manager):
    def colors(self):
        return super(VariationManger ,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(VariationManger ,self).filter(variation_category='size',is_active=True)

variation_category_chioces=(
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_chioces)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    objects=VariationManger()

    def __str__(self):
        return self.variation_value


