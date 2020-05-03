import pandas as pd

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

url = 'https://www.bbc.com/portuguese/internacional-51718755'

try:
    html = urlopen(url)
except HTTPError as e:
    print(e)
except URLError:
    print("The serve could not be found!")
else:
    # print("Consegui acessar a URL")
    bs = BeautifulSoup(html, 'lxml')

    country_name = []
    death_per_country = []
    cases_per_country = []

    get_common_div_for_world = bs.select(
        'div div div.main-container div.input-summary-presentation-container div:nth-child(2) div')

    cases_of_infected_in_the_world = get_common_div_for_world[1].find('span').text
    death_cases_in_the_world = get_common_div_for_world[2].find('span').text
    recovered_data_in_the_world = get_common_div_for_world[3].find('span').text

    get_country_data = bs.select(
        '.core__row')

    for i in get_country_data:
        country_name.append(i.find('td').text.strip())
        death_per_country.append(i.find('td', class_='c__c c__c--d').text.strip())
        cases_per_country.append(i.find('td', class_='c__c c__c--t').text.strip())

    dc = pd.DataFrame({
        "Country Name": country_name,
        "Death on Country": death_per_country,
        "Confirmed Cases on Country": cases_per_country
    })
    dict_ = dc.to_dict()

    print("\nNumber of confirmed cases in world: %s.\n" % cases_of_infected_in_the_world)
    print("Number of deaths in the world: %s\n" % death_cases_in_the_world)
    print("Number of recovered in the world: %s\n" % recovered_data_in_the_world)

    resp = input("\n\t\t\t I WOULD LIKE TO KNOW INFORMATION ABOUT A SPECIFIC COUNTRY ? \n\n Yes/No ? ")

    if resp == 'Yes':
        specified_country = input("\nWhich country ? ")
        while specified_country not in dict_['Country Name'].values():
            print("Country not found, try find other country!")
            specified_country = input("\nWhich country ? ")

        idx = list(dict_['Country Name'].values()).index(specified_country)
        specific_country_death_information = dict_['Death on Country'][idx]
        specific_country_confirmed_cases_information = dict_['Confirmed Cases on Country'][idx]

        print("\nIn %s we have \n%s - deaths \n%s - confirmed cases!!!" % (
            specified_country, specific_country_death_information, specific_country_confirmed_cases_information))
    elif resp == 'No':
        print("Ok. Thanks !!!")
    else:
        print("%s is not valid response.\nAllowed responses are 'Yes' or 'No'. Run the script again and select only allowed responses" % resp)
