from django.urls import path, include
from rest_framework.routers import DefaultRouter

from classroom import views


router = DefaultRouter()
router.register('my_classrooms', views.ClassroomViewSet, basename='myclassroom')
router.register('classrooms', views.ClassroomPublicViewSet)
router.register('tutorials', views.TutorialViewSet)
router.register('comments', views.CommentViewSet)
#router.register('teachers', views.TeacherViewSet)

app_name = 'classroom'

urlpatterns = [
    path('', include(router.urls)),
    path('teachers/', views.TeachersListViewSet.as_view(), name='teachers'),
    path('teachers/<int:pk>/', views.TeachersItemViewSet.as_view(), name='teachers'),
]
