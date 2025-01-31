from django.db import models

class Donor(models.Model):
    blood_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    mobile_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    address = models.TextField()
