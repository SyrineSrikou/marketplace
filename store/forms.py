from django.forms import ModelForm, widgets
from django import forms
from .models import Store, Product, ReviewRating


class CreateStoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['name','logo','description','trader_license', 'phone_number', 'city', 'address']
        def __init__(self, *args, **kwargs):
            super(CreateStoreForm, self).__init__(*args, **kwargs)
            self.fields['trader_license'].required = False

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product name here..."
            }), 
            "logo": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
             "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
            "trader_license": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the store's phone number here..."
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the store's city location here..."
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the store address here..."
            }),

        }


class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True,
    }))

    class Meta:
        model = Product
        fields = ["name","category", "image", "price","description", 'stock', "return_policy",]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product name here..."
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Entre price of the product..."
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
			"stock": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter product stock ..."
            }),
            "return_policy": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product return policy here..."
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
