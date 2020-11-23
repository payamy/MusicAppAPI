from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advertisement import views


router = DefaultRouter()
router.register('advertisements', views.AdvertisementViewSet)
router.register('tags', views.TagViewSet)

app_name = 'advertisement'

urlpatterns = [
    path('', include(router.urls))
]
