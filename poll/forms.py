from django import forms
from django.utils.translation import gettext_lazy as _
from poll.constants import StatusChoices
from geo.models import Station
from people.models import Candidate


class EventForm(forms.Form):
    code = forms.CharField(required=True)
    title = forms.CharField(required=True)
    agent = forms.CharField(required=True)

class OfficeForm(forms.Form):
    title = forms.CharField(required=True)
    agent = forms.CharField(required=True)
    nation = forms.CharField(required=True)
    details = forms.CharField(widget=forms.Textarea, required=True)
    status = forms.CharField(required=True)
    
class PositionForm(forms.Form):
    title = forms.CharField(required=True)
    level = forms.CharField(required=True)
    zone = forms.CharField(required=True)
    details = forms.CharField(widget=forms.Textarea, required=True)

class ResultForm(forms.Form):
    station = forms.ModelChoiceField(label=_('Station'), 
                                      queryset=Station.objects.filter(pk=1),
                                      widget=forms.Select(attrs={
                                        'class':'form-control',
                                        'placeholder': 'select position'
                                      }),
                                      required=True)
    candidate = forms.ModelChoiceField(label=_('Candidate'), 
                                      queryset=Candidate.objects.all(),
                                      widget=forms.Select(attrs={
                                        'class':'form-control',
                                        'placeholder': 'select party'
                                      }),
                                      required=True)
    total_votes = forms.CharField(label=_('Total Votes'), required=True)
    constituency_agent = forms.CharField(label=_('Agent'), required=True)
    details = forms.CharField(widget=forms.Textarea(attrs={
                                                           'class':'form-control',
                                                           'placeholder': 'enter details'
                                                   }), required=True)
    status = forms.CharField(required=True)
    result_sheet = forms.FileField(label=_('Upload result sheet'),
                                   help_text=_('Max. 4 kilobytes'))
    status = forms.ChoiceField(label=_("Status"), choices=StatusChoices.choices,
                               widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        text_attrs={
            "placeholder": "enter nation Name",
            "class": "form-control",
        }
        text_attrs["placeholder"] = "select constituency agent"
        self.fields['constituency_agent'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "enter number of votes"
        self.fields['total_votes'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "enter details"
        self.fields['details'].widget=forms.TextInput(attrs=text_attrs)

    
class ResultApprovalForm(forms.Form):
    title = forms.CharField(required=True)
    agent = forms.CharField(required=True)
    details = forms.CharField(widget=forms.Textarea, required=True)
    status = forms.CharField(required=True)
