from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from snippets.permissions import IsOwnerOrReadOnly

from user.serializers import UserSerializer



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

