from django import forms
from .models import *


def validate_strong_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Must include an uppercase letter.')
    if not re.search(r'[a-z]', value):
        raise ValidationError('Must include a lowercase letter.')
    if not re.search(r'\d', value):
        raise ValidationError('Must include a number.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError('Must include a special character.')

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=
                                                          {'placeholder':'eg:Maha@123',
                                                            'class':'form-control'
                                                            }),
                               validators=[validate_strong_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
                                                                  {'placeholder':'eg:Maha@123',
                                                                         'class':'form-control'}
                                                                  ))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
        
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Maha'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Laxmi'
        self.fields['email'].widget.attrs['placeholder'] = 'someone@gmail.com'
        self.fields['phone_number'].widget.attrs['placeholder'] = '1234567890'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'border: 1px solid orange;'
            
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(" Password Not Match ")
        
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number']
        
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['style'] = 'border: 1px solid orange;'
        
        
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages= { 'invalid' :("Image files only")},widget=forms.FileInput)
    class Meta:
        model = User_Profile_Model
        fields = ['address_line_1','address_line_2','city','state','profile_picture']
        
    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'