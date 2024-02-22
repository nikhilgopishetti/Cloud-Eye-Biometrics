from django.db import models


# Create your models here.
class Shoe(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(max_length=10)
    image_url = models.URLField(max_length=500)
    description = models.TextField(max_length=50)
    phone_number = models.CharField(max_length= 15, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


