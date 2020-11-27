from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advertisement import views


router = DefaultRouter()
router.register('my_advertisements', views.AdvertisementViewSet, basename='myadvertisement')
router.register('advertisements', views.AdvertisementPublicViewSet)
router.register('tags', views.TagViewSet)

app_name = 'advertisement'

urlpatterns = [
    path('', include(router.urls))
]
