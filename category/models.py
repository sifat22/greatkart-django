from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(unique=True,max_length=200)
    description=models.TextField(max_length=225,blank=True)
    cat_image=models.ImageField(upload_to='media/categories',blank=True)

    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    #get url form app store url and showing category details in one page
    def get_url(self):
            return reverse('store:categories_item',args=[self.slug])


    def __str__(self):
        return self.category_name
