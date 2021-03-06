import requests, nltk, string, en_core_web_sm, spacy, collections, itertools
from nltk.chunk import conlltags2tree, tree2conlltags, ne_chunk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from bs4 import BeautifulSoup


USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}

nlp = spacy.load("en_core_web_sm")

# Hardcoded word lists
yesnowords = [
    "can",
    "could",
    "would",
    "is",
    "does",
    "has",
    "was",
    "were",
    "had",
    "have",
    "did",
    "are",
    "will",
]
commonwords = ["the", "a", "an", "is", "are", "were", "."]
questionwords = ["who", "what", "where", "when", "why", "how", "whose", "which", "whom"]


def setToList(arr):
    list = []
    for item in arr:
        list.append(int(item.tolist()))

    return list


def preprocess(sent):
    sent = sent.translate(str.maketrans("", "", string.punctuation))

    stop_words = stopwords.words("english")
    sent = nltk.word_tokenize(sent)
    sent = [word for word in sent if word not in stop_words]
    #    sent = nltk.pos_tag(sent)

    return sent


def word_count(words, doc, searchwords):
    counts = collections.Counter()
    #     words = words.split()
    sentence = nltk.sent_tokenize(doc)
    for (i, sent) in enumerate(sentence):
        sentwords = nltk.word_tokenize(sent)
        wordmatches = set(filter(set(searchwords).__contains__, sentwords))
        counts[sent] = len(wordmatches)

    return counts


# Take in a tokenized question and return the question type and body
def processquestion(qwords):

    # Find "question word" (what, who, where, etc.)
    questionword = ""
    qidx = -1

    #     qwords = preprocess(qwords)

    for (idx, word) in enumerate(qwords):
        if word.lower() in questionwords:
            questionword = word.lower()
            qidx = idx
            break
        elif word.lower() in yesnowords:
            return ("YESNO", qwords)

    if qidx < 0:
        return ("MISC", qwords)

    if qidx > len(qwords) - 3:
        target = qwords[:qidx]
    else:
        target = qwords[qidx + 1 :]
    type = "MISC"

    # Determine question type
    if questionword in ["who", "whose", "whom"]:
        type = "PERSON"
    elif questionword == "where":
        type = "PLACE"
    elif questionword == "when":
        type = "TIME"
    elif questionword == "how":
        if target[0] in ["few", "little", "much", "many"]:
            type = "QUANTITY"
            target = target[1:]
        elif target[0] in ["young", "old", "long"]:
            type = "TIME"
            target = target[1:]

    # Trim possible extra helper verb
    if questionword == "which":
        target = target[1:]
    if target[0] in yesnowords:
        target = target[1:]

    # Return question data
    return (type, target)


def questionModel(question):
    #    Removing stopword & punctuation
    # tokenized = preprocess(question)
    (type, target) = processquestion(preprocess(question))

    # Read doc
    with open("train.txt", "r") as f:
        doc = f.read()

    # Get sentence keywords
    searchwords = set(target)

    # Word Count
    relevant = word_count(target, doc, searchwords).most_common(3)  # list matched
    print(relevant)

    #    NER
    # doc = nlp(question)
    # namedEntity = [(X, X.ent_iob_, X.ent_type_) for X in doc]

    # Pos-Tag
    # NER_type = ["person", "gpe", "org", "date", "time"]
    # NER_data = []

    # Q-type
    # NER_data.append(str(namedEntity[0][0]).lower())

    # nertype = [word[2] for word in namedEntity if word[2].lower() in NER_type]
    # NER_data.append(nertype)

    return answerModel(type, relevant)
    # return type, relevant


def answerModel(type, relevant):

    # ans = [('Raden Ajeng Kartini was a leading feminist of women emancipation in Indonesia.', 3), ('Raden Kartini was born on 21 April 1879 in Jepara.', 2), ('Ibu Kartini was very concerned because of education in Indonesia especially for women.', 1)]

    # NER for ans
    sentences = []
    for idx, word in enumerate(relevant):
        # print(word[0])
        sentences.append(word[0])

    listwords = []
    for sentence in sentences:
        doc = nlp(sentence)
        listwords.append([(X, X.ent_type_) for X in doc])

    # listwords = list(itertools.chain.from_iterable(listwords))
    # print(listwords)
    countList = []
    for i, text in enumerate(listwords):
        count = 0
        for word in text:
            if word[1] == type:
                count += 1

        countList.append(count)

    winner = countList.index(max(countList))

    print(sentences[winner])
    # for sentence in sentences:
    #     print(len(sentence))
    # print(listwords)

    # counting NER in listwords

    # namedEntity = [(X, X.ent_iob_, X.ent_type_) for X in doc]
    # print(namedEntity)


if __name__ == "__main__":
    # =============================================================================
    #    User input
    # =============================================================================
    #    kata_pencarian = str(input())
    question = "When was Raden Ajeng Kartini born?"

    """
    5 W + 1 H
    What/WP When/WRB Where/WRB Who/WP Why/WRB
    How/WRB
    """

    # =============================================================================
    #     preprocessing
    # =============================================================================
    questionModel(question)

    # print("ini qm : ", qm)
    # print("ini question processed : ", candidateAns)

    # =============================================================================
    #     answer sementara
    # =============================================================================
    a1 = [
        "Raden Ajeng Kartini was a prominent Indonesian national heroine from Java.",
        "Friday, 12 July 1998",
    ]

    # answerModel(qm, candidateAns)

    jumlah_pencarian = 5
    bahasa = "en"

    # print("Question : ", question)
    # keyword, html = scraping(q, jumlah_pencarian, bahasa)
    # print("html ", html)
    # hasil = parse_html(keyword, html)
    # print(hasil)

    # print(hasil[0])
