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
        fields = ['cycle', 'cycle_prepa', 'cycle_eng', 'filiere','section','image']
        widgets = {
            'cycle': forms.Select(attrs={'class': 'sec form-control','id':'cycle'}),
            'cycle_prepa': forms.Select(attrs={'class': 'sec form-control','id':'cycle_prep'}),
            'cycle_eng': forms.Select(attrs={'class': 'sec form-control','id':'cycle_eng'}),
            'section': forms.Select(attrs={'class': 'sec form-control','id':'cycle_sec'}),
            'filiere': forms.Select(attrs={'class': 'sec form-control','id':'cycle_fil'}),
            'image': forms.FileInput(attrs={'class': 'form-control' ,'id':'file-input'}),
        }
    def __init__(self, *args, **kwargs):
        super(SeanceData, self).__init__(*args, **kwargs)
        self.fields['cycle_prepa'].required = False
        self.fields['cycle_eng'].required = False
        self.fields['filiere'].required = False
        self.fields['section'].required = False
        self.fields['cycle_prepa'].initial = ''
        self.fields['cycle_eng'].initial = ''
        self.fields['filiere'].initial = ''
        self.fields['section'].initial = ''
        self.fields['cycle'].initial = ''


