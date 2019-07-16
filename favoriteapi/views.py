from django.contrib.auth import get_user_model
from django.db.models import F, Max
from rest_framework import status, generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserDataSerializer, CategorySerializer, FavoriteThingSerializer
from .permissions import AnonymousPermissionOnly, IsOwnerOrReadOnly
from .models import Category, Favorite
from .utils.error_message_handler import raise_error

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
    """
    POST auth/login/
    """
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
    """
    POST category/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(
            favorite__user_id=self.request.user
        ).distinct()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


# Favorite things Related Views
class FavoriteThingView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Favorite.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoriteThingSerializer

    def post(self, request, *args, **kwargs):
        """
        POST favorite/
        """
        data = request.data
        ranking = data.get('ranking')
        category_id = data.get('category')

        if ranking and ranking <= 0:
            raise_error(
                message='Sorry your ranking has to be a positive integer'
            )

        existing_favorites = Favorite.objects.filter(
            user=self.request.user,
            category__id=category_id
        )
        if ranking != 1 and not existing_favorites:
            raise_error(
                message=f'The first valid ranking for a favorite in this category is 1'
            )
        if not existing_favorites:
            return self.create(request, *args, **kwargs)

        current_max = Favorite.objects.filter(
            user=self.request.user,
            category__id=category_id
        ).aggregate(Max('ranking'))

        current_max_ranking = current_max['ranking__max']

        if ranking <= current_max_ranking:
            Favorite.objects.filter(
                ranking__gte=ranking,
                user=self.request.user,
                category__id=category_id
            ).update(ranking=F('ranking') + 1)
            return self.create(request, *args, **kwargs)
        elif ranking - current_max_ranking == 1:
            return self.create(request, *args, **kwargs)
        else:
            raise_error(
                message=f'The next valid ranking for a favorite in this category is {current_max_ranking + 1}'
            )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteThingDetailView(mixins.DestroyModelMixin, generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = FavoriteThingSerializer
    queryset = Favorite.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        favorite_thing_id = kwargs['id']
        new_ranking = request.data.get('ranking')
        favorite_to_update = Favorite.objects.get(id=favorite_thing_id)
        previous_ranking = favorite_to_update.ranking

        if new_ranking and new_ranking <= 0:
            raise_error(
                message='Sorry your ranking has to be a positive integer'
            )

        if not new_ranking or new_ranking == previous_ranking:
            return self.partial_update(request, *args, **kwargs)

        current_max = Favorite.objects.filter(
            user=self.request.user,
            category__id=favorite_to_update.category_id
        ).aggregate(Max('ranking'))

        current_max_ranking = current_max['ranking__max']
        if not current_max_ranking:
            raise_error(
                message='You do not have a favorite thing to update in this category'
            )

        if previous_ranking > new_ranking:
            Favorite.objects.filter(
                category__id=favorite_to_update.category_id,
                ranking__lt=previous_ranking,
                ranking__gte=new_ranking
            ).update(ranking=F('ranking') + 1)
            return self.partial_update(request, *args, **kwargs)
        elif previous_ranking < new_ranking <= current_max_ranking:
            Favorite.objects.filter(
                category__id=favorite_to_update.category_id,
                ranking__gt=previous_ranking,
                ranking__lte=new_ranking
            ).update(ranking=F('ranking') - 1)
            return self.partial_update(request, *args, **kwargs)
        else:
            raise_error(
                message=f'The highest ranking you can update to at the moment is {current_max_ranking}'
            )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        Favorite.objects.filter(
            ranking__gt=instance.ranking,
            category__id=instance.category_id
        ).update(ranking=F('ranking') - 1)
        return instance.delete()


class FavoriteThingsList(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = FavoriteThingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = Favorite.objects.filter(
            category_id=category_id,
            user_id=self.request.user
        )
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
