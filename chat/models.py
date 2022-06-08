from django.db import models
from accounts.models import User


class Channel(models.Model):
    # name = models.CharField(max_length=1000)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='farmer_channels')
    purchaser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchaser_channels')
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def display(self):
        seller = None
        if self.seller.farms.first():
            seller = self.seller.farms.first().name
        return {
            'seller': {'name': seller if seller else self.seller.surname},
            'last_message': self.message_set.latest('timestamp').text
        }

    def add_message(self, text, sender_id):
        sender = User.objects.get(id=int(sender_id))
        Message.objects.create(
            channel=self,
            text=text,
            sender=sender
        )


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)


class TempChatFile(models.Model):
    file = models.FileField(upload_to='')
    timestamp = models.DateTimeField(auto_now=True)
