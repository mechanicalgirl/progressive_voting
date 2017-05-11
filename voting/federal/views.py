from django.shortcuts import render

from .models import District, Candidate, VoterRegistration

def home(request):
    d = District.objects.all()
    context = {
        'districts': d,
    }
    return render(request, 'federal/index.html', context)

def by_district(request, district):
    state, dist = district.split('-')
    d = District.objects.get(state=state, district=dist)
    i = Candidate.objects.get(district=d.id, active=True, incumbent=True)
    ic = Candidate.objects.filter(district=d.id, active=True, incumbent=False)
    context = {
        'district': d,
        'incumbent': i,
        'candidates': ic,
    }
    return render(request, 'federal/district.html', context)
