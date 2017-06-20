from django.contrib import admin

from .models import District, Candidate, Reasons, VoterRegistration, Messages, UnitedStatesMap
from .forms import CandidateModelForm

class VoterRegistrationAdmin(admin.ModelAdmin):
    ordering = ('state',)
    list_display = ('state', 'url', 'last_updated_date',)

class UnitedStatesMapAdmin(admin.ModelAdmin):
    ordering = ('path',)
    list_display = ('path',)

class CandidateInline(admin.StackedInline):
    model = Candidate
    extra = 1

class ReasonsAdmin(admin.ModelAdmin):
    list_display = ('active', 'type', 'reason_text',)

class DistrictAdmin(admin.ModelAdmin):
    ordering = ('state', 'type', 'district',)
    list_display = ('full_district', 'state', 'type', 'district', 'incumbent', 'district_candidate_count', 'next_primary_date', 'next_election_date',)
    list_filter = ('state',)

    inlines = [
        CandidateInline,
    ]

    def full_district(self, obj):
        return ("%s-%s-%s" % (obj.state, obj.district, obj.type))
    full_district.short_description = 'District'

    def incumbent(self, obj):
        incumbent = obj.candidate_set.get(active=True, incumbent=True)
        return incumbent.party
    incumbent.short_description = "Incumbent"

    def district_candidate_count(self, obj):
        return obj.candidate_set.filter(active=True, incumbent=False).count()
    district_candidate_count.short_description = "Challengers"

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
admin.site.register(UnitedStatesMap, UnitedStatesMapAdmin)
