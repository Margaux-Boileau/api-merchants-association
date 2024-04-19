from posts.models import Post
from media.models import Media
from .models import Forum
from .serializers import ForumSerializer
from posts.serializers import PostSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def forum_get_all_view(request):
    forums = Forum.objects.all()
    forums_names = [forum.title for forum in forums]
    return Response(forums_names, status=status.HTTP_200_OK)

@api_view(['GET'])
def forum_detail_view(request, pk):
    try:
        forum = Forum.objects.get(pk=pk)
    except Forum.DoesNotExist:
        return Response({"error": "Forum does not exist"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ForumSerializer(forum)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def forum_post_view(request):
    pass
