from django.db import models
from accounts.models import User
# Create your models here.


Open = 0
Open = 1 

TICKET_STATUS = (
    ("Open", "Open"),
    ("Closed", "Closed"), 
)


TICKET_TYPE = (
    ("Website problem", "Website problem"),
    ("Info inquiry", "Info inquiry"), 
    ("Complaint", "Complaint" )
)


TICKET_PRIORITY = (
    ("Urgent", "Urgent"),
    ("High", "High"), 
    ("Medium", "Medium"), 
    ("Low", "Low"), 

)

class Ticket(models.Model):
    subject = models.CharField(max_length=50)
    content = models.TextField()
    status  = models.CharField(max_length=50, default="Open", choices=TICKET_STATUS)
    ticket_type = models.CharField(max_length=50, default="Info inquiry", choices=TICKET_TYPE)
    priority = models.CharField(max_length=50, default="Low", choices=TICKET_PRIORITY)
    create_date    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    ticket_file = models.ImageField(blank=True, upload_to='images/tickets/files/%Y/%m/%d/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject




class ConversationMessage(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='conversationmessages', on_delete=models.CASCADE)
    content = models.TextField()

    created_by = models.ForeignKey(User, related_name='conversationmessages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']