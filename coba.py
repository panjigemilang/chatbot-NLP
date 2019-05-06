# import en_core_web_sm

# # from spacy import displacy
# # from collections import Counter

# nlp = en_core_web_sm.load()

# doc = nlp("Who is Raden Ajeng Kartini in America 09:00 AM Wednesday?")
# coba = [(X, X.pos_, X.ent_iob_, X.ent_type_) for X in doc]
# for tag in coba:
#     print((tag))

import nltk
from nltk.chunk import tree2conllstr, tree2conlltags
import re

# import time

exampleArray = ["The incredibly intimidating NLP scares people away who are sissies."]


contentArray = [
    "Indonesia is a beautiful country with many cultures in and at 09:00 PM you could stay until Wednesday till Friday",
    "i'm lying about how good i'am hehe",
]


##let the fun begin!##
def processLanguage():
    try:
        for item in contentArray:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            # print(tagged)

            namedEnt = tree2conlltags(nltk.ne_chunk(tagged))
            print(namedEnt)

            # time.sleep(1)

    except (Exception, e):
        print(str(e))


processLanguage()
