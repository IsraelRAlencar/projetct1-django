from django.db import models
from django.contrib.auth import get_user_model
from utils.delete_media_files import delete_files_in_folder
from project.settings.assets import MEDIA_ROOT

User = get_user_model()


def user_directory_path(instance, filename):
    delete_files_in_folder(f'{MEDIA_ROOT}\\authors\\profiles\\{instance.author.pk}') # noqa E501
    return f'authors/profiles/{instance.author.pk}/{filename}'


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    profile_cover = models.ImageField(
        upload_to=user_directory_path,
        blank=True, default=''
    )
