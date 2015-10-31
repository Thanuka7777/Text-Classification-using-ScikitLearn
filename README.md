In this python file, I demonstrated using BeautifulSoup to scrap texts from Wikipedia website. 

The base URL is :https://en.wikipedia.org/wiki/List_of_countries_and_capitals_with_currency_and_language

The workflow process is as follows:

    1. Create a soup object using URL of the website;
    2. Find the right tag by inspecting element of the webpage.
    3. Use findAll() function to traserve down to the tag level
    4. Get texts, titles, etc by specifying specific tags, such as 'table'
