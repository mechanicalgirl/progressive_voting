from django import forms
from django.core.exceptions import ValidationError

from .models import Candidate

class CandidateModelForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['active', 'incumbent', 'party', 'district', 'position', 'name', 'candidate_id', 'term_end', 'url', 'twitter_handle', 'facebook_url', 'reasons', 'bio', 'comments']
