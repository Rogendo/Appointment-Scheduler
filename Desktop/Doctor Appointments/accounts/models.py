from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.utils import UserManager


class CustomUser(AbstractUser):
    TYPE_CHOICES = (("", "Select"), ("doctor", "doctor"), ("user", "user"))
    username = None
    email = models.EmailField(("email address"), unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    bio = models.TextField()
    phone_number = models.CharField(max_length=10, default="07XXXXXXXX")
    user_type = models.CharField(max_length=90, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "users"

