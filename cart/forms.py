from django import forms


class CheckoutForm(forms.Form):
    order_note = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['order_note'].required = False
   