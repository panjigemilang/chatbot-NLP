import requests, nltk, string
from nltk.chunk import conlltags2tree, tree2conlltags, ne_chunk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from bs4 import BeautifulSoup
 
 
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
 
 
def hasil(kata_pencarian, jumlah_pencarian, bahasa):
    assert isinstance(kata_pencarian, str), 'Kata pencarian harus String.'
    assert isinstance(jumlah_pencarian, int), 'Jumlah hasil harus integer.'
    escaped_kata_pencarian = kata_pencarian.replace(' ', '+')
 
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_kata_pencarian, jumlah_pencarian, bahasa)
    
    response = requests.get(google_url, headers = USER_AGENT)
#    response.raise_for_status()
#    print("ini apaan? : ", response.raise_for_status())
 
    return kata_pencarian, response.text

def parse_html(keyword, html):
    soup = BeautifulSoup(html, 'html.parser')

    doc = []
    rank = 1
    hasil_block = soup.find_all('div', attrs = {'class': 'g'})
    
    for parser in hasil_block:
        link = parser.find('a', href=True)
        judul = parser.find('h3')
        deskripsi = parser.find('span', attrs = {'class': 'st'})
        if link and judul:
            link = link['href']
            judul = judul.get_text()
            if deskripsi:
                deskripsi = deskripsi.get_text()
            if link != '#':
                doc.append({'keyword': keyword, 'rank': rank, 'judul': judul, 'deskripsi': deskripsi})
                rank += 1
        
    return doc
 
def preprocess(sent):
    sent = sent.translate(str.maketrans('', '', string.punctuation))
    
    stop_words = stopwords.words('english')
    sent = nltk.word_tokenize(sent)
    sent = [word for word in sent if word not in stop_words]
#    sent = nltk.pos_tag(sent)
    
    return sent    

def questionModel(question):
#    Removing stopword & punctuation
    tokenized = preprocess(question)
    
#    Chunking
    ne_tree = ne_chunk(pos_tag(word_tokenize(question)))
    NER_tagged = tree2conlltags(ne_tree)
    NER_data = []
    for tag in NER_tagged:
        if (tag[1] == 'WP' or tag[1] == 'WRB'):
            NER_data.append(tag[1])
        
        if (tag[2].lower() == 'b-person' or tag[2].lower() == 'i-person'):
            NER_data.append(tag[2].lower())
    
    print("ini Ner : ", NER_data)
    return NER_data, tokenized
    
def answerModel(qm):
    #    sent = preprocess(kata_pencarian)
        pattern = "NP: {<DT>?<JJ>*<NN>}"
    #    cp = nltk.RegexpParser(pattern)
    #    cs = cp.parse(sent)
    #    print("ini cs : ", cs)

if __name__ == '__main__':
# =============================================================================
#    User input
# =============================================================================
#    kata_pencarian = str(input())
    question = "Who is Raden Ajeng Kartini?"
    
    '''
    5 W + 1 H
    What/WP When/WRB Where/WRB Who/WP Why/WRB
    How/WRB
    '''
    
# =============================================================================
#     preprocessing
# =============================================================================
    qm, q_processed = questionModel(question)
#    print(q_processed)
    
#    answear = answerModel(qm)
    
        
# =============================================================================
#     google scrapping
# =============================================================================
    jumlah_pencarian = 5
    bahasa = "en"
    
#    keyword, html = hasil(kata_pencarian, jumlah_pencarian, bahasa)
#    hasil = parse_html(keyword, html)
#    print(hasil[0]['deskripsi'])
    