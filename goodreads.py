
import re
import urllib
from bs4 import BeautifulSoup

def clean_quote(quote):  # To remove stray html tags from the retrieved results
    quote = re.sub('<.*?>', '', quote)
    quote = '“' + quote + '”'
    return quote

print()
quote_tag = "motivational"
query_url = 'https://www.goodreads.com/quotes/tag/' + quote_tag
all_quotes = ''
print()
print("Retrieving all quotes tagged as \"%s\"..." % quote_tag)
print()

#pages = input()

for page in range(101):
    paged_query_url = query_url + '?page=' + str(page)
    print(paged_query_url)
    try:
        query = urllib.request.urlopen(paged_query_url)
        html = query.read()
        soup = BeautifulSoup(html, "lxml")
        quotes = soup.findAll("div", class_="quoteText")
        if (len(quotes) == 0):
            break

        for item in quotes:
            tex = str(item)
            quote = re.findall('“(.*)”', tex)
            #ref = re.findall('"authorOrTitle">(.*)</span>', tex)
            all_quotes = all_quotes + clean_quote(quote[0]) + '\n'

    except urllib.error.HTTPError as err:
        print("Request error: ", err.reason)
        break
    except urllib.error.URLError as err:
        print("Some other error happend:", err.reason)
        break

with open('quotes_' + quote_tag + '.txt', 'w') as fp:
    fp.write(all_quotes)