'''
Created on 2013年12月12日

@author: july
'''
import random
from Accounts.models import OpenAuth,MyUser
from django.core.exceptions import ObjectDoesNotExist

class OpenAuthManager(object):
    
    def __init__(self,**args):
        self.access_token = args['access_token']
        self.refresh_token = args['refresh_token']
        self.openid = args['openid']
        self.expires_in = args['expires_in']
        self.name = args['name']
        self.nick = args['nick']
    
    def getUser(self,site):
        """
        返回一个字典:
        user:保存用户实体对象
        password:只在用户被系统自动创建时返回,否则为空
        """
        retdic = {}
        #尝试获取accessToken
        try:
            oauth = OpenAuth.objects.get(
                site = site,
                access_token = self.access_token,
                refresh_token = self.refresh_token,
                openid = self.openid
            )
        #没有匹配数据,那么新建一个用户,为该用户关联该数据
        except ObjectDoesNotExist:
            #创建用户
            email = self.name + "@temp.com"
            #password = random.randint(100000,999999)
            password = "123456"
            new_user = MyUser.objects.create(username = self.name,email = email, nickname = self.nick)
            new_user.set_password(password)
            new_user.save()
            #绑定到社交网络
            self.createOrUpdateOpenAuth(self.name,site)
            user = new_user
            retdic["password"] = password
        #否则获取该数据的对应用户
        else:
            user = oauth.user
        #为user添加backend,用于将用户寄存在session中
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        retdic["user"] = user
        return retdic
    
    def isUserBindedSite(self,username,site):
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
        
    def createOrUpdateOpenAuth(self,username,site):
        """
        更新用户的绑定信息(比如access_token),如果用户没有绑定对应社交网络,则创建绑定
        """
        oauth = self.isUserBindedSite(username,site)
        #如果已经存在该openAuth,则更新
        if oauth:
            oauth.update(
                site = site, 
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
                site = site, 
                access_token = self.access_token,
                refresh_token = self.refresh_token,
                expires_in = self.expires_in,
                openid = self.openid
            )
            user.save()
        
    
if __name__ == '__main__':
    dic = {'access_token':123, 'refresh_token':123, 'openid':534,"nick":"wyx","name":"wangwang"}
    t = OpenAuthManager(**dic)
    user = t.getUser()
    print(user)
    pass