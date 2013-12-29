from datetime import datetime

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
    )


class MyUserManager(BaseUserManager):
    """
    
    """

    def create_user(self, username, email, password = None):
        """
        创建用户
        """
        if not username:
            raise ValueError('用户名是必须的')
        user = self.model(
            username = username,
            email = self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        创建管理员用户
        """
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name = "用户名",
        max_length = 255,
        unique = True,
        db_index = True,
    )
    email = models.EmailField(
        verbose_name = "Email地址",
        max_length = 255,
        unique = True,
        db_index = True,
    )
    nickname = models.CharField(
        verbose_name = "昵称",
        max_length = 255,
        blank = True,
    )
    ip_address = models.CharField(
        verbose_name = "IP地址",
        max_length = 128,
        blank = True,

    )

    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj = None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Token(models.Model):
    user = models.ForeignKey(User)
    site = models.CharField(max_length = 255)
    access_token = models.CharField(max_length = 255)
    refresh_token = models.CharField(max_length = 255)
    expires_in = models.IntegerField()
    openid = models.CharField(max_length = 255)
    update_on = models.DateTimeField(default = datetime.now())
    enable = models.BooleanField(default = True)

    @property
    def is_overdue(self):
        """
        是否已经过期
        """
        now = datetime.now()
        delta = datetime.timedelta(seconds = self.expires_in)

        if self.update_on + delta >= now:
            return True
        else:
            return False

    @property
    def is_overdue_soon(self):
        """
        是否将在3天内过期
        """
        now = datetime.now()
        delta = datetime.timedelta(days = 3, seconds = self.expires_in)

        if (not self.is_overdue) and (self.update_on + delta >= now):
            return True
        else:
            return False

    REQUIRED_FIELDS = [site, access_token, refresh_token]

    def __str__(self):
        mstr = self.site + ":" + self.user.username
        return mstr


if __name__ == "__main__":
    pass
