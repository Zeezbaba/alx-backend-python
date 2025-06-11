from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user = instance.receiver,
            message = instance
        )

@receiver(pre_save, sender=Message)
def log_edit_message(sender, instance, **kwargs):
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content
        )
        instance.edited = True