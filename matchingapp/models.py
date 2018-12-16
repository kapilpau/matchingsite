from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Hobby model has a name field
class Hobby(models.Model):
    name = models.TextField(max_length=200)

    def __str__(self):
        return self.name


# Profile model has a number of fields
# and there is a OneToOne relationship between Member and Profile where a Member might not have a Profile.
# There is a ManyToMany relationship with Hobby.
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

    def __str__(self):
        return self.name


# Django's User model already has username and password
# both of which are required fields, so Member inherits
# these fields. It has ManyToMany relationships with itself
# representing matches and match requests
class Member(User):
    isAdmin = models.BooleanField(default=False)
    profile = models.OneToOneField(
        to=Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    matches = models.ManyToManyField(
        to='self',
        symmetrical=True,
        blank=True
    )
    match_requests = models.ManyToManyField(
        to='self',
        symmetrical=False,
        blank=True
    )


# Conversation model has a name and a ManyToMany relationship with
# Member representing the participants of the conversation
class Conversation(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    participants = models.ManyToManyField(
        to=Member,
        blank=True,
        symmetrical=False
    )


# Message model has ForeignKey relationships with Conversation and Member
# representing the conversation the message is in and the user who sent it.
# It also has a ManyToMany relationship with Member representation the users
# who have read the message
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    read_by = models.ManyToManyField(
        to=Member,
        related_name='ready_by',
        symmetrical=False
    )
    sent_at = models.DateTimeField(default=datetime.now, blank=False, null=False)
    contents = models.TextField()
