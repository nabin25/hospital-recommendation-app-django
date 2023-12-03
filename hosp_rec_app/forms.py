from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Schedule, Preference

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': '',
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'hosp','details']
        labels = {
            'date': 'Date',
            'hosp': 'Hospital',
            'details': 'Additional details',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-6 mb-0'),
                Column('hosp', css_class='form-group col-md-6 mb-0'),
                Column('details', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )
    def save(self, commit=True, user=None):
            instance = super().save(commit=False)
            if user:
                instance.user = user
            if commit:
                instance.save()
            return instance
    
class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['preferred_hosp']
        labels = {
            'preferred_hosp': 'Hospital',
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('preferred_hosp', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )
    def save(self, commit=True, user=None):
            instance = super().save(commit=False)
            if user:
                instance.user = user
            if commit:
                instance.save()
            return instance


from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from .models import Hospital

class HospitalForm(forms.ModelForm):
    hosSpec = SimpleArrayField(forms.ChoiceField(choices=Hospital.CAT, widget=forms.CheckboxSelectMultiple))

    class Meta:
        model = Hospital
        fields = '__all__'


