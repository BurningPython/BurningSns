'''
Created on 2013年12月18日

@author: july
'''
from urllib.error import URLError,HTTPError 
from urllib.request import urlopen
import json

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


if __name__ == '__main__':
    pass
