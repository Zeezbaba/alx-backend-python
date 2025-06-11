from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageNotificationTestcase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='zeezbaba', password='pwd123')
        self.user2 = User.objects.create_user(username='darasimi', password='pwd123')

    def test_notification_created_on_new_message(self):
        # send message from zeezbaba to darasimi
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello daughter'
        )

        # Check if notification was created for darasimi
        notification = Notification.objects.filter(user=self.user2, message=message)
        self.assertTrue(notification.exists())
