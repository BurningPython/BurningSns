from django.db import models
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from datetime import datetime
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from Accounts.OpenAuth.sns.tencentWeibo import (ActionHandler as tHandler)



class MyUserManager(BaseUserManager):
    """
    
    """
    def create_user(self, username,email, password = None):
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
    
    def create_superuser(self, username,email, password):
        """
        创建管理员用户
        """
        user = self.create_user(username,email, password)
        user.is_admin = True
        user.save(using = self._db)
        return user
    
class MyUser(AbstractBaseUser):
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
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def set_access_token(self,site_name,access_token,refresh_token,openid):
        """
        设置用户指定开放平台 的access_token,如果已经有该平台的信息,则更新,若没有,则添加
        """
        try:
            token = self.openauth_set.get(site = site_name)
        except:
            token = None
        if token:
            token.access_token = access_token
            token.refresh_token = refresh_token
            token.openid = openid
        else:
            token = self.openauth_set.create(site = site_name, access_token = access_token, refresh_token = refresh_token, openid = openid)
        
        token.save()
        
    def get_open_auth_handler(self,site_name,request = None):
        """
        获取用于操作开放平台api的handler
        """
        try:
            token = self.openauth_set.get(site = site_name)
        except:
            return None
        else:
            if site_name == "腾讯微博":
                handler = tHandler(token.access_token, token.openid, request)
            elif site_name == "新浪微博":
#                 return OpenAuth.SinaWeibo.action.ActionHandler()
                pass
            else:
                handler = None
                
            return handler
    
    
class OpenAuth(models.Model):
    user = models.ForeignKey(MyUser)
    site = models.CharField(max_length = 255)
    access_token = models.CharField(max_length = 255)
    refresh_token = models.CharField(max_length = 255)
    expires_in = models.IntegerField()
    openid = models.CharField(max_length = 255)
    update_on = models.DateTimeField(default = datetime.now())
    
    @property
    def isOverdue(self):
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
    def isOverdueSoon(self):
        """
        是否将在3天内过期
        """
        now = datetime.now()
        delta = datetime.timedelta(days = 3 ,seconds = self.expires_in)
        
        if not self.isOverdue and self.update_on + delta >= now:
            return True
        else:
            return False
    
    REQUIRED_FIELDS = [site,access_token,refresh_token]
    
    def __str__(self):
        mstr = self.site +":"+ self.user.username
        return mstr
    
if __name__ == "__main__":
    pass
