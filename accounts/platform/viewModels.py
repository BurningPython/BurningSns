class ViewModel(object):
    """
    视图模型基类
    """
    site = ''                        #社交缩写名称
    site_name = ''                  #社交网络中文全名
    created_at = ''                #创建时间
    id = 0                            #内容ID

class Status(ViewModel):
    """
    docstring for News
    """

    def __init__(self):
        pass

    mid = 0                            #内容MID
    idstr = ''                        #字符串型的微博ID
    text = ''                        #微博信息内容
    source = ''                        #微博来源
    source_url =''                  #来源url
    favorited = False                #是否已收藏
    truncated = False                #是否被截断
    in_reply_to_status_id = ''        #回复ID
    in_reply_to_user_id = ''        #回复人UID
    in_reply_to_screen_name = ''    #回复人昵称
    thumbnail_pic = ''                #缩略图地址,没有时不返回此字段

    bmiddle_pic = ''                    #中等尺寸图片地址，没有时不返回此字段
    original_pic = ''                #原始图片地址，没有时不返回此字段
    geo = ''                        #地理信息字段 详细
    uid = 0                         #用户id
    user = ''                        #微博作者的用户名字段
    nick = ''                       #用户的昵称
    head_pic = ''                   #用户头像
    retweeted_status = ''            #被转发的原微博信息字段，当该微博为转发微博时返回 详细
    reposts_count = 0                #转发数
    comments_count = 0                #评论数
    attitudes_count = 0                #表态数
    mlevel = 0                        #暂未支持
    visible = 0                    #微博的可见性及指定可见分组信息。该object中type取值，0：普通微博，1：私密微博，3：指定分组微博，4：密友微博；list_id为分组的组号
    pic_urls = ''                    #微博配图地址。多图时返回多图链接。无配图返回“[]”
    ad = []                            #微博流内的推广微博ID
    is_self = False                    #是否是自己发的微博

class Comment(ViewModel):
    """docstring for Comment"""

    def __init__(self):
        pass

    text = ''            #评论的内容
    source = ''            #评论的来源
    source_url = ''
    uid = 0
    user = ''            #评论作者的用户信息字段 详细
    nick = ''
    mid = ''            #评论的MID
    idstr = ''            #字符串型的评论ID
    status = ''            #评论的微博信息字段 详细
    reply_comment = ''    #评论来源评论，当本评论属于对另一评论的回复时返回此字段

class Topic(ViewModel):
    """
    话题模型  话题就是 #topic#
    """
    def __init__(self):
        pass

    favorite_num = 0     #被收藏次数,
    status_num = 0   #话题下微博总数,
    title = ''       #话题名字,

class HotData(object):
    """
    这是面向UI层的请求相应数据包类
    由于请求有可能面向多个平台,因此每个请求都可能同时存在 失败 和 成功,
    所以把请求失败的错误记录放在一个errors列表中,列表中的每个元素都是
    一个字典,记录错误来源(site),错误码(code)和描述(message),以便对
    用户做出提醒或是其他操作.
    所有成功的请求数据均以统一的模型存放在data列表中
    """

    data = []
    errors = []

    def __init__(self,data = None, error = None):
        """
        初始化
        """
        self.data = []
        self.errors = []

        if data:
            self.data.append(data)
        if error:
            self.errors.append(error)

    def set_error_flag(self, response):
        """
        合并DataResponse
        """
        if not isinstance(response, DataResponse):
            raise Exception("参数response的类型必须为DataResponse")

        error = {
            'code': response.code,
            'site': response.site,
            'message': response.message
        }
        self.errors.append(error)

        return self

class DataResponse(object):
    """
    这是每个平台基本接口请求数据后返回的数据包
    """

    data = []
    code = ""
    message = ""
    site = ""
    ret = 0

    def __init__(self, ret = 0, code = 0, message = "", site="unknow", data = None):
        """
        ret:0为正常,1为错误
        code:错误编码
        message:错误描述
        data:数据
        """
        self.ret = ret
        self.code = code
        self.message = message
        self.site = site
        if data:
            self.data = data