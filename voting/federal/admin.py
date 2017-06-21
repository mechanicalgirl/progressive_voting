from django.contrib import admin
from django.utils.html import format_html

from .models import District, Candidate, Reasons, VoterRegistration, Messages, UnitedStatesMap
from .forms import CandidateModelForm

class VoterRegistrationAdmin(admin.ModelAdmin):
    ordering = ('state',)
    list_display = ('state', 'url', 'last_updated_date',)

class UnitedStatesMapAdmin(admin.ModelAdmin):
    ordering = ('path',)
    list_display = ('path',)

class ReasonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_type', 'active', 'reason_text', 'get_candidates')
    search_fields = ('reason_text',)
    readonly_fields = ('reason_candidates',)

    def reason_candidates(self, obj):
        associated_candidates = []
        candidates = obj.candidate_set.filter(active=True)
        for c in candidates:
            can = '<a href="/admin/federal/candidate/%s/" target="new">%s (%s) - %s-%s (%s)</a>' % \
                (c.id, c.name, c.party, c.district.state, c.district.district, c.district.type)
            associated_candidates.append(can)
        a = '<br>\n'.join(associated_candidates)
        return format_html(a)

    def get_candidates(self, obj):
        associated_candidates = obj.candidate_set.filter(active=True)
        return len(associated_candidates)
    get_candidates.short_description = 'Count'

    def get_type(self, obj):
        if obj.type == 'I':
            color = 'green'
        else:
            color = 'red'
        div = '<div style="width: 6px; border: 2px solid %s; padding: 0px; margin: 0px;"></div>' % color
        return format_html(div)
    get_type.short_description = 'Type'

class CandidateInline(admin.StackedInline):
    model = Candidate
    extra = 1

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
