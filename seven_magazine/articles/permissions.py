# from rest_framework import permissions
# from rest_framework.permissions import SAFE_METHODS

# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         return request.method in SAFE_METHODS or obj == request.user
    
# class IsArticleOwnerOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated
    
#     def has_object_permission(self, request, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         return obj.author == request.user
    
# class IsAuthor(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated and request.user.role == 'author'

# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated and request.user.role == 'admin'

# class IsOwnerOrAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.author == request.user or request.user.role == 'admin'