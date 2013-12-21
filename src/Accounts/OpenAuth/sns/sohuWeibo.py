'''
Created on 2013年12月19日

@author: july
'''
from Accounts.OpenAuth.utils import *
from Accounts.OpenAuth import config

class ActionHandler(object):
    '''
    用来调用API的类
    '''
    
    def __init__(self, access_token, openid, request):
        '''
        初始化
        '''
        ip = getClientIp(request)
        self.client_id = config.sw_client_id
        
#         self.api_url = config.sw_api_url
#         self.common_parm = config.sw_api_common_parm % (
#             self.client_id,
#             access_token,
#             openid,
#             ip,
#             self.oauth_version,
#             "all",
#         )
    
    def make_api_url(self,api_name,api_param):
        target_url = (self.api_url % api_name) +self.common_parm + api_param
        return target_url
    
    def home_timeline(self,pageflag = 0,pagetime = 0,reqnum = 25,type = 0,contenttype = 0):
        """
        主页时间线
        """
        #api的名称
        api_name = "statuses/home_timeline"
        #参数列表
        api_param_list = "format=%s&pageflag=%s&pagetime=%s&reqnum=%s&type=%s&contenttype=%s"
        #拼接参数列表字符串
        api_param_str = api_param_list % (
            "json",
            pageflag,
            pagetime,
            reqnum,
            type,
            contenttype,
        )
        #完整url
        target_url = self.make_api_url(api_name,api_param_str)
        #读取接口数据
        ret = urlRead(target_url)
        #将数据转换成字典返回
        return jsonToParamDic(ret) 
    
     
class TokenManager(object):
    """
    用来获取和管理 access token
    """
    def __init__(self,code):
        """
        初始化
        """
        self.client_id = config.sw_client_id
        self.app_secret = config.sw_consumer_secret
        self.code = code 
        self.redrect_uri = config.sw_redirect_uri
        
    def requestAccessToken(self):
        """
        如果获取成功,返回一个字典,包含accesstoken等信息
        如果获取失败,返回一个字典,包含errorCode和errorMsg
        """
        targetUrl = config.sw_access_token_url % (self.client_id,self.app_secret,self.code,self.redirect_uri)
        result = urlRead(targetUrl)
        return jsonToParamDic(result)
    
if __name__ == '__main__':
    url = "https://api.t.sohu.com/oauth2/authorize?client_id=QzijcaDQtONTNKv4MNE5&scope=basic&response_type=code&redirect_uri=http://127.0.0.1:8000/account/sw_oauthProcess&state=12345"
    ret = urlRead(url)
    print("ret:" + ret)
    pass