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

    # Return question data
    return (type, target)


def questionModel(question):
    # get type n target from question
    (type, target) = processquestion(preprocess(question))

    # Read document train
    with open("train.txt", "r") as f:
        doc = f.read()

    # Get sentence keywords
    searchwords = set(target)

    # list match
    relevant = word_count(target, doc, searchwords).most_common(3)  # list matched
    # print(relevant)

    return answerModel(type, relevant)


def answerModel(type, relevant):
    sentences = []
    for idx, word in enumerate(relevant):
        sentences.append(word[0])

    listwords = []
    for sentence in sentences:
        doc = nlp(sentence)
        listwords.append([(X, X.ent_type_) for X in doc])

    countList = []
    for i, text in enumerate(listwords):
        count = 0
        for word in text:
            if word[1] == type:
                count += 1

        countList.append(count)

    winner = countList.index(max(countList))
    winner = sentence[winner]
    print(sentences[winner])

    return sentence


if __name__ == "__main__":
    # =============================================================================
    #    User input
    # =============================================================================
    print("Masukkan pertanyaan : ")
    question = str(input())

    # =============================================================================
    #     Answer Processing
    # =============================================================================
    questionModel(question)

    # =============================================================================
    #     Evaluasi
    # =============================================================================
