from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    users = models.CharField(max_length=264,default="")
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)
    face_encode=models.TextField(null=True)
    def __str__(self):
        return self.users

        # Built-in attribute of django.contrib.auth.models.User !


#class Transact(models.Model):
class Transaction_Pairs(models.Model):
    person1=models.CharField(max_length=264)
    person2=models.CharField(max_length=264)
    amount=models.FloatField(null=True)
    grp_pic=models.ImageField(upload_to='profile_pics',blank=True,default= "default.jpg")

    def __str__(self):
        return self.person1 +" "+self.person2 + " "

class Transaction_history(models.Model):
    person1=models.CharField(max_length=264,default=" ")
    person2=models.CharField(max_length=264,default=" ")
    date= models.DateTimeField( auto_now_add=True, null=True)
    reason=models.CharField(max_length=264)
    amount=models.FloatField(null=True)
    def __str__(self):
        return self.person1 +" "+self.person2 + " "+self.reason
