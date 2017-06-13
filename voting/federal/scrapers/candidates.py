import json
import sys

import requests

api_key = 'voQZ63Obcja8S2338pgGANCeSYmPMV0akuE49hS4'
base_url = 'https://api.open.fec.gov/v1'
endpoint = '/candidates/search/'
election_year = '2018' # make this a sys arg?

def search_candidates():
    """
    https://api.open.fec.gov/v1/candidates/search/?api_key=voQZ63Obcja8S2338pgGANCeSYmPMV0akuE49hS4&candidate_status=C&party=DEM&incumbent_challenge=C
    candidate_status -> One-letter code explaining if the candidate is: C (present candidate), F (future candidate), N (not yet a candidate), P (prior candidate)
    incumbent_challenge -> 'One-letter code ('I', 'C', 'O') explaining if the candidate is an incumbent, a challenger, or if the seat is open.'
    """
    url = "%s%s?api_key=%s&candidate_status=C&party=DEM&incumbent_challenge=C&election_year=%s" % (base_url, endpoint, api_key, election_year)
    r = requests.get(url)
    if r.status_code == 200:
        results = r.json()['results']
        all_candidates = parse_candidates(results)

        current_page, total_pages = r.json()['pagination']['page'], r.json()['pagination']['pages']
        remaining_pages = total_pages - current_page
        for p in reversed(range(remaining_pages)):
            page = total_pages - p
            r = requests.get(url+"&page="+str(page))
            results = r.json()['results']
            candidates = parse_candidates(results)
            all_candidates = all_candidates + candidates

        all_candidates.sort()
        for c in all_candidates:
            print(c)
            print("SELECT * FROM candidates WHERE candidate_id = '%s';" % c[2])
            # if no result: get district.id
            print("SELECT id FROM federal_district WHERE state = %s AND district = %s;" % (c[0].split('-')[0], c[0].split('-')[1]))
            print("INSERT INTO federal_candidates (name, district_id, candidate_id) VALUES ('%s', '%s', '%s')" % (c[1], 'district_id', c[2]))

def parse_candidates(results):
    candidates_list = []
    for candidate in results:
        candidate_name = "%s %s" % (candidate['name'].split()[1].title(), candidate['name'].split()[0][:-1].title())
        district = "%s-%s" % (candidate['state'], candidate['district_number'])
        c_list = tuple([district, candidate_name, candidate['candidate_id']])
        candidates_list.append(c_list)
    return candidates_list

if __name__ == '__main__':
    search_candidates()
