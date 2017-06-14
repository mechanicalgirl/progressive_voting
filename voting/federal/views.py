import sys
import requests

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
    state, dist = district.split('-', 1)
    d = District.objects.get(state=state, district=dist)
    i = Candidate.objects.filter(district=d.id, active=True, incumbent=True)
    ic = Candidate.objects.filter(district=d.id, active=True, incumbent=False)
    context = {
        'district': d,
        'incumbent': i,
        'candidates': ic,
    }
    return render(request, 'federal/district.html', context)

def get_new_candidates(request):
    """
    https://api.open.fec.gov/v1/candidates/search/?api_key=voQZ63Obcja8S2338pgGANCeSYmPMV0akuE49hS4&candidate_status=C&party=DEM&incumbent_challenge=C
    candidate_status -> One-letter code explaining if the candidate is: C (present candidate), F (future candidate), N (not yet a candidate), P (prior candidate)
    incumbent_challenge -> 'One-letter code ('I', 'C', 'O') explaining if the candidate is an incumbent, a challenger, or if the seat is open.'
    """

    api_key = 'voQZ63Obcja8S2338pgGANCeSYmPMV0akuE49hS4'
    base_url = 'https://api.open.fec.gov/v1'
    endpoint = '/candidates/search/'
    election_year = '2018' # make this an arg?

    new_candidates = []

    url = "%s%s?api_key=%s&candidate_status=C&party=DEM&incumbent_challenge=C&election_year=%s" % (base_url, endpoint, api_key, election_year)
    r = requests.get(url)
    if r.status_code == 200:
        results = r.json()['results']
        all_candidates = parse_new_candidates(results)

        current_page, total_pages = r.json()['pagination']['page'], r.json()['pagination']['pages']
        remaining_pages = total_pages - current_page
        for p in reversed(range(remaining_pages)):
            page = total_pages - p
            r = requests.get(url+"&page="+str(page))
            results = r.json()['results']
            candidates = parse_new_candidates(results)
            all_candidates = all_candidates + candidates

        all_candidates.sort()
        for c in all_candidates:
            candidate = Candidate.objects.get(candidate_id=c[2])
            if not candidate:
                district = District.objects.get(state=c[0].split('-')[0], district=c[0].split('-')[1])
                new_candidate = Candidate(name=c[1], district=district.pk, candidate_id=c[2])
                new_candidate.save()
                new_c = tuple(new_candidate.name, new_candidate.district, new_candidate.candidate_id)
                new_candidates.append(new_c)

    context = {
        'all': all_candidates,
        'new': new_candidates,
    }
    return render(request, 'federal/new_candidates.html', context)

def parse_new_candidates(results):
    candidates_list = []
    for candidate in results:
        candidate_name = "%s %s" % (candidate['name'].split()[1].title(), candidate['name'].split()[0][:-1].title())
        district = "%s-%s" % (candidate['state'], candidate['district_number'])
        c_list = tuple([district, candidate_name, candidate['candidate_id']])
        candidates_list.append(c_list)
    return candidates_list

def get_ids(request):
    api_key = 'voQZ63Obcja8S2338pgGANCeSYmPMV0akuE49hS4'
    base_url = 'https://api.open.fec.gov/v1'
    endpoint = '/candidates/search/'
    election_year = '2018' # make this a sys arg?

    """
    https://api.open.fec.gov/v1/candidates/search/?api_key=voQZ63Obcja8S2338pgGANCeSYmPMV0akuE49hS4&name=??
    """
    # SELECT name FROM federal_candidate WHERE candidate_id IS NULL ORDER BY name;
    candidates = Candidate.objects.filter(candidate_id=None, active=True, incumbent=True)
    for c in candidates:
        name = c.name
        # url = "%s%s?api_key=%s&name=%s&candidate_status=C" % (base_url, endpoint, api_key, name)
        url = "%s%s?api_key=%s&name=%s" % (base_url, endpoint, api_key, name)
        r = requests.get(url)
        if r.status_code == 200:
            results = r.json()['results']
            if results:
                candidate = parse_candidate(results, name)
            else:
                print("URL", url)
    return HttpResponse('')

def parse_candidate(results, name):
    for candidate in results:
        candidate_id = candidate['candidate_id']
        print("UPDATE federal_candidate SET candidate_id = '%s' WHERE name = '%s';" % (candidate_id, name))

