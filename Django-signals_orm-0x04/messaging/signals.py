from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        # Create notification for the reciever
        Notification.objects.create(
            user = instance.reciever,
            message = instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)

            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message = instance,
                    old_content = old_message.content,
                    edited_by = instance.edited_by
                )

                instance.edited = True

        except Message.DoesNotExist:
            pass