import sys
import requests
from pyquery import PyQuery as pq
import html as html_goodies
import click
import csv

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
                print('\t'.join([original_species, data['Order'], data['Family'], data['Genus'], data['Species'], data['Authority']]))
            except ValueError as e:
                print(e)

def process_csv_file(csv_file_name, column):
    with open(csv_file_name, encoding="utf-8") as input_file:
        with open('algae_base_not_found.txt', 'w') as not_found:
            data = csv.DictReader(input_file, dialect="excel")
            for row in data:
                original_species = row[column]
                try:
                    data = retrieve(original_species)
                    print('\t'.join([original_species, data['Order'], data['Family'], data['Genus'], data['Species'], data['Authority']]))
                except ValueError as e:
                    print(e, file=not_found)

@click.command()
@click.argument('species_file',
                required = True,
                type=click.Path(exists=True)
)
@click.option(
    '--csv', 'csv_column',
    required = False,
    help="If using a csv file as input, set the Species column."
)
def main(species_file, csv_column):
    if csv_column:
        process_csv_file(species_file, csv_column)
    else:
        process_file(species_file)

if __name__ == '__main__':
    main()
    
