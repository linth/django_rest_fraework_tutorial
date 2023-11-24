from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.api_root),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),

    # function-based view
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),

    # class-based view
    path('snippets-class-based/', views.SnippetList.as_view(), name='snippet-list'),
    path('snippets-class-based/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),

    # class-based view with mixin
    path('snippets-mixin/', views.SnippetMixinList.as_view()),
    path('snippets-mixin/<int:pk>/', views.SnippetDatail.as_view()),

    # class-based view with generic
    path('snippet-generic/', views.SnippetGenericList.as_view()),
    path('snippet-generic/<int:pk>/', views.SnippetGenericDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
