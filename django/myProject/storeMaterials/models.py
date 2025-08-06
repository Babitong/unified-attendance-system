from django.db import models

# Create your models here.


class Electronics(models.Model):
    ProductName = models.CharField(max_length=30)

    Product_Type = models.CharField(max_length=30)
    Price = models.IntegerField(default=0)
    # address = models.CharField(max_length=30)
    # town = models.CharField(max_length=30)
    # photo = models.CharField(max_length=30)
    # idOrBirthCertificate = models.CharField(max_length=30)

    # contactPhone = models.CharField(max_length=30)

    # birth_date = models.DateTimeField("birth date")
    entry_date = models.DateTimeField("entry date")

    remarks = models.TextField()

    def __str__(self):
         return self.ProductName + "." + self.Product_Type
