from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='User', blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Avatar')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        permissions = [
            ('user_view', 'User View')
        ]