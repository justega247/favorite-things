from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from .serializers import UserDataSerializer


User = get_user_model()


class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserDataSerializer
