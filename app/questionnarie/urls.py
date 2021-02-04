from django.urls import path, include
from rest_framework.routers import DefaultRouter

from questionnarie import views

router = DefaultRouter()
router.register('questions', views.QuestionViewSet, basename='questions')

app_name = 'question'

urlpatterns = [
    path('', include(router.urls))
]