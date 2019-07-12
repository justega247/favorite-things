from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import status, generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserDataSerializer, CategorySerializer, FavoriteThingSerializer
from .permissions import AnonymousPermissionOnly, IsOwnerOrReadOnly
from .models import Category, Favorite

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


# Favorite things Related Views
class FavoriteThingView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Favorite.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoriteThingSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        ranking = data.get('ranking')
        category_id = data.get('category')
        existing_favorites = Favorite.objects.filter(
            ranking__gte=ranking,
            user=self.request.user
        ).filter(
            category__id=category_id
        )
        if existing_favorites:
            existing_favorites.update(ranking=F('ranking') + 1)

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteThingDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = FavoriteThingSerializer
    queryset = Favorite.objects.all()
    lookup_field = 'id'
