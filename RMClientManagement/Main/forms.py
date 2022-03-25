from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Email, Document

hidden_input = forms.TextInput(attrs={'type': 'hidden'})

class BaseForm(forms.ModelForm):
    '''
        base class for forms
        - applies basic styling to all fields
    '''
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ClientForm(UserCreationForm, BaseForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class RequestDocumentForm(BaseForm):
    subject = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Email
        fields = ['subject', 'body', 'sender', 'recipient']
        widgets = {
            'sender': hidden_input,
            'recipient': hidden_input,
        }

class SubmitDocumentForm(BaseForm):
    custom_name = forms.CharField(max_length=255, required=False, label="Document name")

    class Meta:
        model = Document
        fields = ['custom_name', 'document', 'document_type', 'uploaded_by', 'email']
        widgets = {
            'uploaded_by': hidden_input,
            'email': hidden_input,
        }

