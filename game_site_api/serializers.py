from rest_framework import serializers

from game_site_api.models import User, ProfilePic, Post, PostPic, PostComent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePic
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPic
        fields = '__all__'

class PostComentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComent
        fields = '__all__'