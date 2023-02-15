from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tasks
from .serializers import TasksSerializer


class TasksList(APIView):
    serializer_class = TasksSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        tasks = Tasks.objects.all()
        serializer = TasksSerializer(
            tasks, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )