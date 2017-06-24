from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from .choices import STATE_CHOICES, PARTY_CHOICES, POSITION_CHOICES, DISTRICT_TYPE_CHOICES

class VoterRegistration(models.Model):
    state = models.CharField(max_length=2, choices=STATE_CHOICES, unique=True)
    url = models.CharField(max_length=200)
    last_updated_date = models.DateField(default=date.today)

    def __str__(self):
        return "%s voter registration" % self.state

class UnitedStatesMap(models.Model):
    """
    A collection of state dimensions to fill in a US map
    """
    path = models.CharField(max_length=2, choices=STATE_CHOICES, unique=True)
    fill = models.CharField(max_length=6, default='D3D3D3')
    dimensions = models.TextField()

    class Meta:
        verbose_name_plural = "US Map Coordinates"
        verbose_name = "US Map Coordinates"

    def __str__(self):
        return "%s map" % self.path

class District(models.Model):
    """
    House districts, Senate seats at Federal level
    # House districts, Senate seats at State level
    # Other State level races, such as Governor, Lt. Governor
    """

    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    district = models.IntegerField()
    type = models.CharField(max_length=2, choices=DISTRICT_TYPE_CHOICES, default="H")

    # zip_codes - TBD
    # lat/lng or map info - TBD
    voter_reg_url = models.ForeignKey(VoterRegistration, null=True, blank=True)

    next_primary_date = models.DateField('Next Primary', null=True, blank=True)
    next_early_vote_date_begin = models.DateField('Early Voting Begins', null=True, blank=True)
    next_early_vote_date_end = models.DateField('Early Voting Ends', null=True, blank=True)
    next_election_date = models.DateField('Election Date', null=True, blank=True)

    class Meta:
        ordering = ["state", "district"]
        unique_together = ("state", "district", "type")

    def __str__(self):
        # self.get_level_display()
        return "%s-%s-%s" % (self.state, self.district, self.type)

class Reasons(models.Model):
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=4, choices=((u'O', u'Vote Out'), (u'I', u'Keep In'),))
    reason_title = models.CharField(max_length=50, null=True, blank=True)
    reason_text = models.TextField()

    class Meta:
        verbose_name_plural = "reasons"

    def __str__(self):
        return "(%s) %s" % (self.type, self.reason_text)

class Candidate(models.Model):
    active = models.BooleanField(default=True)
    incumbent = models.BooleanField(default=False)
    party = models.CharField(max_length=1, choices=PARTY_CHOICES)
    term_end = models.DateField('Term End', null=True, blank=True)

    district = models.ForeignKey(District)
    position = models.CharField(max_length=200, choices=POSITION_CHOICES)
    candidate_id = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True, blank=True)

    twitter_handle = models.CharField(max_length=100, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)

    reasons = models.ManyToManyField(Reasons, blank=True)

    bio = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["district", "position"]
        unique_together = ("name", "district")

    def __str__(self):
        return "%s (%s) - %s" % (self.name, self.party, self.district)


class Messages(models.Model):
    active = models.BooleanField(default=True)
    posted = models.BooleanField(default=True)
    date_to_post = models.DateTimeField('date to post', null=True, blank=True)
    tweet_text = models.CharField(max_length=135, null=True, blank=True)
    facebook_text = models.TextField(null=True, blank=True)

    def clean(self):
        if self.tweet_text is None and not self.facebook_text:
            raise ValidationError("Twitter text and/or Facebook text must be populated")

    class Meta:
        ordering = ["active", "posted", "-date_to_post"]
        verbose_name_plural = "messages"
