from django.urls import path, include
from rest_framework.routers import DefaultRouter

from classroom import views


router = DefaultRouter()
router.register('my_classrooms', views.ClassroomViewSet)
router.register('classrooms', views.ClassroomPublicViewSet)
router.register('tutorials', views.TutorialViewSet)
router.register('comments', views.CommentViewSet)

app_name = 'classroom'

urlpatterns = [
    path('', include(router.urls))
]
