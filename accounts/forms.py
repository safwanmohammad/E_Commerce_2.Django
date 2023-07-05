from django import forms
from . models import Account,UserProfile

class  RegistretionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class':'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class':'form-control',
    }))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={
    #     'placeholder': 'Enter your email',
    #     'class':'form-control',
    # }))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'placeholder': 'Enter your first name',
    #     'class':'form-control',
    # }))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'placeholder': 'Enter your last name',
    #     'class':'form-control',
    # }))
    # phone_number = forms.CharField(widget=forms.TextInput(attrs={
    #     'placeholder': 'Enter your phone number',
    #     'class':'form-control',
    #     # 'type':'number',
    # }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']

    def __init__(self,*args,**kwargs):
        super(RegistretionForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your emaial'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your phone number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistretionForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match !'
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')

    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,error_messages= {'invalid':("Image files Only")},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')

    def __init__(self,*args,**kwargs):
        super(UserProfileForm ,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'