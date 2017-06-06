from django.contrib import admin

from .models import District, Candidate, VoterRegistration
from .forms import CandidateModelForm

class VoterRegistrationAdmin(admin.ModelAdmin):
    ordering = ('state',)
    list_display = ('state', 'url', 'last_updated_date',)

class CandidateInline(admin.StackedInline):
    model = Candidate
    extra = 1

class DistrictAdmin(admin.ModelAdmin):
    ordering = ('state', 'district',)
    list_display = ('state', 'district_or_senate', 'incumbent', 'district_candidate_count', 'next_primary_date', 'next_election_date',)
    list_filter = ('state',)

    inlines = [
        CandidateInline,
    ]

    def district_or_senate(self, obj):
        val = obj.district
        if obj.district != 'Senate':
            val = 'House %s' % obj.district
        return val

    def incumbent(self, obj):
        val = ''
        incumbent = obj.candidate_set.filter(active=True, incumbent=True)
        if len(incumbent) == 1:
            val = incumbent[0].party
        if obj.district == 'Senate' and len(incumbent) == 2:
            val = '%s, %s' % (incumbent[0].party, incumbent[1].party)
        return val
    incumbent.short_description = "Incumbent"

    def next_up(self, obj):
        candidates = obj.candidate_set.filter(active=True)
        dates = []
        for c in candidates:
            if c.term_end:
                dates.append(c.term_end)
        if len(dates) > 0:
            dates.sort(reverse=False)
            return dates[0]
        return None

    def district_candidate_count(self, obj):
        return obj.candidate_set.filter(active=True, incumbent=False).count()
    district_candidate_count.short_description = "Challenging Candidates"

class CandidateAdmin(admin.ModelAdmin):
    ordering = ('district',)
    list_display = ('name', 'active', 'incumbent', 'party', 'district', 'position', 'term_end',)
    list_filter = ('district__state',)
    form = CandidateModelForm

admin.site.register(District, DistrictAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(VoterRegistration, VoterRegistrationAdmin)
