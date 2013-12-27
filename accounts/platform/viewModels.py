class Status(object):
    """
    docstring for News
    """

    def __init__(self, id):
        self.id = id

    site = ''                        #社交网站名称
    created_at = ''                #微博创建时间
    id = 0                            #微博ID
    mid = 0                            #微博MID
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

class Comment(object):
    """docstring for Comment"""

    def __init__(self):
        pass

    site = ''            #社交网站名称
    created_at = ''        #评论创建时间
    id = 0                #评论的ID
    text = ''            #评论的内容
    source = ''            #评论的来源
    user = ''            #评论作者的用户信息字段 详细
    mid = ''            #评论的MID
    idstr = ''            #字符串型的评论ID
    status = ''            #评论的微博信息字段 详细
    reply_comment = ''    #评论来源评论，当本评论属于对另一评论的回复时返回此字段
