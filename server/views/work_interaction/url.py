from django.urls import path

from .add_comment import AddComment
from .collect import Collect
from .comment_section import AddCommentSection, GetCommentSection
from .get_comment_list import GetCommentList
from .get_more_main_comment import GetMoreMainComment
from .get_more_reply_comment import GetMoreReplyComment
from .like import Like
from .watch import Watch
from .like_comment import LikeComment

urlpatterns = [
    path('Watch/', Watch.as_view(), name='Watch'),
    # 作品观看记录
    path('Like/', Like.as_view(), name='Like'),
    # 作品点赞记录
    path('Collect/', Collect.as_view(), name='Collect'),
    # 作品收藏记录
    path('AddCommentSection/', AddCommentSection.as_view(), name='AddCommentSection'),
    # 新增评论
    path('GetCommentSection/', GetCommentSection.as_view(), name='GetCommentSection'),
    # 获取评论
    path('LikeComment/', LikeComment.as_view(), name='LikeComment'),
    # 点赞评论
    path('AddComment',AddComment.as_view(),name='AddComment'),
    # 新增评论
    path('GetCommentList', GetCommentList.as_view(),name='GetCommentList'),
    # 获取评论列表
    path('GetMoreMainComment', GetMoreMainComment.as_view(),name='GetMoreMainComment'),
    # 获取更多主评论
    path('GetMoreReplyComment', GetMoreReplyComment.as_view(),name='GetMoreReplyComment'),
    # 获取更多回复评论
]
