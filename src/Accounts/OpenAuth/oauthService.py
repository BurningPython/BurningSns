'''
处理第三方登录的操作

Created on 2013年12月12日

@author: july
'''
import random
from Accounts.models import OpenAuth,MyUser
from django.core.exceptions import ObjectDoesNotExist
class OpenAuthService(object):
    
    def __init__(self,site,**args):
        """
        根据site名称和accesstoken相关的参数来初始化这个Service
        """
        self.site = site
        
        #这3个参数必须有
        if 'access_token' and 'refresh_token' and 'expires_in' in args:
            self.access_token = args['access_token']
            self.refresh_token = args['refresh_token']
            self.expires_in = args['expires_in']
        else:
            #should raise something excption...
            pass
        #以下参数可能不一定有
        if 'openid' in args:
            self.openid = args['openid']
        else:
            self.openid = ""
        if 'name' in args:
            self.name = args['name']
        else:
            self.name = ""
        if 'nick' in args:
            self.nick = args['nick']
        else:
            self.nick = ""

    
    def getUser(self):
        """
        返回一个字典:
        user:保存用户实体对象
        password:只在用户被系统自动创建时返回,否则为空
        """
        retdic = {}
        #尝试获取oauth,以此来得到对应的用户
        try:
            oauth = OpenAuth.objects.get(
                site = self.site,
                access_token = self.access_token,
                refresh_token = self.refresh_token,
                openid = self.openid
            )
        #没有匹配数据,那么新建一个用户,为该用户关联该数据
        #自动创建的账号名和密码等规则还需要进一步讨论才能确定,
        #目前暂时这么处理
        except ObjectDoesNotExist:
            #创建用户
            email = self.name + "@temp.com"
            #password = random.randint(100000,999999)
            password = "123456"
            new_user = MyUser.objects.create(username = self.name,email = email, nickname = self.nick)
            new_user.set_password(password)
            new_user.save()
            #绑定到社交网络
            self.bindOrUpdateOpenAuth(self.name)
            user = new_user
            retdic["password"] = password
        #否则获取该数据的对应用户
        else:
            user = oauth.user
        #为user添加backend,用于将用户寄存在session中
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        retdic["user"] = user
        return retdic


    
    def isUserBindedSite(self,username):
        """
        检查用户是否已经绑定到指的社交平台
        如果是,返回openauth对象,否则返回None
        """
        try:
            oauth = OpenAuth.objects.get(username = username,site = site)
        except ObjectDoesNotExist:
            return None
        else:
            return oauth
        
    def bindOrUpdateOpenAuth(self,username):
        """
        更新用户的绑定信息(比如access_token),如果用户没有绑定对应社交网络,则创建绑定
        """
        oauth = self.isUserBindedSite(username)
        #如果已经存在该openAuth,则更新
        if oauth:
            oauth.update(
                site = self.site,
                access_token = self.access_token,
                refresh_token = self.refresh_token,
                expires_in = self.expires_in,
                openid = self.openid
            )
            oauth.save()
        #如果不存在这个openAuth,则继续
        else:
            user = MyUser.objects.get(username = username)
            user.openauth_set.create(
                site = self.site, 
                access_token = self.access_token,
                refresh_token = self.refresh_token,
                expires_in = self.expires_in,
                openid = self.openid
            )
            user.save()
        
    
if __name__ == '__main__':
    pass
