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
        if len(incumbent) > 0:
            val = incumbent[0].party
        return val
    incumbent.short_description = "Incumbent"

    def district_candidate_count(self, obj):
        return obj.candidate_set.filter(active=True, running=True).count()
    district_candidate_count.short_description = "Total Candidates"

class CandidateAdmin(admin.ModelAdmin):
    ordering = ('district',)
    list_display = ('name', 'active', 'incumbent', 'running', 'party', 'district', 'position',)
    list_filter = ('district__state',)
    form = CandidateModelForm

admin.site.register(District, DistrictAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(VoterRegistration, VoterRegistrationAdmin)
