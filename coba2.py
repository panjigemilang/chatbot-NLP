import en_core_web_sm, spacy

nlp = spacy.load("en_core_web_sm")

doc = nlp("$27 April 2018 Wednesday")
print([(X, X.ent_type_) for X in doc])
