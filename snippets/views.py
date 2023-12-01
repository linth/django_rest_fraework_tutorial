from rest_framework import status
from snippets.models import Snippet
from snippets.permissions import IsOwnerOnly, IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import permissions, mixins, generics
from rest_framework import reverse, renderers



'''
tutorial 2: function-based and requests and responses.

tutorial 5: relationships & hyperlinked apis.

Reference:
    - https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
'''

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # 'user': reverse('user-list', request=request, format=format),
        # 'snippets': reverse('snippet-list', request=request, format=format)
    })


# @csrf_exempt
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *arg, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


'''
tutorial 3: class-based views.

Reference:
    - https://www.django-rest-framework.org/tutorial/3-class-based-views/
'''
class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = [
        # permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAuthenticated
    ]

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = [
        # permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAuthenticated,
        # IsOwnerOrReadOnly,
        IsOwnerOnly,
    ]

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

'''
using mixins class to implement the class-based views.
'''
class SnippetMixinList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *arg, **kwargs):
        return self.list(request=request, *arg, **kwargs)
    
    def post(self, request, *arg, **kwargs):
        return self.create(request=request, *arg, **kwargs)
    

class SnippetDatail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *arg, **kwargs):
        return self.retrieve(request, *arg, **kwargs)
    
    def put(self, request, *arg, **kwargs):
        return self.update(request, *arg, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


'''
using generic class-based views.
'''
class SnippetGenericList(generics.ListAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    