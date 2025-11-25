from django.db.models.signals import post_save, pre_save, post_delete
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
        

@receiver(post_delete, sender=Message)
def delete_user_related_data(sender, instance, **kwargs):
    ''' Deletes all user-related messages, notifications and histories'''

    # Delete messages sent by user
    Message.objects.filter(sender=instance).delete()

    # Delete messages recieved by user
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications belonging to user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories created by user
    MessageHistory.objects.filter(edited_by=instance).delete()