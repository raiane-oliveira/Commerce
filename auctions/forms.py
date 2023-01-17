from django import forms

class FormNewListing(forms.Form):

    # Required Fields
    title = forms.CharField(label="Title of Listing:", widget=forms.TextInput(attrs={
        "class": "form-control",
    }))

    description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={
        "class": "form-control",
    }))
    
    bid = forms.DecimalField(label="Start Bid:", widget=forms.TextInput(attrs={
        "placeholder": "$",
        "class": "form-control"
    }))

    # Optional Fields
    imageURL = forms.URLField(label="Image URL:", required=False, widget=forms.URLInput(attrs={
        "class": "form-control"
    }))
    category = forms.CharField(label="Category:", required=False, widget=forms.TextInput(attrs={
        "class": "form-control"
    }))


class FormComments(forms.Form):

    # Remove label
    def __init__(self, *args, **kwargs):
        super(FormComments, self).__init__(*args, **kwargs)
        self.fields['comment'].label = ""

    comment = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Write something...",
        "rows": "5"
    }))