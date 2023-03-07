from django import forms
from poll.constants import StatusChoices
from people.models import Party, Candidate, Agent
from poll.models import Position


class AgentForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(required=True)
    descriptions = forms.CharField(required=True)
    zone_ct = forms.CharField(required=True)
    zone_id = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        text_attrs={
            "placeholder": "enter nation Name",
            "class": "form-control",
        }
        self.fields['first_name'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "enter agent first name"
        self.fields['last_name'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "enter agent last name"
        self.fields['email'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "enter agent email"
        self.fields['phone'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "enter address"
        self.fields['address'].widget=forms.Textarea(attrs=text_attrs)
        text_attrs["placeholder"] = "enter details"
        self.fields['descriptions'].widget=forms.Textarea(attrs=text_attrs)
        text_attrs["placeholder"] = "select zone type"
        self.fields['zone_ct'].widget=forms.Select(attrs=text_attrs)
        text_attrs["placeholder"] = "select zone"
        self.fields['zone_id'].widget=forms.Select(attrs=text_attrs)


class CandidateForm(forms.Form):
    prefix = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    other_names = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    status = forms.ChoiceField(label="Status", choices=StatusChoices.choices,
                               widget=forms.Select(attrs={'class':'form-control'}))
    position = forms.ModelChoiceField(label="Position", queryset=Position.objects.all(),
                               widget=forms.Select(attrs={'class':'form-control'}))
    party = forms.ModelChoiceField(label="Party", queryset=Party.objects.all(),
                               widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        text_attrs={
            "placeholder": "enter nation name",
            "class": "form-control",
        }
        text_attrs["placeholder"] = "enter contituency code"
        self.fields['prefix'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "enter contituency name"
        self.fields['first_name'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "enter details"
        self.fields['last_name'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "select party agent"
        self.fields['other_names'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "select party agent"
        self.fields['address'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "select party agent"
        self.fields['description'].widget=forms.TextInput(attrs=text_attrs)


class PartyForm(forms.Form):
    code = forms.CharField(required=True)
    title = forms.CharField(required=True)
    agent = forms.CharField(required=True)
    details = forms.CharField(widget=forms.Textarea(attrs={
                "placeholder": "enter detials",
                "class": "form-control",
            }), required=True)
    status = forms.ChoiceField(label="Status", choices=StatusChoices.choices,
                               widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(PartyForm, self).__init__(*args, **kwargs)
        text_attrs={
            "placeholder": "enter party name",
            "class": "form-control",
        }
        self.fields['title'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "enter party name"
        self.fields['code'].widget=forms.TextInput(attrs=text_attrs)
        text_attrs["placeholder"] = "select party agent"
        self.fields['agent'].widget=forms.TextInput(attrs=text_attrs)




'''

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
'''
