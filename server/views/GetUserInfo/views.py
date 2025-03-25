# views/GetUserInfo/views.py

from django.http import JsonResponse

from django.views.generic import TemplateView, ListView, DetailView


def placeholder_view(request):
    """一个占位视图，用于测试路由是否正常工作。"""
    return JsonResponse({'message': 'This is a placeholder view for GetUserInfo.'})


def view_name(request):
    pass


class MyTemplateView(TemplateView):
    template_name = "my_template.html"


class MyModel:
    pass


class MyModelListView(ListView):
    model = MyModel


class MyModelDetailView(DetailView):
    model = MyModel

