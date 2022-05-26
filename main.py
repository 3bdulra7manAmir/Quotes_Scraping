#NEW
import jovian as jovian
import requests
from bs4 import BeautifulSoup
base_url = "http://quotes.toscrape.com/"

def parse_quote_page(url):
    """ Used to parse the parse the webpage and return a beautiful soup object"""
    quote_url = url
    response = requests.get(quote_url)
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ' + quote_url)
    return BeautifulSoup(response.text)


#NEW
def get_top_quotes(doc):
    """ Used to extract all the top quotes in the given webpage"""
    quotes = doc.find_all('div', class_='quote')
    parsed_quotes = [parse_each_quotes(quote_html) for quote_html in quotes]
    return parsed_quotes

def parse_each_quotes(quote_html):
    """ Extract the specific information from each quote tag. """
    quote_tag = quote_html.find('span', class_='text')
    quote = quote_tag.get_text().strip('')
    author_tag = quote_html.find('small', class_='author')
    author = author_tag.get_text().strip()
    about_tag = quote_html.find_all('a')[0]
    about = base_url + about_tag['href']
    tags = quote_html.find_all('a')
    tag = ''
    for i in range(1, len(tags)):
        tag += tags[i].get_text() + " "

    tag = tag.strip()
    return {"quote": quote, "author": author, "about": about, "related_tags": tag}

#NEW
def write_csv(items, path):
    """ Write the extracted dictionary to a csv file"""
    with open('quotes-scraped.csv', 'a+') as f:
        if len(items) == 0:
            return
        headers = list(items[0].keys())
        for item in items:
            values = []
            for header in headers:
                values.append(str(item.get(header, "")))
            f.write(','.join(values) + "\n")

#NEW
def scrape_by_url(url, path):
    """ Helper function to scrape all the quotes by URL."""

    quote_doc = parse_quote_page(url)
    top_quotes = get_top_quotes(quote_doc)
    write_csv(top_quotes, path)
    return quote_doc


def scrape_quotes(tag, path=None):
    """Scrape quotes by tag and write them to csv file."""
    if path is None:
        path = tag + '.csv'
    url = base_url + "tag/" + tag
    first_doc = scrape_by_url(url, path)
    next_pages = first_doc.find_all('li', class_="next")
    while True:
        if next_pages:
            # so if there are more pages to scrape from the website, navigate to next page.
            url = base_url + next_pages[0].a['href']
            next_doc = scrape_by_url(url, path)
            next_pages = next_doc.find_all('li', class_="next")
        else:
            break
    print('Top quotes for tag "{}" written to file quotes.csv'.format(tag))
    return 'quotes-scraped.csv'


with open('quotes-scraped.csv', 'a+') as f:
    f.write('quote,author,about,related_tags' + '\n')

#NEW
scrape_quotes('love')
scrape_quotes('inspirational')
scrape_quotes('life')
scrape_quotes('humor')
scrape_quotes('friendship')
scrape_quotes('books')
scrape_quotes('reading')
scrape_quotes('friends')
scrape_quotes('truth')
scrape_quotes('choices')
scrape_quotes('thinking')
scrape_quotes('romance')
scrape_quotes('classic')
scrape_quotes('library')
scrape_quotes('writing')
scrape_quotes('children')
scrape_quotes('religion')
scrape_quotes('faith')


#NEW
with open('quotes-scraped.csv', 'r') as f:
    for i in range(5):
        print(f.readline())


#NEW
jovian.commit(files=['quotes-scraped.csv'])