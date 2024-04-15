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
def forum_post_view(request, pk):
    pass

@api_view(['GET'])
def forum_posts_view(request, pk):
    try:
        forum = Forum.objects.get(pk=pk)
    except Forum.DoesNotExist:
        return Response({"error": "Forum does not exist"}, status=status.HTTP_404_NOT_FOUND)

    posts = Post.objects.filter(forum=forum)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def forum_post_post_view(request, pk):
    data = request.data
    media_files = data.get('media', []) 
    # Crear instancias de Media para cada archivo proporcionado en la lista media
    media_instances = []
    for media_file in media_files:
        media_instance = Media.objects.create(id=media_file)
        media_instances.append(media_instance.id)   
    # Eliminar la lista de media del diccionario de datos para que no se incluya al crear el objeto Post
    data.pop('media', None) 
    # Añadir la instancia de Media al objeto Post si se crearon
    if media_instances:
        data['media'] = media_instances 
    # Añadir el id_creator desde la URL (pk) o desde el JSON (si se proporciona)
    data['id_creator'] = data.get('id_creator', pk) 
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        post = serializer.save()    
        # Añadir el ID del nuevo Post al campo posts del Forum correspondiente
        forum = Forum.objects.get(pk=pk)
        forum.posts.add(post.id)    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  