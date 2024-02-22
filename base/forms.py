from django.forms import ModelForm
from .models import Shoe


class RoomForm(ModelForm):
    class Meta:
        model = Shoe
        fields = '__all__'
