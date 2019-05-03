import requests
from bs4 import BeautifulSoup
 
 
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
 
 
def hasil(search_term, number_hasils, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_hasils, int), 'Number of hasils must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
 
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_hasils, language_code)
    response = requests.get(google_url, headers = USER_AGENT)
    response.raise_for_status()
 
    return search_term, response.text

def parse_html(keyword, html):
    soup = BeautifulSoup(html, 'html.parser')

    doc = []
    rank = 1
    hasil_block = soup.find_all('div', attrs={'class': 'g'})
    for parser in hasil_block:

        link = parser.find('a', href=True)
        title = parser.find('h3')
        description = parser.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                doc.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description})
                rank += 1
        
    return doc
 
if __name__ == '__main__':
    keyword, html = hasil("web hosting adalah", 5, 'en')
    hasil = parse_html(keyword, html)
    print(hasil)
    