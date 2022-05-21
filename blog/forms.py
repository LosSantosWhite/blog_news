from django import forms
from blog.models import Post, Images


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["post_title", "post_barcode", "post_text"]


class CreateImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={
                    "multiple": True,
                    "enctype": "multipart/form-data",
                }
            )
        }


class UploadPostForm(forms.Form):
    file = forms.FileField()
