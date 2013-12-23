'''
Created on 2013年12月18日

@author: july
'''
from urllib.error import URLError,HTTPError 
from urllib.request import urlopen
import json

def urlParamToDicParam(pramStr):
    """
    用于解析如 xxx=xxx&yyy=yyy&zzz=zzz的字符串
    返回一个字典
    """
    currStr = encodingToUtf8(pramStr)
    ret_dic = {}
    for pair in currStr.split("&"):
        key_value = pair.split("=")
        ret_dic[key_value[0]] = key_value[1]
    return ret_dic

def jsonToParamDic(jsonStr):
    """
    将一串json字符串解析成字典,如果解析失败,则会返回一个空的字典
    """
    currStr = encodingToUtf8(jsonStr)
    ret_dic = {}
    try:
        ret_dic = json.loads(currStr)
    except BaseException as e:
        print(e)
        pass
    return ret_dic

def urlRead(urlStr):
    """
    相当于 urlopen(urlStr).read()
    """
    try:
        response = urlopen(urlStr)
    except URLError as e:  
        retInfo = e.code
        print('Reason',e.reason)
    else:
        retInfo = response.read()
    return retInfo

def getClientIp(request):
    """
    获取用户的ip地址
    """
    if request:
        if 'HTTP_X_FORWARDED_FOR' in request.META:  
            ip = request.META['HTTP_X_FORWARDED_FOR']  
        else:  
            ip = request.META['REMOTE_ADDR'] 
    else:
        ip = "127.0.0.1"
    return ip

def encodingToUtf8(baseStr):
    return str(baseStr,encoding="utf-8")


if __name__ == '__main__':
    pass
