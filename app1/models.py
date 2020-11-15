
from django.db import models
import re	
from datetime import datetime 
# Create your models here.
class UserManager(models.Manager):
    def fields_required_validator(self, postData):
        errors = {}
        for key, value in postData.items():
            if len(value) <= 0:
                errors[key] = f'{key} is a required field '
        return errors
    def fields_max_length_validator(self, postData):
        errors = {}
        if 0 < len(postData['first_name']) < 2 :
            errors["first_name"] = " First name should be at least 2 characters"
        if 0 < len(postData['last_name']) < 2 :
                errors["last_name"] = " Last name should be at least 2 characters"
        if 0 < len(postData['password'])  < 8 :
            errors["password"] = " Password should be at least 8 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    
            errors['email'] = "Invalid email address!"
        return errors
    def confirm_password(self, postData):
        errors = {}
        if postData['confirm_password'] != postData['password']:
            errors["confirm_password"] = "You enterd a different password,please confirm your password"
        return errors
class WishManager(models.Manager):
    def fields_required_validator(self, postData):
        errors = {}
        if len(postData['item']) <= 0:
                errors['item'] ="Item is a required field "
        if len(postData['desc']) <= 0:
                errors['desc'] ="Description  is a required field "
        return errors
    def fields_max_length_validator(self, postData):
        errors = {}
        if 0 < len(postData['item']) < 3 :
            errors["item"] = " Item should be at least 3 characters"
        if 0 < len(postData['desc']) < 3 :
            errors["desc"] = " Description should be at least 3 characters"
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    salt = models.CharField(max_length=255)
    objects = UserManager()

class PendingWish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.CharField(max_length=255,default=" ")
    wisher = models.ForeignKey(User, related_name="pending_wishes",on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
class GrantedWish(models.Model):
    item = models.CharField(max_length=255)
    number_of_likes = models.IntegerField(default= 0)
    desc = models.CharField(max_length=255,default=" ")
    wisher = models.ForeignKey(User, related_name="granted_wishes",on_delete = models.CASCADE)
    the_time_wish_was_created=models.DateTimeField(default=datetime.now())
    users_who_like_this_wish= models.ManyToManyField(User, related_name="liked_wishes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

