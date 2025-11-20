from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import MessageViewset, ConversationViewset

### DRF Base Router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewset, basename='conversations')

# DRF Nested Router for messages under conversation
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewset, basename='conversation-message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]