from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
# import os
from recipes.models import Recipe
from utils.delete_media_files import delete_file


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    delete_file(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return

    if old_instance.cover != instance.cover:
        delete_file(old_instance)
