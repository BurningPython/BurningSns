__author__ = 'july'


def parse_params(**params):
    pass


def unparse_params(pramStr):
    ret_dic = {}
    for pair in pramStr.split("&"):
        key_value = pair.split("=")
        ret_dic[key_value[0]] = key_value[1]
    return ret_dic