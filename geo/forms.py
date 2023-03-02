from django import forms
from poll.constants import StatusChoices
from .models import Nation, Region, Constituency, Station

class NationForm(forms.Form):
    code = forms.CharField(required=True, label="Two-Letter Code")
    title = forms.CharField(required=True, label="Nation Name")
    agent = forms.CharField(required=True, label="Party Agent")

    def __init__(self, *args, **kwargs):
            super(NationForm, self).__init__(*args, **kwargs)
            text_attrs={
                "placeholder": "enter nation Name",
                "class": "form-control",
            }
            text_attrs["placeholder"] = "enter nation name"
            self.fields['code'].widget=forms.TextInput(attrs=text_attrs)
            text_attrs["placeholder"] = "nation two letter code"
            self.fields['title'].widget=forms.TextInput(attrs=text_attrs)
            text_attrs["placeholder"] = "select party agent"
            self.fields['agent'].widget=forms.TextInput(attrs=text_attrs)


class RegionForm(forms.Form):
    title = forms.CharField(required=True)
    agent = forms.CharField(required=True)
    nation = forms.ModelChoiceField(label="Nation", queryset=Nation.objects.all(),
                               widget=forms.Select(attrs={'class':'form-control'}))
    details = forms.CharField(widget=forms.Textarea, required=True)
    status = forms.ChoiceField(label="Status", choices=StatusChoices.choices,
                               widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
            super(RegionForm, self).__init__(*args, **kwargs)
            text_attrs={
                "placeholder": "enter nation Name",
                "class": "form-control",
            }
            text_attrs["placeholder"] = "enter region name"
            self.fields['title'].widget=forms.TextInput(attrs=text_attrs)
            text_attrs["placeholder"] = "nation two letter code"
            self.fields['details'].widget=forms.TextInput(attrs=text_attrs)
            text_attrs["placeholder"] = "select party agent"
            self.fields['agent'].widget=forms.TextInput(attrs=text_attrs)


class ConstituencyForm(forms.Form):
    title = forms.CharField(required=True)
    agent = forms.CharField(required=True)
    region = forms.ModelChoiceField(label="Region",
                                    queryset=Region.objects.all(),
                                    widget=forms.Select(attrs={
                                        'class':'form-control',
                                        'placeholder': 'select region'
                                        }))
    details = forms.CharField(widget=forms.Textarea, required=True)
    status = forms.ChoiceField(label="Status", choices=StatusChoices.choices,
                               widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
            super(ConstituencyForm, self).__init__(*args, **kwargs)
            text_attrs={
                "placeholder": "enter nation name",
                "class": "form-control",
            }
            text_attrs["placeholder"] = "enter contituency name"
            self.fields['title'].widget=forms.TextInput(attrs=text_attrs)
            text_attrs["placeholder"] = "enter details"
            self.fields['details'].widget=forms.TextInput(attrs=text_attrs)
            text_attrs["placeholder"] = "select party agent"
            self.fields['agent'].widget=forms.TextInput(attrs=text_attrs)


class StationForm(forms.Form):
    code = forms.CharField(required=True)
    title = forms.CharField(required=True)
    constituency = forms.ModelChoiceField(label="Constituency", queryset=Constituency.objects.all(),
                               widget=forms.Select(attrs={'class':'form-control'}))
    details = forms.CharField(widget=forms.Textarea, required=True)
    status = forms.ChoiceField(label="Status", choices=StatusChoices.choices,
                               widget=forms.Select(attrs={'class':'form-control'}))
    agent = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
            super(StationForm, self).__init__(*args, **kwargs)
            text_attrs={
                "placeholder": "enter nation name",
                "class": "form-control",
            }
            text_attrs["placeholder"] = "enter contituency code"
            self.fields['code'].widget=forms.TextInput(attrs=text_attrs)
            text_attrs["placeholder"] = "enter contituency name"
            self.fields['title'].widget=forms.TextInput(attrs=text_attrs)
            text_attrs["placeholder"] = "enter details"
            self.fields['details'].widget=forms.TextInput(attrs=text_attrs)
            text_attrs["placeholder"] = "select party agent"
            self.fields['agent'].widget=forms.TextInput(attrs=text_attrs)
