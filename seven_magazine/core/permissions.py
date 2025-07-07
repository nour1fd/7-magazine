from rest_framework.permissions import BasePermission, SAFE_METHODS

# 1. Only the author (owner) can edit/delete, others can view
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


# 2. Only the author (owner) can do anything (including view)
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.author == request.user


# 3. Only authenticated users can write; everyone can read
class IsAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


# 4. Only admins can write; everyone can read
class IsAdminOrReadOnly(BasePermission):
  
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser


# 5. Only the user can access their own profile
class IsProfileOwner(BasePermission):

    def has_object_permission(self, request,  obj):
        return request.user.is_superuser or obj == request.user


# 6. Only the user can manage their own read-later list or purchases
class IsSelf(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user == request.user


# 7. Supervisor-only permission
class IsSupervisor(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type == "SUPERVISOR" or request.user.is_superuser
        )


# 8. Only authors can create or edit articles
class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == "AUTHOR"