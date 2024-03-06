from django.core.cache import cache
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .permissions import UserRegisterPermission

from .serializers import UserSerializer, ProfilePicSerializer, PostSerializer, PostPicSerializer, PostComentSerializer
from .models import User, ProfilePic, Post, PostPic, PostComent

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action

class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserRegisterPermission, )

    def create(self, request, *args, **kwargs):
        user_data = request.data
        user_data['password'] = make_password(user_data['password'])
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'user_name': user.username,
            }

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePicViewSet(viewsets.ModelViewSet):
    queryset = ProfilePic.objects.all()
    serializer_class = ProfilePicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class PostViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        post_data = request.data
        user = post_data['user']
        cache.delete(user)

        serializer = PostSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'пост создан'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        post_data = request.data
        user = post_data['user']
        cache.delete(user)
        serializer = PostSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        post_data = request.data
        user = post_data['user']
        cache.delete(user)
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def filter(self, request, pk=None):
        cached_data = cache.get(pk)
        if cached_data:
            posts = cached_data
        else:
            posts = Post.objects.filter(user=pk)
            cache.set(pk, posts, timeout=3600)

        return Response(PostSerializer(posts, many=True).data)

class PostPicViewSet(viewsets.ModelViewSet):
    queryset = PostPic.objects.all()
    serializer_class = PostPicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class PostComentViewSet(viewsets.ModelViewSet):
    queryset = PostComent.objects.all()
    serializer_class = PostComentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(methods=['get'], detail=True)
    def filter(self, request, pk=None):
        posts = PostComent.objects.filter(post=pk)
        return Response(PostComentSerializer(posts, many=True).data)

