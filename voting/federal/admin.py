from django.contrib import admin

from .models import District, Candidate, Reasons, VoterRegistration, Messages
from .forms import CandidateModelForm

class VoterRegistrationAdmin(admin.ModelAdmin):
    ordering = ('state',)
    list_display = ('state', 'url', 'last_updated_date',)

class CandidateInline(admin.StackedInline):
    model = Candidate
    extra = 1

class ReasonsAdmin(admin.ModelAdmin):
    list_display = ('active', 'type', 'reason_text',)

class DistrictAdmin(admin.ModelAdmin):
    ordering = ('state', 'type', 'district',)
    list_display = ('state', 'type', 'district', 'incumbent', 'district_candidate_count', 'next_primary_date', 'next_election_date',)
    list_filter = ('state',)

    inlines = [
        CandidateInline,
    ]

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
    ordering = ('district', 'position')
    list_display = ('name', 'candidate_id', 'active', 'incumbent', 'party', 'district', 'position', 'term_end',)
    list_filter = ('district__state',)
    search_fields = ('name',)
    form = CandidateModelForm

class MessageAdmin(admin.ModelAdmin):
    ordering = ('date_to_post',)
    list_display = ('date_to_post', 'active', 'posted',)


admin.site.register(District, DistrictAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(VoterRegistration, VoterRegistrationAdmin)
admin.site.register(Messages, MessageAdmin)
admin.site.register(Reasons, ReasonsAdmin)
