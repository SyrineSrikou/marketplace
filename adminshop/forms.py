from django import forms
from django.contrib.auth.models import User
from store.models import Category
from blog.models import BlogPost

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_name"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the category title here..."
            }),

        }




class BlogPostForm(forms.ModelForm):
 
    class Meta:
        model = BlogPost
        fields = ["headline","sub_headline", "image", "body"]
        widgets = {
            "headline": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your post Title here..."
            }),
            "sub_headline": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your post subTitle here..."
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
          
            "body": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Add your blog post body here...",
                "rows": 5
            }),
           
        }
       
            
        