import base64

from shops.models import Shop
from .models import Post
from media.models import Media
from forums.models import Forum
from forums.serializers import ForumSerializer
from rest_framework.views import APIView
from .serializers import PostSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# /forums/<pk_forum>/posts/
class PostListView(APIView):
    def get(self, request, forum_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
        except Forum.DoesNotExist:
            return Response({"error": "Forum does not exist"}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(forum=forum)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, forum_pk):
        data = request.data
        media_names = data.get('media', [])
        media_contents = data.get('media_contents', [])

        media_objects = []
        for name, content in zip(media_names, media_contents):
            image_data = base64.b64decode(content)
            with open(f'uploads/{name}', 'wb') as f:
                f.write(image_data)
            media = Media.objects.create(id_name=name)
            media_objects.append(media)

        data.pop('media_names', [])
        data.pop('media_contents', [])

        post = Post.objects.create(
            title = data.get('title'),
            date = data.get('date'),
            body = data.get('body'),
            id_creator = Shop.objects.get(pk=data.get('id_creator')) ,
        )
        post.media.add(*media_objects)
        
        forum = Forum.objects.get(pk=forum_pk)
        forum.posts.add(post)

        return Response(status=status.HTTP_201_CREATED)


# /forums/<pk_forum>/posts/<pk_post>
class PostDetailView(APIView):
    def get(self, request):
        pass

# /forums/<pk_forum>/posts/<pk_post>/comments/
class CommentsListView(APIView):
    def get(self, request):
        pass