from django.forms import ModelForm, widgets
from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["subject","content", "ticket_type", "priority","ticket_file",]
        widgets = {
            "subject": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product name here..."
            }),
            "ticket_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "priority": forms.Select(attrs={
                "class": "form-control"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
			 "ticket_file": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
           
        }
        
        def __init__(self, *args, **kwargs):
            super(TicketForm, self).__init__(*args, **kwargs)
            self.fields['ticket_file'].required = False