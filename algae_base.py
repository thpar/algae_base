import sys
import requests
from pyquery import PyQuery as pq
import html as html_goodies
import click

algae_base_url = "http://www.algaebase.org/search/species/"
algae_base_species_details_url = "http://www.algaebase.org/search/species/detail/"

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def search_species_page(species):
    payload = {'name': species,
               'currentMethod': 'species',
               'fromSearch': 'yes',
               'displayCount': '20',
               'sortBy': 'genus',
               'sortBy2': 'species'
    }
    r = requests.post(algae_base_url, data=payload)
    check_valid_page(r, species)    
    return r.text

def is_accepted(html):
    d = pq(html)
    p = d('p b:contains("Status of name") + br + span')
    return not p or "entity that is currently accepted taxonomically" in p.text()

def check_valid_page(r, species):
    if "no records were found with your search parameters" in r.text:
        raise ValueError("Species not found: "+species)
    if "For more detail, click on the name or the currently accepted name" in r.text:
        raise ValueError("Multiple entries found: "+species)
    if "An error has occurred" in r.text:
        raise ValueError("Error occurred for: "+species)

def get_synonym_page(html, species):
    d = pq(html)
    a = d('p b:contains("Status of name") + br + span a')
    species_id = a.attr['href'].split('=')[1]
    r = requests.get(algae_base_species_details_url, params={'species_id': species_id})
    check_valid_page(r, species)
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
    auth_part = p.html().split('</i>')[1]
    auth = auth_part.split(':')[0]
    return html_goodies.unescape(auth.strip())
    
def get_data(html, include_auth=False):
    data = {}
    data['Order'] = get_classification_data(html, 'Order')
    data['Family'] = get_classification_data(html, 'Family')
    data['Genus'] = get_classification_data(html, 'Genus')
    if include_auth:
        data['Species'] = get_accepted_name(html)
        data['Authority'] = get_authority(html)
    else:
        data['Species'] = ''
        data['Authority'] = ''
    return data

def retrieve(species):
    html = search_species_page(species)
    if not is_accepted(html):
        html = get_synonym_page(html, species)
        data = get_data(html, include_auth=True)
    else:
        data = get_data(html)
    return data

    
def process_file(missing_file_name):
    with open(missing_file_name) as missing_file:
        for line in missing_file:
            original_species = line.strip()
            eprint(original_species)
            try:
                data = retrieve(original_species)
            except ValueError as e:
                print(e)

            print('\t'.join([original_species, data['Order'], data['Family'], data['Genus'], data['Species'], data['Authority']]))


@click.command()
@click.argument('species_file',
                required = True,
                type=click.Path(exists=True)
)
def main(species_file):
    process_file(species_file)

if __name__ == '__main__':
    main()
    
