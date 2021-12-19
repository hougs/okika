import requests
import json
from bs4 import BeautifulSoup

ROOT_URL = "http://www.botany.hawaii.edu/faculty/carr/"

page = requests.get(ROOT_URL + "alpha_cronq_judd_apgii.htm")

soup = BeautifulSoup(page.content, "html.parser")
# Non Flowing Plant Families (cycads, conifers, ferns, and fern allies)

# Flowering Plant Families (magnolias, lilies, etc.)
# TODO: Which system for angiospersm? Is it relevant? Going with Angiosperm Phylogeny Group
# Actually, maybe not important. Ignore groupings and just grab data by family name.

plant_families = soup.find_all('p', class_='MsoNormal')
family_name_and_ref = []
for tag in plant_families:
    for a_tags in tag.find_all('a'):
        family_name_and_ref.append((tag.text.strip(), a_tags['href']))


def find_family_description(in_soup):
    desc = in_soup.find('p').text
    if "Each \"thumbnail\" image below is linked to a larger photograph." in desc:
        desc = ""
    return desc

family_info = []
species_info = []

for family, link in family_name_and_ref:
    family_page = requests.get(ROOT_URL + link)
    family_soup = BeautifulSoup(family_page.content, "html.parser")
    family_description = find_family_description(family_soup)
    family_info.append({'family': family, 'family_desc': family_description})
    print(ROOT_URL + link)
    for row in family_soup.find_all('tr'):
        for col in row.find_all('td', recursive=False):
            species_name = ""
            species_desc = ""
            if 'align' in col.attrs:
                species_photo_links = [link.get('href') for link in col.find_all('a')]
            else:
                species_name = ''
                for itals in col.find_all('i'):
                    species_name = itals.text
                species_desc = col.text
        species_info.append({'family': family,
                             'species': species_name,
                             'photo_links': species_photo_links,
                             'species_desc': species_desc})

print(family_info[0])
print(species_info[0])
with open('resources/uh-botany-families.json', 'w+') as fout:
    json.dump(family_info , fout)

with open('resources/uh-botany-species.json', 'w+') as fout:
    json.dump(species_info , fout)
