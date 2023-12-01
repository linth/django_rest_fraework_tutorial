from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    # 任何使用者可讀取資料, 但必須owner才可以修改。
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


class IsOwnerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # 這個方法主要用於檢查對於整個資源（例如列表視圖）的權限
        return True
    
    def has_object_permission(self, request, view, obj):
        # 這個方法主要用於檢查對於單個資源對象的權限（例如詳細視圖）
        if request.user.is_superuser:
            # 當 admin 時, 可以操作。
            return True        
        
        return obj.owner == request.user