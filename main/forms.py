from django import forms
from .models import ImageModel

class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']

from .models import UserPassphrase

class PassphraseForm(forms.ModelForm):
    class Meta:
        model = UserPassphrase
        fields = ['expected_passphrase']