from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
# Create your models here.

class Hospital(models.Model):
    hosId = models.IntegerField(primary_key=True)
    hosName = models.CharField(max_length=50)
    address = models.CharField(max_length=50,null=True,blank=True)
    hosImage = models.ImageField(null=True, blank=True, upload_to='images/')
    hosLat = models.FloatField()
    hosLong = models.FloatField()
    contact = models.CharField(blank=True,null=True,max_length=15)
    TYPES = (
        ('Government','Government'),
        ('Private','Private'),
    )
    hosType = models.CharField(max_length=50, choices=TYPES)
    CAT = (
            ('Orthopedics','Orthopedics'),
            ('Cardiology','Cardiology'),
            ('Neurology','Neurology'),
            ('Oncology','Oncology'),
            ('Pediatrics','Pediatrics'),
            ('Dermatology','Dermatology'),
            ('Gastroenterology','Gastroenterology'),
            ('Gynecology','Gynecology'),
            ('Psychiatry','Psychiatry'),
            ('Ophthalmology','Ophthalmology'),
            ('Pulmonology','Pulmonology'),
            ('Nephrology','Nephrology'),
    )
    hosSpec = ArrayField(models.CharField(max_length=50,choices=CAT))
    def __str__(self) :
        return self.hosName

class Preference(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   preferred_hosp = models.ForeignKey(Hospital, on_delete=models.CASCADE, to_field='hosId')
    

class Schedule(models.Model):
    date = models.DateField(null=False)
    hosp = models.ForeignKey(Hospital, on_delete=models.CASCADE, to_field='hosId')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.CharField(max_length=100, null=True, blank=True)

class UserResponse(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField(max_length=500)