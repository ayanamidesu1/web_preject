from django.urls import path
from .views import recommend

urlpatterns=[
    path('recommentd/',recommend.as_view(),name='recommend'),
    #推荐作品的请求接口
]