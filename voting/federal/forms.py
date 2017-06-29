from django import forms
from django.db import models
from django.core.exceptions import ValidationError

from .models import Candidate

class CandidateModelForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['active', 'incumbent', 'party', 'district', 'position', 'name', 'candidate_id', 'term_end', 'url', 'twitter_handle', 'facebook_url', 'reasons', 'bio', 'comments']

class SearchForm(forms.Form):
    name = forms.CharField(label="Name", max_length=64, required=False)
