from django.db import models

# Create your models here.


class Student(models.Model):
    firstName = models.CharField(max_length=30)

    lastName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    town = models.CharField(max_length=30)
    photo = models.CharField(max_length=30)
    idOrBirthCertificate = models.CharField(max_length=30)

    contactPhone = models.CharField(max_length=30)

    birth_date = models.DateTimeField("birth date")
    entry_date = models.DateTimeField("entry date")

    remarks = models.TextField()

    def __str__(self):
         return self.lastName + "." + self.firstName
