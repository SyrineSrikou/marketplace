from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)