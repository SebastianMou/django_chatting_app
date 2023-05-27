from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(blank=True, default=':)', max_length=355)
    profile_image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self) -> str:
        return self.user.username
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    reciepient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, body, file=None):
        sender_message = Message(
            user=from_user,
            sender=from_user,
            reciepient=to_user,
            body=body,
            is_read=True,
        )

        if file:
            sender_message.file = file

        sender_message.save()

        recipient_message = Message(
            user=to_user,
            sender=from_user,
            reciepient=from_user,
            body=body,
            is_read=False,
        )

        if file:
            recipient_message.file = sender_message.file  # Use the file saved in the sender_message

        recipient_message.save()
        return sender_message
    
    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values('reciepient').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                    'user': User.objects.get(pk=message['reciepient']),
                    'last': message['last'],
                    'unread': Message.objects.filter(user=user, reciepient__pk=message['reciepient'], is_read=False).count()
                })
        return users