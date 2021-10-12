from accounts.models import User
from django.db import models

class Notification(models.Model):
    STORE = 'store'
    ORDER = 'order'
    TICKET = 'ticket'

    CHOICES = (
        (STORE, 'store'),
        (ORDER, 'order'),
        (TICKET, 'ticket'),

    )

    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)
    extra_id = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creatednotifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']