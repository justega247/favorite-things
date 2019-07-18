from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterUsersView,
    LoginView,
    CategoryViewSet,
    FavoriteThingView,
    FavoriteThingDetailView,
    FavoriteThingsList,
    FavoriteThingAudit)

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')

urlpatterns = [
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('favorite/', FavoriteThingView.as_view(), name="create-favorite"),
    path('favorite/<int:id>', FavoriteThingDetailView.as_view(), name="detail-favorite"),
    path('favorite/category/<int:category_id>', FavoriteThingsList.as_view(), name="favorite-category-list"),
    path('favorite/history/<int:id>', FavoriteThingAudit.as_view(), name="favorite-history")
]

urlpatterns += router.urls
