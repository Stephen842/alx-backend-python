from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        # Create notification for the reciever
        Notification.objects.create(
            user = instance.reciever,
            message = instance
        )