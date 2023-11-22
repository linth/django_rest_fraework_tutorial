from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions

from user.serializers import UserSerializer
from user.permissions import IsOwnerOrReadOnly


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

