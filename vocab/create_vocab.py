# %%
import os
import json
import string
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer


corpora = []
for file_name in os.listdir("output"):
    filepath = os.path.join("output", file_name)

    if os.path.isfile(filepath) and filepath.endswith(".json"):

        with open(filepath, "r") as f:
            annots = json.load(f)
            corpus = []
            for sentence in annots['sentences']:
                for token in sentence['tokens']:
                    if token['lemma'] not in string.punctuation:
                        corpus.append(token['lemma'].lower())
            corpora.append((file_name, corpus))

# %%
total_words = sum([len(c) for c in corpora])

# calc tf-idf without stopwords
def identity_tokenizer(text):
    return text

for name, corpus in corpora:
    print(name)
    vectorizer = TfidfVectorizer(tokenizer=identity_tokenizer, stop_words='english', lowercase=False)    
    X = vectorizer.fit_transform([corpus])
    
    break


# %%
# all at once
vectorizer = TfidfVectorizer(tokenizer=identity_tokenizer, stop_words='english', lowercase=False)    
X = vectorizer.fit_transform([text for name,text in corpora])


# %%
import numpy as np
feature_array = np.array(vectorizer.get_feature_names())
tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]

n = 10
print(feature_array[tfidf_sorting][:n])
# %%
