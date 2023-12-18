from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # TODO:AUTH ROUTES
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # TODO: POKEMON ROUTES
    # TODO: USERS
    # TODO: TEAMS ROUTES

]
