from django.urls import path

from .GetAllWorkData import GetAllWorkData
from .GetAppointWorkData import GetAppointWorkData

urlpatterns=[
    path('GetAllWorkData/',GetAllWorkData.as_view(),name='GetAllWorkData'),
    #获取作者的所有作品数据以及历史数据
    path('GetAppointWorkData/',GetAppointWorkData.as_view(),name='GetAppointWorkData'),
    #获取指定作品数据
]