from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class NotificationSignalTest(TestCase):

    def test_notification_created_on_message(self):
        user1 = User.objects.create_user(username='sender', password='pass123')
        user2 = User.objects.create_user(username='reciever', password='pass123')

        msg = Message.objects.create(
            sender = user1,
            reciever = user2,
            content = 'Hello Stephen'
        )

        notification = Notification.objects.filter(message=msg).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, user2)