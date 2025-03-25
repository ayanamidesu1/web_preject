# djangoWebServer/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from djangoWebServer.register import register

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('mysql_conn_test/', include('views.mysql_conn_test.urls')),
    path('GetUserInfo/', include('views.GetUserInfo.url')),
    path('file/', include('views.upload.url')),
    path('notice_control/', include('views.notice_control.url')),
    path('novel/', include('views.novel.url')),
    path('get_work_info/', include('views.get_work_info.url')),
    path('work_interaction/', include('views.work_interaction.url')),
    # 作品互动的主接口
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('update/',include('views.update_userinfo.url')),
    #更新操作接口的入口
    path('recommend/',include('views.recommend.url')),
    #推荐系统
    path('rank_list/',include('views.rankling_list.url')),
    #排行榜
    path('data_analysis/',include('views.data_analysis.url')),
    #数据分析
    path('admin_control/',include('views.background_control.url')),
    #管理员后台管理
    path('get_browse_history/',include('views.get_browse_history.url')),
    #获取浏览记录
    path('register/',register.as_view(),name='register'),
    # 注册接口
]
