import requests
from bs4 import BeautifulSoup
 
 
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
 
 
def hasil(kata_pencarian, jumlah_hasil, bahasa):
    assert isinstance(kata_pencarian, str), 'Kata pencarian harus String.'
    assert isinstance(jumlah_hasil, int), 'Jumlah hasil harus integer.'
    escaped_kata_pencarian = kata_pencarian.replace(' ', '+')
 
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_kata_pencarian, jumlah_hasil, bahasa)
    response = requests.get(google_url, headers = USER_AGENT)
    response.raise_for_status()
 
    return kata_pencarian, response.text

def parse_html(keyword, html):
    soup = BeautifulSoup(html, 'html.parser')

    doc = []
    rank = 1
    hasil_block = soup.find_all('div', attrs={'class': 'g'})
    for parser in hasil_block:

        link = parser.find('a', href=True)
        judul = parser.find('h3')
        deskripsi = parser.find('span', attrs={'class': 'st'})
        if link and judul:
            link = link['href']
            judul = judul.get_text()
            if deskripsi:
                deskripsi = deskripsi.get_text()
            if link != '#':
                doc.append({'keyword': keyword, 'rank': rank, 'judul': judul, 'deskripsi': deskripsi})
                rank += 1
        
    return doc
 
if __name__ == '__main__':
    keyword, html = hasil("web hosting adalah", 5, 'en')
    hasil = parse_html(keyword, html)
    print(hasil)
    