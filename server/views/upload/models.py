# views/GetUserInfo/models.py

from django.db import models

class PlaceholderModel(models.Model):
    """一个占位模型，用于确保模型定义正常工作。"""
    name = models.CharField(max_length=100, default='Placeholder')

    def __str__(self):
        return self.name
