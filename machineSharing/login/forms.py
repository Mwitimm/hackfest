from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label=''
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Remove labels and help text for all fields
        for field_name in self.fields:
            self.fields[field_name].label = ''
            self.fields[field_name].help_text = ''

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


class EditUserForm(forms.Form):
    turn = forms.IntegerField()
    status = forms.ChoiceField(choices=[('verify', 'verify'), ('reject', 'reject')],
                               widget=forms.Select(attrs={'class': 'form-select'}))


class ContributionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get a list of usernames that have already made contributions this month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        paid_usernames = Contribution.objects.filter(
            contribution_month=current_month, contribution_year=current_year
        ).values_list('member', flat=True)

        # Exclude paid users from the queryset
        self.fields['username'].queryset = Account.objects.exclude(name__in=paid_usernames)

    username = forms.ModelChoiceField(queryset=Account.objects.all(), empty_label=None)


class Add_equipment(forms.Form):
    user_id = models.IntegerField()  # Replace with your actual field
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rental_rate = models.IntegerField()  # Replace with your actual field
    condition = models.CharField(max_length=20, choices=[('used', 'Used'), ('new', 'New')])
    img = models.ImageField(upload_to='images/', null=True, blank=True)
    desc = models.TextField()