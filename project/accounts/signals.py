from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

from .models import User, Notification as NotificationModel

@receiver(post_save, sender=NotificationModel)
def post_save_notification(instance: NotificationModel, created, *args, **kwargs):
    if created:
        if instance.for_all:
            devices = FCMDevice.objects.all()
        else:    
            devices = FCMDevice.objects.filter(user=instance.user)  
        
        for device in devices:
            message = Message(notification=Notification(
                title=instance.name,
                body=instance.content,
                image=instance.image.url if instance.image else None
            ))
            device.send_message(message)
