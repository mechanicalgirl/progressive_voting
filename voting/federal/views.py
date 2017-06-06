from django.http import HttpResponse
from django.shortcuts import render

from .models import District, Candidate, VoterRegistration
from .choices import STATE_CHOICES

def home(request):
    if request.build_absolute_uri() == 'http://127.0.0.1:8000/' or request.path == '/preview/':
        d = District.objects.all()
        district_groups = []
        for state in STATE_CHOICES:
            abbrev, label = state[0], state[1]
            districts_by_state = []
            districts = District.objects.filter(state=abbrev)
            for district in districts:
                i = Candidate.objects.filter(district=district.id, active=True, incumbent=True)
                val = ''
                incumbent_title = 'Click through to see incumbent(s)'
                if len(i) == 1:
                    val = i[0].party.lower()
                    if val == 'd':
                        incumbent_title = 'Democratic Incumbent'
                    if val == 'r':
                        incumbent_title = 'Republican Incumbent'
                if district.district == 'Senate' and len(i) == 2:
                    val = '%s, %s' % (i[0].party.lower(), i[1].party.lower())
                    incumbent_title = 'Multiple Incumbents'
                d = {'district': district, 'incumbent': val, 'incumbent_title': incumbent_title}
                districts_by_state.append(d)
            g = {'state_label': label, 'districts': districts_by_state}
            district_groups.append(g)
        context = {
            'district_groups': district_groups,
        }
        return render(request, 'federal/index.html', context)
    return HttpResponse('')

def by_district(request, district):
    state, dist = district.split('-')
    d = District.objects.get(state=state, district=dist)
    i = Candidate.objects.filter(district=d.id, active=True, incumbent=True)
    ic = Candidate.objects.filter(district=d.id, active=True, incumbent=False)
    context = {
        'district': d,
        'incumbent': i,
        'candidates': ic,
    }
    return render(request, 'federal/district.html', context)
