from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=300)
    cat_image = models.ImageField(upload_to='photos/category/', blank=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'