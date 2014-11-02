
from bs4 import BeautifulSoup
from urllib2 import urlopen
import json as js
import os
import re
import nltk.data



# Make a soup object
def make_soup(url):
    html = urlopen(url)
    return BeautifulSoup(html, "lxml")

# Given a wikipedia URL, extract all the relevant text
def findText(url):
    currentURL = url
    soup = make_soup(currentURL)
    content = soup.body.find('div',{'id':'content'},recursive=False).find('div',{'id':'bodyContent'},recursive=False).find('div',{'id':'mw-content-text'},recursive=False)
    
    #Set recursive = False to access the direct children (not grandchildren, grand-grandChildren...)
    paragraphs = content.findAll('p',recursive = False)
    text = ''
    for p in paragraphs:
        text = text + p.get_text()
    return text
    
# Given a link determine if it is a valid capital city
def isCapital(link,countryName):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    soup = make_soup(link)
    content = soup.body.find('div', {'id':'content'}).find('div',{'id': 'bodyContent'}).find('div',{'id':'mw-content-text'})
    firstParagraph = content.findAll('p',recursive=False)[0].get_text()
   
    firstSentence = sent_detector.tokenize(firstParagraph.strip())[0]
    
    #The first sentence should contain either capital or city AND country name, if it is a legal article about a capital
    pattern1 = re.compile('[.]*\\bcapital\\b[.]*')
    pattern2 = re.compile('[.]*\\bcity\\b[.]*')
    pattern3 = re.compile('[.]*\\b%s\\b[.]*'%countryName)
    
    if ((re.search(pattern1,firstSentence) or re.search(pattern2,firstSentence)) and re.search(pattern3,firstSentence)):
        return True
    else:
        return False
    


# Extract table row information as a json file to be written into a textfile
def extractRowInfo(row, continent):
    rowInfo = row.findAll('td',recursive=False)
    #Country Info
    ROOT_URL = "http://en.wikipedia.org"
    countryName = rowInfo[1].a['title']
    countryLink = ROOT_URL + rowInfo[1].a['href']
    countryText = findText(countryLink)
   
    # Extract a capital city block and get all the valid capital names and texts (sometimes 
    #    one country may have multiple capitals
    capitalNames = []
    capitalText = []
    capitalBlock = rowInfo[2].findAll('a',recursive=False) #This is the list of all relevant links in the block
    #print capitalBlock
    if len(capitalBlock) > 1:
        for a in capitalBlock:
            link = ROOT_URL + a['href']
            if(isCapital(link,countryName)):
                capitalNames.append(a['title'])
                capitalText.append(findText(link))
    if len(capitalBlock) == 1:
        capitalNames.append(capitalBlock[0]['title'])
        capitalText.append(findText(ROOT_URL+capitalBlock[0]['href']))
        
    jsonList = []
    for n in capitalNames:
        capitalName = n
        text = capitalText[capitalNames.index(n)]
        Dict = {"country":countryName, "countryText":countryText,
               "capital":capitalName, "capitalText":text, "continent":continent}
        jsonList.append(js.dumps(Dict))
    return jsonList

# Write json object to a text file
def writeTextFile(json):
    jsonObj = js.loads(json)
    textFileName = jsonObj["country"] + "_" + jsonObj["capital"] + ".txt"
    f = open(textFileName, "w")
    f.write((jsonObj["continent"] + "\n").encode('utf8'))
    f.write((jsonObj["country"] + "\n").encode('utf8'))
    f.write((jsonObj["capital"] + "\n").encode('utf8'))
    f.write("\n")
    f.write((jsonObj["countryText"] + "\n").encode('utf8'))
    f.write("\n")
    f.write((jsonObj["capitalText"] + "\n").encode('utf8'))
    f.close()

# MainFunction
if __name__ == "__main__":
    os.chdir("C:/Users/Daniel/Desktop/Study/Fall2014/TextAnalytics/assignment5/textFile/")
    ROOT_URL = "http://en.wikipedia.org"
    listURL = ROOT_URL + "/wiki/List_of_countries_and_capitals_with_currency_and_language"
    soup = make_soup(listURL)
    
    content = soup.body.find("div", {"id":"content"},recursive=False).find("div",{"id":"bodyContent"},recursive=False).find("div",{"id":"mw-content-text"},recursive=False)
    continents = content.findAll("h2",recursive=False)[1:8]
    
    continent_names = []
    for i in range(7):
        continent_names.append(continents[i].find("span").string)
    
    tables = content.findAll("table", {"class":"wikitable sortable"},recursive=False)
    
    for t in tables:
        continentName = continent_names[tables.index(t)]
        rows = t.findAll('tr',recursive=False)
        #print continentName
        # Skipping the first row
        for i in range(1, len(rows)):
            #print i
            #print rows[i]
            curjson = extractRowInfo(rows[i], continentName)
            for j in curjson:
                writeTextFile(j)
            
    
