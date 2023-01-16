from django import forms

class FormNewListing(forms.Form):

    # Required Fields
    title = forms.CharField(label="Title of Listing:", widget=forms.TextInput(attrs={
        "class": "form-control",
    }))

    description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 5,
        "cols": 30
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


class FormNewBid(forms.Form):
    bid = forms.DecimalField(label="New Bid:", decimal_places=2, min_value=1, localize=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))