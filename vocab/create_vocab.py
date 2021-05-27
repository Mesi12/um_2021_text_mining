# %%
import os
import json
import string

import sys, os, subprocess
repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
sys.path.insert(1, os.path.join(sys.path[0], repo_dir))
from helper.HolmesReader import HolmesReader


def get_corpus(title):
    """
    Returns all lemma (non distinct) for a story/novel title
    """
    filepath = os.path.join(FOLDER_LEMMA, f"{title}.txt.json")

    with open(filepath, "r") as f:
        annots = json.load(f)
        corpus = []
        for sentence in annots['sentences']:
            for token in sentence['tokens']:
                if token['lemma'] not in string.punctuation:
                    # e.g. lemma extracts quotes as individual tokens
                    corpus.append(token['lemma'].lower())
    
    return corpus


if __name__ == "__main__":
    FOLDER_LEMMA = "output"
    holmesReader = HolmesReader()
    df_meta = holmesReader.get_metadata(True)
    df_meta.sort_values(by="publish_date", ascending=True, inplace=True)
    corpus_total = set()
    metric_cols = []
    metric_cols_names = ["title","words", "vocab", "cum. vocab"]

    for title in df_meta['i_title']:
        # get lemma for title
        corpus = get_corpus(title)
        corpus_total.update(corpus)
        
        # metrics: count size && add to full_corpus & count size
        metrics = [
            title,
            len(corpus),
            len(set(corpus)),
            len(corpus_total)
        ]
        metric_cols.append(metrics)

    # add to list for dataframe later
    df_meta[metric_cols_names] = metric_cols

    df_meta.to_csv("output_vocab.csv", index=False)
    

# %%
import seaborn as sns

#sns.lineplot(data=df_meta, x="publish_date", y="cum. vocab")
sns.barplot(data=df_meta, x="publish_date", y="vocab")
    

# do tf-idf for a novel only

# %%

from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

# gather all story and novel text
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
            corpora.append((file_name.replace(".txt.json", ""), corpus))

# %%
total_words = sum([len(c) for c in corpora])
vocab_output = []
vocab_output_cols = "type,title,date,"

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
print(feature_array[tfidf_sorting][-n:])
# %%
