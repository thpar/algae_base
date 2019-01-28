import requests

algae_base_url = "http://www.algaebase.org/search/species/"

## Sample GET request
## http://www.algaebase.org/search/species/detail/?species_id=1839

def get_species_page(species):
    payload = {'name': species,
               'currentMethod': 'species',
               'fromSearch': 'yes',
               'displayCount': '20',
               'sortBy': 'genus',
               'sortBy2': 'species'
    }
    r = requests.post(algae_base_url, data=payload)
    print(r.text)

