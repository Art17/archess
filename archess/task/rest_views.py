from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from rest_framework import views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


from task.models import Task
from task.serializers import TaskPutSerializer, TaskGetSerializer


class TasksAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        name = request.GET.get('name')
        if name != '':
            tasks = Task.objects.filter(author__username__startswith=name)
        else:
            tasks = Task.objects.all()
        task_serializer = TaskGetSerializer(tasks, many=True)
        return Response(task_serializer.data)

    def post(self, request):
        serializer = TaskPutSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return_serializer = TaskGetSerializer(task)
            return Response(return_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(api_view(['GET', 'PUT', 'DELETE']), name='dispatch')
class TaskAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskGetSerializer(task)
        return Response(serializer.data)


    def put(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not request.user.is_superuser and request.user.id != id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TaskPutSerializer(task, data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return_serializer = TaskGetSerializer(task)
            return Response(return_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (request.user.id == task.author.id):
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
