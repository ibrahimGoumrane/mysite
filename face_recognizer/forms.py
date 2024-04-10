from django import  forms
from .models import UtilsData
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'firstName', 'email', 'subject', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'firstName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description','rows': 5, 'cols': 40}),
        }
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = False


class SeanceData(forms.ModelForm):
    class Meta:
        model = UtilsData
        fields = ['module_name', 'cycle', 'cycle_prepa', 'cycle_eng', 'filiere','image']
        widgets = {
            'module_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cycle': forms.Select(attrs={'class': 'form-control'}),
            'cycle_prepa': forms.Select(attrs={'class': 'form-control'}),
            'cycle_eng': forms.Select(attrs={'class': 'form-control'}),
            'filiere': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SeanceData, self).__init__(*args, **kwargs)
        self.fields['cycle_prepa'].required = False
        self.fields['cycle_eng'].required = False
        self.fields['filiere'].required = False
    #     for field in self.fields:
    #         self.fields[field].label = False
            # self.fields[field].widget.attrs['class'] = 'form-control'
            # self.fields[field].widget.attrs['placeholder'] = field

        # Dynamic population of choices for filiere field based on cycle selection
        # if 'cycle' in self.data:

        #     cycle = self.data.get('cycle')
        #     if cycle == 'prepa':
        #         self.fields['filiere'].choices =cycle_year['prep_years']
        #     elif cycle == 'engineer':
        #         self.fields['filiere'].choices =cycle_year['engineer_years']

