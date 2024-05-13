from django.http import FileResponse
from posts.models import Post
from forums.models import Forum
from accounts.models import Account
from .models import Media
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def get_logo(request):
    img = open('uploads/logo.jpg', 'rb')

    response = FileResponse(img)
    
    return response

# forums/<int:forum_pk>/posts/<int:post_pk>/media/<str:media_pk>/
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_post_media_view(request, forum_pk, post_pk, media_pk):

    try:
        forum = Forum.objects.get(pk=forum_pk)
        post = Post.objects.get(pk=post_pk)
    except Exception as error:
        return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if user not in forum.read_members:
        return Response({"error": "You do not have permission to see this content."}, status=status.HTTP_403_FORBIDDEN)

    if post not in forum.posts:
        return Response({"error": "Post not found in specified forum"}, status=status.HTTP_404_NOT_FOUND)
    
    if media_pk not in post.media:
        return Response({"error": "Media not found in specified forum"}, status=status.HTTP_404_NOT_FOUND)
    
    img = open(f'media/{media_pk}', 'rb')

    response = FileResponse(img)
    
    return response
