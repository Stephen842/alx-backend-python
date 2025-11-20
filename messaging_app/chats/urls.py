from django.urls import path, include
from rest_framework import routers
from .views import MessageViewset, ConversationViewset

### DRF Router
router = routers.DefaultRouter()
router.register(r'messages', MessageViewset, basename='messages')
router.register(r'conversations', ConversationViewset, basename='conversations')

urlpatterns = [
    path('', include(router.urls)),
]