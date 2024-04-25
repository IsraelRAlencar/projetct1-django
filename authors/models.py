from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def user_directory_path(instance, filename):
    return f'authors/profiles/{instance.author}/{filename}'


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    profile_cover = models.ImageField(
        upload_to=user_directory_path,
        blank=True, default=''
    )
