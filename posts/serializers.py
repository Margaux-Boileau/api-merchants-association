from rest_framework import serializers

from media.serializers import MediaSerializer
from .models import Post

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'creator', 'content', 'date']

class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'date', 'body', 'media', 'comments', 'id_creator']