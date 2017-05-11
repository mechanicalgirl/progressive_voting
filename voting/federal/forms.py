from django import forms
from django.core.exceptions import ValidationError

from .models import Candidate

class CandidateModelForm(forms.ModelForm):
    tweet_text = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Candidate
        fields = ['active', 'incumbent', 'party', 'district', 'position', 'name', 'url', 'twitter_handle', 'tweet_text', 'facebook_url', 'facebook_text', 'reasons_to_keep', 'reasons_to_vote_out', 'bio', 'comments']
