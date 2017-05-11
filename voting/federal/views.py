from django.http import HttpResponse
from django.shortcuts import render

from .models import District, Candidate, VoterRegistration

def home(request):
    print(request.build_absolute_uri())
    if request.build_absolute_uri() == 'http://127.0.0.1:8000/':
        d = District.objects.all()
        context = {
            'districts': d,
        }
        return render(request, 'federal/index.html', context)
    return HttpResponse('')

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
