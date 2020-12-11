from django.urls import path, include
from rest_framework.routers import DefaultRouter

from direct import views


router = DefaultRouter()
router.register('my_messages', views.DirectMessageViewSet)

app_name = 'direct'

urlpatterns = [
    path('', include(router.urls)),
    path('my_chats/', views.ChatView.as_view(), name='chat'),
]