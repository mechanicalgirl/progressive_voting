from datetime import date

from django.db import models

from .choices import STATE_CHOICES, PARTY_CHOICES, POSITION_CHOICES

class VoterRegistration(models.Model):
    state = models.CharField(max_length=2, choices=STATE_CHOICES, unique=True)
    url = models.CharField(max_length=200)
    last_updated_date = models.DateField(default=date.today)

    def __str__(self):
        return "%s voter registration" % self.state

class District(models.Model):
    """
    House districts, Senate seats at Federal level
    # House districts, Senate seats at State level
    # Other State level races, such as Governor, Lt. Governor
    """

    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    district = models.CharField(max_length=8, default="Senate")

    # zip_codes - TBD
    # lat/lng or map info - TBD
    voter_reg_url = models.ForeignKey(VoterRegistration, null=True, blank=True)

    next_primary_date = models.DateField('Next Primary', null=True, blank=True)
    next_early_vote_date_begin = models.DateField('Early Voting Begins', null=True, blank=True)
    next_early_vote_date_end = models.DateField('Early Voting Ends', null=True, blank=True)
    next_election_date = models.DateField('Election Date', null=True, blank=True)

    class Meta:
        ordering = ["state", "district"]
        unique_together = ("state", "district")

    def __str__(self):
        # self.get_level_display()
        return "%s-%s" % (self.state, self.district)

class Candidate(models.Model):
    active = models.BooleanField(default=True)
    incumbent = models.BooleanField(default=False)
    party = models.CharField(max_length=1, choices=PARTY_CHOICES)
    term_end = models.DateField('Term End', null=True, blank=True)

    district = models.ForeignKey(District)
    position = models.CharField(max_length=200, choices=POSITION_CHOICES)

    name = models.CharField(max_length=200, unique=True)
    url = models.CharField(max_length=200, null=True, blank=True)

    twitter_handle = models.CharField(max_length=100, null=True, blank=True)
    tweet_text = models.TextField(max_length=135, null=True, blank=True)

    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    facebook_text = models.TextField(null=True, blank=True)

    reasons_to_keep = models.TextField(null=True, blank=True)
    reasons_to_vote_out = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s (%s) - %s" % (self.name, self.party, self.district)
