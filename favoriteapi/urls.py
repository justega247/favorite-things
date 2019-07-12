from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterUsersView,
    LoginView,
    CategoryViewSet,
    FavoriteThingView,
    FavoriteThingDetailView)

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')

urlpatterns = [
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('favorite/', FavoriteThingView.as_view(), name="create-favorite"),
    path('favorite/<int:id>', FavoriteThingDetailView.as_view(), name="detail-favorite")
]

urlpatterns += router.urls
