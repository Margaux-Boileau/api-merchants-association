import base64
import uuid
from rest_framework.pagination import PageNumberPagination
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
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

# URL: /forums/<forum_pk>/posts/
class PostListView(APIView):    
    permission_classes = [IsAuthenticated]

    # PERMISSIONS: read members of forum
    def get(self, request, forum_pk):
        itemsPerPage = self.request.query_params.get('itemsPerPage')
        page = self.request.query_params.get('page')
        print(page)

        try:
            forum = Forum.objects.get(pk=forum_pk)
        except Forum.DoesNotExist:
            return Response({"error": "Forum does not exist"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if not user.shop_working_at:
            return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)
        elif not forum.read_members.filter(id=user.shop_working_at.id).exists():
            return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)

        posts = Post.objects.filter(forum=forum).order_by('-id')
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(posts, request)
        serializer = PostSerializer(page, many=True)
        return pagination.get_paginated_response(serializer.data)
    
    # PERMISIIONS: write members of forum
    def post(self, request, forum_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Forum does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if not user.shop_working_at:
            return Response({"error": "You do not have permission to post in this forum."}, status=status.HTTP_403_FORBIDDEN)
        elif not forum.read_write_members.filter(id=user.shop_working_at.id).exists():
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

            media_name = f'{uuid.uuid4()}.jpg'

            with open(f'uploads/{media_name}', 'wb') as f:
                f.write(decoded)
            
            media_obj = Media.objects.create(id=media_name)
            media_objects.append(media_obj)
        
        post.media.add(*media_objects)        
        forum.posts.add(post)

        for shop in forum.read_members.all():
            for worker in shop.workers.all():
                device = FCMDevice.objects.filter(user=worker)
                message = Message(
                notification=Notification(title="Nuevo post", body=f"Se ha publicado un nuevo post en el foro {forum.title}", image="http://172.23.6.211:8000/media/logo/")
                )
                try:
                    device.send_message(message)
                except Exception as e:
                    # Manejo de la excepción
                    print(f"Error al enviar el mensaje a {worker.username}: {e}")

        return Response({"message": "Post created successfully."}, status=status.HTTP_201_CREATED)

# URL: /forums/<forum_pk>/posts/<post_pk>/
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # PERMISSIONS: read members of forum
    def get(self, request, forum_pk, post_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Forum does not exist."}, status=status.HTTP_404_NOT_FOUND)
                  
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        if not user.shop_working_at:
            return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)
        elif not forum.read_members.filter(id=user.shop_working_at.id).exists():
            return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post)        
        return Response(serializer.data)
    
    # PERMISSIONS: creator of post
    def delete(self, request, forum_pk, post_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Forum does not exist."}, status=status.HTTP_404_NOT_FOUND)
                  
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        if not user.shop_working_at:
            return Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        elif not user.shop_working_at==post.id_creator:
            return Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        
        post.delete()
        return Response({"message": "Post deleted successfully from the forum."}, status=status.HTTP_200_OK)

# URL: /forums/<forum_pk>/posts/<post_pk>/comments/
class CommentsListView(APIView):
    permission_classes = [IsAuthenticated]

    # PERMISSIONS: read members of forum
    def get(self, request, forum_pk, post_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Forum does not exist."}, status=status.HTTP_404_NOT_FOUND)
                  
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if post not in forum.posts.all():
            return Response({"error": "Post does not belong to this forum."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if not user.shop_working_at:
            return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)
        elif not forum.read_members.filter(id=user.shop_working_at.id).exists():
            return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)

        comments = post.comments.all().order_by('-id')
        pagination = PageNumberPagination()
        page = pagination.paginate_queryset(comments, request)
        serializer = CommentSerializer(page, many=True)
        return pagination.get_paginated_response(serializer.data)
    
    # PERMISSIONS: read members of forum
    def post(self, request, forum_pk, post_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Forum does not exist."}, status=status.HTTP_404_NOT_FOUND)
                  
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if post not in forum.posts.all():
            return Response({"error": "Post does not belong to this forum."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if not user.shop_working_at:
            return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)
        elif not forum.read_members.filter(id=user.shop_working_at.id).exists():
            return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            comment = Comment.objects.create(
                creator=user.shop_working_at,
                content=request.data.get('content'))
            post.comments.add(comment)
            return Response({"message": "Comment created sucessfully"} ,status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)    

# URL: /comments/<pk_comment>/
# PERMISSIONS: owner of comment
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ])
def delete_comment(request, comment_pk): 
    try:
        comment = Comment.objects.get(pk=comment_pk)
    except ObjectDoesNotExist:
        return Response({"error": "Comment does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if not user.shop_working_at:
        return Response({"error": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
    elif user.shop_working_at != comment.creator:
        return Response({"error": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
    
    comment.delete()
    return Response({"message": "Comment deleted successfully."}, status=status.HTTP_200_OK)

# URL: /forums/<forum_pk>/posts/<post_pk>/media/<media_pk/
# PERMISSIONS: read members of forum
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_post_media(request, forum_pk, post_pk, media_pk):
    try:
        forum = Forum.objects.get(pk=forum_pk)
    except ObjectDoesNotExist:
        return Response({"error": "Forum does not exist."}, status=status.HTTP_404_NOT_FOUND)
              
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        media = Media.objects.get(pk=media_pk)
    except Media.DoesNotExist:
        return Response({"error": "Media does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if post not in forum.posts.all():
        return Response({"error": "Post does not belong to this forum."}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if not user.shop_working_at:
        return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)
    elif not forum.read_members.filter(id=user.shop_working_at.id).exists():
        return Response({"error": "You do not have access to this forum."}, status=status.HTTP_403_FORBIDDEN)

    if media not in post.media.all():
        return Response({"error": "Media does not belong to this post."}, status=status.HTTP_404_NOT_FOUND)
    
    media_name = media.id
    with open('uploads/'+media_name, 'rb') as img_file:
        img_data = img_file.read()
        img_base64 = base64.b64encode(img_data).decode('utf-8')

    return Response({"image" :img_base64},  status=status.HTTP_200_OK)
    #img = open('uploads/'+media_name, 'rb')
    #response = FileResponse(img)
    #return response 