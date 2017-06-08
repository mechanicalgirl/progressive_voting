from django import forms
from django.core.exceptions import ValidationError

from .models import Candidate

class CandidateModelForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['active', 'incumbent', 'party', 'district', 'position', 'name', 'term_end', 'url', 'twitter_handle', 'facebook_url', 'reasons_to_keep', 'reasons_to_vote_out', 'bio', 'comments']
