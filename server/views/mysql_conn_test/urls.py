# views/mysql_conn_test/urls.py
from django.urls import path
from .views import TestDBConnectionView

urlpatterns = [
    path('test-db/', TestDBConnectionView.as_view(), name='test_db_connection'),
]
