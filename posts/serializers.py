from rest_framework import serializers

from media.serializers import MediaSerializer
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'creator', 'content', 'date']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id','title', 'date', 'body', 'media', 'comments', 'id_creator']