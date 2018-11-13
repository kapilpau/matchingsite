from django.db import models
from django.contrib.auth.models import User

# Hobby model has a name field and an optional description
# field and has a Many-To-Many field with Profile


class Hobby(models.Model):
    name = models.TextField(max_length=200)

    def __str__(self):
        return self.name


# Profile model has a number of fields and there is
# a OneToOne relationship between Member and Profile
# where a Member might not have a Profile


class Profile(models.Model):
    profile_image = models.ImageField(upload_to='profile_images')
    name = models.TextField(max_length=40)
    email = models.TextField(max_length=100)
    gender = models.TextField(max_length=20)
    dob = models.DateField(default=False)
    hobbies = models.ManyToManyField(
        to=Hobby,
        blank=True,
        symmetrical=False
    )


# Django's User model already has username and password
# both of which are required fields, so Member inherits
# these fields


class Member(User):
    isAdmin = models.BooleanField(default=False)
    profile = models.OneToOneField(
        to=Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
