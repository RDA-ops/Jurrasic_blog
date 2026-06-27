from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, verbose_name="О себе")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    notify_new_articles = models.BooleanField(default=True, verbose_name="Уведомлять о новых статьях")

    def __str__(self):
        return f'Профиль {self.user.username}'
