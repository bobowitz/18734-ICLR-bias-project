# get_country_from_authorid_domains.py
#
# Guesses the country of each email domain and adds a new field 'authorid_domain_countries' to each json
# containing country codes

import json
import os
import tqdm


# edo and deu were typos of edu in the data
us_codes = ['COM', 'EDU', 'GOV', 'ORG', 'EDO',
            'DEU', 'NET', 'MIL', 'CODELFM', 'GLOBAL', 'IO']
# these I looked up per domain
canada_codes = ['QUEBEC']
germany_codes = ['SAARLAND', 'SCIENCE']
france_codes = ['NAME']
spain_codes = ['CAT']


def add_country_to_json(fname):
    data = []
    countries = set()
    with open(fname, 'r') as f:
        data = json.load(f)

        for email in data['authorids']:
            domain = email[email.find('@') + 1:]
            country_code = domain.split('.')[-1].upper()
            if country_code in us_codes:
                countries.add('US')
            elif country_code in canada_codes:
                countries.add('CA')
            elif country_code in germany_codes:
                countries.add('DE')
            elif country_code in france_codes:
                countries.add('FR')
            elif country_code in spain_codes:
                countries.add('ES')
            else:
                countries.add(country_code)

    data['authorid_domain_countries'] = list(countries)

    with open(fname, 'w') as f:
        json.dump(data, f, indent=2)


print('finding countries for accepted papers:')
for fname in tqdm.tqdm(os.listdir('Data/2020/Accept/')):
    add_country_to_json('Data/2020/Accept/' + fname)
print('finding countries for rejected papers:')
for fname in tqdm.tqdm(os.listdir('Data/2020/Reject/')):
    add_country_to_json('Data/2020/Reject/' + fname)
