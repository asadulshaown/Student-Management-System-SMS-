
# forms.py
from django import forms
from .models import StudentRequest,Student

class ApproveStudentForm(forms.ModelForm):
    class Meta:
        model = StudentRequest
        fields = ['roll','HonorsRegisterNO'] # roll field set
        
        widgets = {
            'roll': forms.TextInput(attrs={
                'class': 'form-control text-white bg-dark border-info',
                'placeholder': 'Enter Roll Number',
            }),
            'HonorsRegisterNO': forms.TextInput(attrs={
                'class': 'form-control text-white bg-dark border-info',
                'placeholder': 'Enter Honors Register No',
            }),
        }
   
   # validate data in admin form     
    def clean(self):
        cleaned_data = super().clean()
        roll = cleaned_data.get('roll')
        honors = cleaned_data.get('HonorsRegisterNO')

        if not roll or not honors:
            raise forms.ValidationError("Both Roll and Honors RegisterNo are required to approve!")
