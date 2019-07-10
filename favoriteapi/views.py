from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserDataSerializer, CategorySerializer
from .permissions import AnonymousPermissionOnly
from .models import Category

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


# User Related Views
class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = UserDataSerializer


class LoginView(APIView):
    permission_classes = (AnonymousPermissionOnly,)

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        qs = User.objects.filter(username__exact=username)
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                payload = jwt_payload_handler(user_obj)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user=user_obj, request=request)
                return Response(response)
        return Response({
            "error": "Invalid Credentials"
        }, status=status.HTTP_400_BAD_REQUEST)


# Category Related Views
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
