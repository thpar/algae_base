import requests
from pyquery import PyQuery as pq
import html as html_goodies

algae_base_url = "http://www.algaebase.org/search/species/"
algae_base_species_details_url = "http://www.algaebase.org/search/species/detail/"

def search_species_page(species):
    payload = {'name': species,
               'currentMethod': 'species',
               'fromSearch': 'yes',
               'displayCount': '20',
               'sortBy': 'genus',
               'sortBy2': 'species'
    }
    r = requests.post(algae_base_url, data=payload)
    return r.text

def is_accepted(html):
    d = pq(html)
    p = d('p b:contains("Status of name") + br + span')
    return "entity that is currently accepted taxonomically" in p.text()

def get_synonym_page(html):
    d = pq(html)
    a = d('p b:contains("Status of name") + br + span a')
    species_id = a.attr['href'].split('=')[1]
    r = requests.get(algae_base_species_details_url, params={'species_id': species_id})
    return r.text

def get_classification_data(html, data_type):
    d = pq(html)
    b = d('#detailsidebar p i b:contains("{}")'.format(data_type))
    i = b.parent()
    return i.next().text()

def get_accepted_name(html):
    d = pq(html)
    i = d('p b:contains("Publication details") + br + i')
    return i.text()

def get_authority(html):
    d = pq(html)
    p = d('p b:contains("Publication details")').parent()
    auth = p.html().split('</i> ')[1].split(':')[0]    
    return html_goodies.unescape(auth)
    
def get_data(html):
    data = {}
    data['Order'] = get_classification_data(html, 'Order')
    data['Family'] = get_classification_data(html, 'Family')
    data['Genus'] = get_classification_data(html, 'Genus')
    data['Species'] = get_accepted_name(html)
    data['Authority'] = get_authority(html)
    return data

def retrieve(species):
    html = search_species_page(species)
    if not is_accepted(html):
        html = get_synonym_page(html)
    data = get_data(html)
    print(data)

    
