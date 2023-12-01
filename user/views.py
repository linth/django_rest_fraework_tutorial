from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from snippets.permissions import IsOwnerOrReadOnly

from user.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



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


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = { 'status': 'request was permitted' }
        return Response(content)

