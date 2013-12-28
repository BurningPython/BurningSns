__author__ = 'july'

from accounts.platform.viewModels import HotData

def data_integration(services, call_name, compare_key="created_at", data_size=40, **params):
    """
    数据整合  返回的数据都按key从大到小排序

    services:服务列表
    call_name:获取数据的方法名称
    key:排序关键字  默认'created_at'
    data_size:获取数据的容量 默认40
    params:请求的参数
    """

    if not isinstance(services, dict):
        raise Exception("services 必须是一个成员类型为服务的字典")
    #单个平台的预读取数据量,之后可以看情况设置
    size = data_size / len(services) * 2
    params['size'] = size

    retdata = HotData()
    data_store = {}
    for key in services:
        service = services[key]
        if hasattr(service, call_name):
            call = getattr(service, call_name)
            response_data = call(**params)
        else:
            continue
        #获取第一批数据
        if response_data.ret == 0 and len(response_data.data) > 0:
            data_store[key] = response_data.data
        #如果第一批数据获取失败,则认为该绑定可能已经失效,之后不再获取
        else:
            retdata.set_error_flag(response_data)

    while len(retdata.data) <= data_size and data_store:
        to_insert = None
        this_site = ""
        for sname in data_store:
            d = data_store[sname][0]
            if not to_insert:
                to_insert = d
                this_site = sname
            else:
                if hasattr(d,compare_key) and hasattr(to_insert,compare_key):
                    d_key = getattr(d,compare_key)
                    to_insert_key = getattr(to_insert,compare_key)
                else:
                    raise Exception("元素缺少用来比较大小的Key属性:%s" % compare_key)
                if d_key > to_insert_key:
                    to_insert = d
                    this_site = sname
        retdata.data.append(to_insert)
        ds = data_store[this_site]
        #删除这个已插入的数据
        del ds[0]
        #如果数据已经取完了,则再获取一批数据
        if not ds:
            #向下翻页标识
            params['page_flag'] = 1
            #最后一次插入的数据,各自的接口中可以根据这里的数据来进行分页
            params['last_data'] = to_insert
            call = getattr(services[this_site], call_name)
            response_data = call(**params)
            if response_data.ret == 0 and len(response_data.data) > 0:
                data_store[this_site] = response_data.data
            #如果此时获取数据失败,则不再继续尝试获取该平台的数据,以免发生错误
            else:
                del data_store[this_site]
    #返回一个类型为HotData的对象
    return retdata

if __name__ == "__main__":
    pass