from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyAccountManager(BaseUserManager):
    def create_user(self, username, password=None, is_owner_of_shop=False, shop_working_at=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            is_owner_of_shop=is_owner_of_shop,
            shop_working_at=shop_working_at,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, is_owner_of_shop):
        user = self.create_user(
            username=username,
            password=password,
            is_owner_of_shop=is_owner_of_shop,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    shop_working_at = models.ForeignKey('shops.Shop', on_delete=models.DO_NOTHING, null=True, blank=True)
    is_owner_of_shop = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
