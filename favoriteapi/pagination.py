from rest_framework import pagination


class FavoriteThingPagination(pagination.PageNumberPagination):
    page_size = 10
