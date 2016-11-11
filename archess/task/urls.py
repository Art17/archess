from django.conf.urls import url
from . import views
from . import rest_views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^create-task/$', views.CreateTaskView.as_view()),
    url(r'^task/(\d+)', views.get_task),

    url(r'^api/tasks/$', rest_views.TasksAPI.as_view()),
    url(r'^api/tasks/(\d+)$', rest_views.TaskAPI.as_view())
]