import base64
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
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
    


        if len(media_names)!=len(media_contents): 
            return Response({"error": "Number of image names and content do not match"}, status=status.HTTP_400_BAD_REQUEST)

    
    def post(self, request, forum_pk):
        try:
            forum = Forum.objects.get(pk=forum_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Forum does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if not forum.read_write_members.filter(id=user.shop_working_at.id).exists():
            return Response({"error": "You do not have permission to post in this forum."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        media_names = data.get('media_names', [])
        media_contents = data.get('media_contents', [])

        if len(media_names) != len(media_contents):
            return Response({"error": "Mismatch between media names and contents."}, status=status.HTTP_400_BAD_REQUEST)

        media_objects = []
        for name, content in zip(media_names, media_contents):
            if Media.objects.filter(Q(id=name)).exists():
                return Response({"error": f"Media with name '{name}' already exists."}, status=status.HTTP_400_BAD_REQUEST)

            image_data = base64.b64decode(content)
            with open(f'uploads/{name}', 'wb') as f:
                f.write(image_data)
            media = Media(id=name)
            media_objects.append(media)

        # Usamos bulk_create para crear los medios
        Media.objects.bulk_create(media_objects)

        post = Post.objects.create(
            title=data.get('title'),
            body=data.get('body'),
            id_creator=user.shop_working_at,
        )
        post.media.add(*media_objects)
        
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