from django import forms

class Subscribe(forms.Form):
    Email = forms.EmailField(widget=forms.TextInput(attrs={'class':'sub-form-field','placeholder':'E-mail'}))

    def __str__(self):
        return self.Email
