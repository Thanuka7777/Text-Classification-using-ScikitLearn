Classify country capitals based on their wikipedia descriptions. The labels are continents.

**Step 1**: Scrape Capital Texts from Wikipedia Pages

Starting from Base URL https://en.wikipedia.org/wiki/List_of_countries_and_capitals_with_currency_and_language, the scraper traverses through a list of hyperlinks to extract descriptions of country capitals from Wikipedia

The workflow process is as follows:

    1. Create a soup object using URL of the website;
    2. Find the right tag by inspecting element of the webpage.
    3. Use findAll() function to traserve down to the tag level
    4. Get texts, titles, etc by specifying specific tags, such as 'table'
    
**Step 2**: Using ScikitLearn and NLTK packages to build algorithms to classify country capitals. Three python files:

    1. capitalCorpus.py: main text corpus class containing texts and labels
    2. textTransformer.py: a transfomer class used to transform raw texts (removing stopwords, stemming, etc)
    3. Classify.py: classification script
