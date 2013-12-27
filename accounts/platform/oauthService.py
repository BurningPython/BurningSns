'''
处理第三方登录的操作

Created on 2013年12月12日

@author: july
'''

from django.core.exceptions import ObjectDoesNotExist

from accounts.models import OpenAuth, User
from accounts.platform.tokenService import TokenService


class OpenAuthService(object):
    
    def __init__(self,site,**args):
        """
        根据site名称和accesstoken相关的参数来初始化这个Service
        """
        self.site = site
        
        #这2个参数必须有
        if ('access_token' in args) and ('expires_in' in args):
            self.access_token = args['access_token']
            self.expires_in = args['expires_in']
        else:
            raise Exception("没有给定access_token和expires_in参数")
        #以下参数可能不一定有
        if 'refresh_token' in args:
            self.refresh_token = args['refresh_token']
        else:
            self.refresh_token = ""
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

    
    def get_or_create_user(self):
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
            )
        #没有匹配数据,那么新建一个用户,为该用户关联该数据
        #自动创建的账号名和密码等规则还需要进一步讨论才能确定,
        #目前暂时这么处理
        except ObjectDoesNotExist:
            #创建用户
            username = ""
            email = ""
            if self.name:
                username = self.name
                email = self.name + "@temp.com"
            else:
                username = self.openid
                email = self.openid + "@temp.com"
                #password = random.randint(100000,999999)
            password = "123456"
            new_user = User.objects.create(username=username, email=email, nickname=self.nick)
            new_user.set_password(password)
            new_user.save()
            #绑定到社交网络
            tokenService = TokenService(new_user)
            tokenService.addToken(
                self.site,
                access_token=self.access_token,
                refresh_token=self.refresh_token,
                expires_in=self.expires_in,
                openid=self.openid,
                )
            user = new_user
            retdic["password"] = password
        #否则获取该数据的对应用户
        else:
            user = oauth.user
        #为user添加backend,用于将用户寄存在session中
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        retdic["user"] = user
        return retdic

    
if __name__ == '__main__':
    pass
