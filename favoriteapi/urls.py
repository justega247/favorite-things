from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterUsersView, LoginView, CategoryViewSet

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')

urlpatterns = [
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login")
]

urlpatterns += router.urls
