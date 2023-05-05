from django import forms
from .models import Account

class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter password',
        'class': 'form-control',
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email']

  

    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'your first name'    
        self.fields['last_name'].widget.attrs['placeholder'] = 'your last name'    
        self.fields['email'].widget.attrs['placeholder'] = 'your email'    
        self.fields['phone_number'].widget.attrs['placeholder'] = 'your phone number'    
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'    


    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password!= confirm_password:
            raise forms.ValidationError("password doesnot match")        


  