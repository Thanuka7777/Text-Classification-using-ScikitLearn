__author__ = 'Daniel'

from bs4 import BeautifulSoup
from urllib import request
from urllib.error import URLError
import re
import os
from urllib.parse import quote #deal with unicode in URL


#Make a soup from a specific URL
def make_soup(URL):
    try:
        html = request.urlopen(URL)
        return BeautifulSoup(html,"html.parser")
    except URLError:
        return None


#   Target the right section without traversing through a long path...
#   Given a soup objects containing continent info
#   Returns a list of continent names
def getContinents(URL):
    soup = make_soup(URL)
    nameList = soup.findAll('span',{'class':'mw-headline'})
    headlines = [n.get_text() for n in nameList]
    return headlines[:7] #the first seven entries are continent names


#Strip any non-alphabetic characters from the string
def stripNonAlphabetic(s):
    pattern = re.compile(r'[\[\]0-9\n ]')
    return pattern.sub('',s)


#  Given an URL of continent wiki page
#  Return a list of capitals
def getCapitals(continentURL):
    soup = make_soup(continentURL)
    capitalList = []
    if soup:
        body = soup.find('body')
        tables = body.findAll('table')

        for t in tables:
            headTexts = [stripNonAlphabetic(str.lower(h.get_text())) for h in t.findAll('th')]
            #find the table containing capital information
            if 'capital' in headTexts:
                capitalIndex = headTexts.index('capital')
                rows = t.findAll('tr')

                for r in rows:
                    fields = r.findAll('td')
                    try:
                        capitalName = fields[capitalIndex].findAll('a')[0].get_text()
                        capitalList.append(stripNonAlphabetic(capitalName))
                    except IndexError:
                        capitalList.append(None)

    return capitalList


#   Given a capital name
#   Return text string
def getText(capitalURL):
    soup = make_soup(capitalURL)

    if soup:
        paragraphs = soup.findAll('p')
        capital_text = ''.join([p.get_text() for p in paragraphs])
        return capital_text
    else:
        return ''

#   Given text string and Capital name
#   Write text to a file
def writeText(text,name,continent):
    with open('txt/%s/%s.txt'%(continent,name), 'w') as f:
        f.write(text)

def main():
    #ROOT_URL for extracting capital and Continent texts
    ROOT_URL = 'https://en.wikipedia.org/wiki/%s'

    #URL to extract continents
    BASE_URL = 'https://en.wikipedia.org/wiki/List_of_countries_and_capitals_with_currency_and_language'

    #RootURL to extract capitals from continent
    capital_LIST_URL = 'https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_%s'

    continents = getContinents(BASE_URL)

    for continent in continents[:]:
        continent = continent.replace(' ','_') #Replace space in the continent name
        os.system('mkdir txt/%s'%continent) #create a subfolder containing continent info
        #print('continent is %s'%continent)
        cont_URL = ROOT_URL%continent
        #print(cont_URL)

        #Write continent texts
        cont_text = getText(cont_URL)
        writeText(cont_text, continent, continent)

        #Get list of capitals
        capitals = getCapitals(capital_LIST_URL%continent)


        for capital in capitals:
            if capital:
                print(capital)
                cap_text = getText(ROOT_URL%quote(capital))
                writeText(cap_text,capital,continent)

if __name__ == '__main__':
    main()





