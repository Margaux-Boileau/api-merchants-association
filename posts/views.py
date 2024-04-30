import base64
import os
import uuid
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from .models import Post, Comment
from media.models import Media
from forums.models import Forum
from forums.serializers import ForumSerializer
from rest_framework.views import APIView
from .serializers import CommentSerializer, PostSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# /forums/<forum_pk>/posts/
class PostListView(APIView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []

        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, forum_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
        except Forum.DoesNotExist:
            return Response({"error": "Forum does not exist"}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(forum=forum)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, forum_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Forum does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if not forum.read_write_members.filter(id=user.shop_working_at.id).exists():
            return Response({"error": "You do not have permission to post in this forum."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        medias = data.get('medias', [])

        post = Post.objects.create(
            title=data.get('title'),
            body=data.get('body'),
            id_creator=user.shop_working_at,
        )        
        
        media_objects = []
        for media in medias:
            decoded = base64.b64decode(media)

            media_name = f'uploads/{uuid.uuid4()}.jpg'

            with open(media_name, 'wb') as f:
                f.write(decoded)
            
            media_obj = Media.objects.create(id=media_name)
            media_objects.append(media_obj)
        
        post.media.add(*media_objects)        
        forum.posts.add(post)

        return Response(status=status.HTTP_201_CREATED)

# /forums/<forum_pk>/posts/<post_pk>
class PostDetailView(APIView):
    def get(self, request, forum_pk, post_pk):
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        
        return Response(serializer.data)

# /forums/<forum_pk>/posts/<post_pk>/comments/
class CommentsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, forum_pk, post_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
            post = Post.objects.get(pk=post_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Object does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if post not in forum.posts.all():
            return Response({"error": "Post does not belong to this forum."}, status=status.HTTP_404_NOT_FOUND)
        
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, forum_pk, post_pk):
        user = request.user
        data = request.data

        try:
            forum = Forum.objects.get(pk=forum_pk)
            post = Post.objects.get(pk=post_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Object does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if user.shop_working_at not in forum.read_members.all():
            return Response({"error": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)

        if post not in forum.posts.all():
            return Response({"error": "Post does not belong to this forum."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            comment = Comment.objects.create(
                creator=user.shop_working_at,
                content=data.get('content'))
            post.comments.add(comment)
            return Response({"message": "Comment created sucessfully"} ,status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# /comments/<pk_comment/
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ])
def delete_comment(request, comment_pk):
    user = request.user
    
    try:
        comment = Comment.objects.get(pk=comment_pk)
    except ObjectDoesNotExist:
        return Response({"error": "Comment does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    if user.shop_working_at != comment.creator:
        return Response({"error": "You do not have permission."}, status=status.HTTP_403_FORBIDDEN)
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# /forums/<forum_pk>/posts/<post_pk>/media/<media_pk/
@api_view(['GET'])
def get_post_media(request, forum_pk, post_pk, media_pk):
    try:
        forum = Forum.objects.get(pk=forum_pk)
        post = Post.objects.get(pk=post_pk)
        media = Media.objects.get(pk=media_pk)
    except ObjectDoesNotExist:
        return Response({"error": "Object does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    if post not in forum.posts.all():
        return Response({"error": "Post does not belong to this forum."}, status=status.HTTP_404_NOT_FOUND)
    
    if media not in post.media.all():
        return Response({"error": "Media does not belong to this post."}, status=status.HTTP_404_NOT_FOUND)
    
    media_name = media.id
    print(media_name)
    img = open('uploads/'+media_name, 'rb')

    response = FileResponse(img)

    return response    