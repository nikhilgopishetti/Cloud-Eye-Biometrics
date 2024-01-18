from django import forms
from .models import Employee

from django import forms
from .models import Role, Department
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description', 'responsibilities']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'responsibilities': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            'responsibilities',
            Submit('submit', 'Add Role', css_class='btn-primary')
        )
        self.helper.form_method = 'post'

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description',
            Submit('submit', 'Add Department', css_class='btn-primary')
        )
        self.helper.form_method = 'post'

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'  # You can specify the fields you want in the form here if not all

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields for styling
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
