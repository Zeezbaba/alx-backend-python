from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet, delete_user

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

convo_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'message', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_router.urls)),
    path('delete-account/', delete_user, name='delete_account')
]