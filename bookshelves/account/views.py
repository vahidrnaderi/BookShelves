"""Auth views."""
from base.permissions import AAPDjangoModelPermissions
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    ContentTypeSerializer,
    GroupSerializer,
    LoginSerializer,
    PermissionSerializer,
    RegisterSerializer,
    UserSerializer,
)


class ContentTypeFilter(filters.FilterSet):
    """Content type filter."""

    name = filters.CharFilter(field_name="model")

    class Meta:
        model = ContentType
        fields = ("name", "app_label")


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Content type view set."""

    permission_classes = [permissions.IsAuthenticated, AAPDjangoModelPermissions]
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    filterset_class = ContentTypeFilter


class UserViewSet(viewsets.ModelViewSet):
    """User view set."""

    permission_classes = [permissions.IsAuthenticated, AAPDjangoModelPermissions]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = (
        "username",
        "mobile",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )


class GroupViewSet(viewsets.ModelViewSet):
    """Group view set."""

    permission_classes = [permissions.IsAuthenticated, AAPDjangoModelPermissions]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_fields = ("name",)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """Permission view set."""

    permission_classes = [permissions.IsAuthenticated, AAPDjangoModelPermissions]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filterset_fields = ("name", "codename")


class LoginView(views.APIView):
    """Login view."""

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        """Handle POST method to authenticate a user."""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=serializer.data["username"],
            password=serializer.data["password"],
        )
        if not user:
            return Response(
                data={"message": "invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = Token.objects.get_or_create(user=user)
        return Response(data={"token": token[0].key})


class LogoutView(views.APIView):
    """Logout view."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET request to logout a user."""
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(views.APIView):
    """Change a user's password view."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def patch(self, request):
        """Handle PATCH request to update a user's password."""
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if (
            serializer.data.get("username")
            and request.user.username != serializer.data["username"]
            and not request.user.has_perm("auth.change_user")
        ):
            return Response(
                {"message": "permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        if not request.user.has_perm("auth.change_user"):
            user = authenticate(
                username=serializer.data.get("username") or request.user,
                password=serializer.data["old_password"],
            )
            if not user:
                return Response(
                    data={"message": "invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            if serializer.data.get("username"):
                user = User.objects.get(username=serializer.data["username"])
            else:
                user = request.user
        user.set_password(serializer.data["new_password"])
        user.save()
        return Response({"message": "password has been updated"})


class MyProfileView(generics.RetrieveAPIView, generics.UpdateAPIView):
    """User profile view."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """DRF built-in method.

        Only return the current logged-in user object.
        """
        return self.request.user


class RegisterView(generics.CreateAPIView):
    """Register user view."""

    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
