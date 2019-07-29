from django.db.models import F, Max
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import CategorySerializer, FavoriteThingSerializer
from .models import Category, Favorite
from .utils.error_message_handler import raise_error


# Category Related Views
class CategoryViewSet(viewsets.ModelViewSet):
    """
    POST category/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    pagination_class = None


# Favorite things Related Views
class FavoriteThingView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Favorite.objects.all()
    permission_classes = (AllowAny,)
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
            category__id=category_id
        )
        if ranking != 1 and not existing_favorites:
            raise_error(
                message=f'The first valid ranking for a favorite is 1'
            )
        if not existing_favorites:
            return self.create(request, *args, **kwargs)

        current_max = Favorite.objects.filter(
            category__id=category_id
        ).aggregate(Max('ranking'))

        current_max_ranking = current_max['ranking__max']

        if ranking <= current_max_ranking:
            created = self.create(request, *args, **kwargs)
            if created:
                Favorite.objects.filter(
                    ~Q(id=created.data['id']),
                    ranking__gte=ranking,
                    category__id=category_id
                ).update(ranking=F('ranking') + 1)
            return created

        elif ranking - current_max_ranking == 1:
            return self.create(request, *args, **kwargs)
        else:
            raise_error(
                message=f'The next valid ranking for a favorite in this category is {current_max_ranking + 1}'
            )


class FavoriteThingDetailView(mixins.DestroyModelMixin, generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FavoriteThingSerializer
    queryset = Favorite.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        favorite_thing_id = kwargs['id']
        print(favorite_thing_id)
        new_ranking = request.data.get('ranking')
        print(request.data)
        favorite_to_update = get_object_or_404(Favorite, id=favorite_thing_id)
        previous_ranking = favorite_to_update.ranking

        if not new_ranking:
            raise_error(
                message='Please provide a value for the ranking'
            )

        if new_ranking <= 0:
            raise_error(
                message='Sorry your ranking has to be a positive integer'
            )

        if new_ranking == previous_ranking:
            return self.update(request, *args, **kwargs)

        current_max = Favorite.objects.filter(
            category__id=favorite_to_update.category_id
        ).aggregate(Max('ranking'))

        current_max_ranking = current_max['ranking__max']

        if previous_ranking > new_ranking:
            updated = self.update(request, *args, **kwargs)
            if updated:
                Favorite.objects.filter(
                    ~Q(id=updated.data['id']),
                    category__id=favorite_to_update.category_id,
                    ranking__lt=previous_ranking,
                    ranking__gte=new_ranking
                ).update(ranking=F('ranking') + 1)
            return updated
        elif previous_ranking < new_ranking <= current_max_ranking:
            updated = self.update(request, *args, **kwargs)
            if updated:
                Favorite.objects.filter(
                    ~Q(id=updated.data['id']),
                    category__id=favorite_to_update.category_id,
                    ranking__gt=previous_ranking,
                    ranking__lte=new_ranking
                ).update(ranking=F('ranking') - 1)
            return updated
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
    permission_classes = (AllowAny,)

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        queryset = Favorite.objects.filter(
            category_id=category_id,
        )
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FavoriteThingAudit(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        favorite_id = kwargs['id']
        favorite = get_object_or_404(Favorite, pk=favorite_id)
        response = []
        all_history = favorite.history.all()
        changes = []
        for i in range(0, len(all_history) - 1):
            new_history, old_history = all_history[i], all_history[i + 1]
            delta = new_history.diff_against(old_history)
            changes = changes + delta.changes
        for change in changes:
            response.append(f'{change.field.capitalize()} changed from {change.old} to {change.new}')
        return Response({
            "audit": response
        })
