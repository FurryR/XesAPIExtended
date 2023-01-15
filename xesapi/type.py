from typing import TypedDict, Literal, TypeVar
class Info_Data(TypedDict):
    """
    学而思回传的 InfoData。
    """

    auth: str  # 未知
    avatar_default: int  # 未知
    avatar_path: str  # 头像链接
    avatar_version: str  # 头像上传日期（Unix 时间戳）
    bussinessline_id: int  # 未知
    create_time: str  # 账户创建时间
    email: str  # email
    en_name: str  # 英文名
    encrypt_user_id: str  # 未知
    grade_alias: str  # 别名，参照 grade_id 和 grade_name
    grade_id: int  # 学历
    grade_name: str  # 人类可读学历
    id: str  # 学员 ID
    name: str  # 同 id
    nickname: str  # 昵称
    realname: str  # 真名
    role: str  # 未知
    sex: str  # 性别(参照 API 返回结果)
    status: str  # 未知
    tal_cg_id: int  # 未知
    tal_id: str  # 好未来 ID
    uid: str  # 账户的 UID（不是学员 ID）
    user_id: str  # 同 id
    xes_encrypt_uid: str  # 加密了的 UID

class TalToken_Data(TypedDict):
    """
    TalToken 的内部 data。
    """

    code: str  # 唯一标识符，可以在 https://login.xueersi.com/V1/Web/getToken 使用。
    passport_token: str  # 好未来 token，用于 Cookie（tal_id）。


class Captcha_Data(TypedDict):
    """
    Captcha 的内部 data。
    """

    captcha: str  # base64 url, data:image\\/jpeg;base64,...

class Asset_Data(TypedDict):
    """
    Assets 的内部 data。
    """
    asset: list
    assets_url: str # assets 的 json url
    cdn: list[str] # cdn
    hide_filelist: bool
    index_file: None

class Work_Data(TypedDict):
    """
    作品的内部 data。
    """
    adapter: str
    asset: Asset_Data
    audio: str
    category: int
    code_complete: int
    code_complete_json: None
    comments: int # 评论数
    created_at: str # 创建时间
    created_source: str
    deleted_at: str # 删除时间(?)
    description: str # 作品介绍
    favorites: int # 收藏数
    hidden_code: int
    id: int # id
    is_cooperation: int
    lang: str # 语言(不确定未来会不会加新的)
    likes: int # 赞数
    live_id: None
    manual_weight: int # 手动权重(判断是否被限流)
    modified_at: str # 最后更新日期
    name: str # 作品
    original_id: int
    popular_score: int
    project_type: str
    published: int # 是否发布
    published_at: str # 发布时间
    removed: int # 是否被删除
    source: str
    source_code_views: int # 改编数
    tags: str # tags
    template_project_id: None
    thumbnail: str # 作品封面
    topic_id: str # 作品对应的评论区ID
    type: str
    unlikes: str # 踩数
    updated_at: str # 数据时间
    user_avatar: str # 用户的头像
    user_id: int # 用户的 id
    username: str # 用户的名字
    version: str
    video: str
    views: int # 观看数
    weight: int # 权重

class Reply_Data(TypedDict):
    can_delete: bool # 可否删除
    can_top: Literal[False] # 可否置顶(若智后端)
    comment_from: str
    content: str # 回复内容
    created_at: str # 创建时间
    emojis: None # 暂不支持emojis
    id: int # 回复ID
    is_like: bool # 是否已喜欢
    is_topic_author_like: bool # 是否被作者喜欢
    is_topic_author_reply: bool # 是否被作者回复
    is_unlike: bool # 是否被踩
    likes: int # 喜欢数
    links: None # 没屁用
    parent_id: int # 父评论 id
    removed: bool # 是否被删除
    reply_user_id: str # 回复目标评论的作者的ID
    reply_username: str # 回复目标评论的作者的用户名
    target_id: int # 回复目标的id(可能是评论也可能是回复)
    topic_id: str # topic id
    unlikes: int # 踩数
    user_avatar_path: str # 回复作者的头像链接
    user_id: str # 回复作者的id
    user_profile: None # 暂不支持获得奖牌
    username: str # 回复作者的昵称

class ReplyList_Data(TypedDict):
    """
    回复列表的内部 data
    """
    data: list[Reply_Data]
    hasMore: bool # 展开
    total: int # 总共的回复数

class Comment_Data(TypedDict):
    """
    评论内部 Data
    """
    can_delete: bool # 可否删除
    can_top: bool # 可否置顶
    comment_from: str
    content: str # 评论内容
    create_at: str # 创建时间
    emojis: None # 暂不支持emojis
    id: int # 评论id
    is_like: bool # 是否喜欢此条评论
    is_topic_author_like: bool # 是否被作者喜欢
    is_topic_author_reply: bool # 是否被作者回复
    is_unlike: bool # 是否喜欢这条评论
    likes: int # 赞数
    links: None # 没屁用
    removed: int # 是否被删除
    replies: int # 回复数
    reply_list: ReplyList_Data # 回复列表
    top: int # 是否被置顶
    topic_id: str # 话题 ID
    unlikes: int # 踩数
    user_avatar_path: str # 用户头像
    user_id: str # 用户ID
    user_profile: None # 暂不支持奖牌获取
    username: str # 用户名
    
GetComment_Data_Element = TypeVar("GetComment_Data_Element")
class GetComment_Data(TypedDict):
    data: list[GetComment_Data_Element] # 当前页面的 Comment_Data
    page: str # 当前页数
    per_page: str # 每页数量