from rest_framework import pagination


class FavoriteThingPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
