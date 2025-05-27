from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversation', ConversationViewSet)
router.register(r'message', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]