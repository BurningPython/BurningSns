__author__ = 'july'


def parse_params(**params):
    pass


def unparse_params(pramStr):
    ret_dic = {}
    for pair in pramStr.split("&"):
        key_value = pair.split("=")
        ret_dic[key_value[0]] = key_value[1]
    return ret_dic


def get_client_ip(request):
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