from rest_framework import serializers
from .models import Forum

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id','title', 'date', 'read_members', 'read_write_members', 'posts']