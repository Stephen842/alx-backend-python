from django.urls import path, include
from rest_framework.router import DefaultRouter
from .views import MessageViewset, ConversationViewset

### DRF Router
router = DefaultRouter()
router.register(r'messages', MessageViewset, basename='messages')
router.register(r'conversations', ConversationViewset, basename='conversations')

urlpatterns = [
    path('', include(router.urls)),
]