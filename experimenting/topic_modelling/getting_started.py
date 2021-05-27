# %%
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

# https://stackoverflow.com/questions/22081209/find-the-root-of-the-git-repository-where-the-file-lives#comment44778829_22081487
import sys, os, subprocess
repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
sys.path.insert(1, os.path.join(sys.path[0], repo_dir))
from helper.HolmesReader import HolmesReader

holmesReader = HolmesReader()
collections = holmesReader.get_collections(as_dataframe=True)




# %%

"""
stemming?
lemma
tokenize
    -> pos_tag -> NER
    -> "_".join()
todo: have a look at research internship presentation
"""

# todo clean text

vect = TfidfVectorizer(min_df=10, stop_words="english")
X = vect.fit_transform(collections['text'])

# Create an NMF instance: model
# the 5 components will be the topics
model = NMF(n_components=10, random_state=42, max_iter=1000)

# Fit the model to TF-IDF
model.fit(X)

# %%
from sklearn.feature_extraction.text import CountVectorizer
count_vectorizer = CountVectorizer(min_df=10, max_df=0.95, ngram_range=(1,1), stop_words='english')
feature_matrix = count_vectorizer.fit_transform(collections['text'])

import pyLDAvis.sklearn
panel = pyLDAvis.sklearn.prepare(model, X, feature_matrix, mds='tsne')
pyLDAvis.display(panel)

# %% 
# Transform the TF-IDF: nmf_features
nmf_features = model.transform(X)

# Create a DataFrame: components_df
components_df = pd.DataFrame(model.components_, columns=vect.get_feature_names())

for topic in range(components_df.shape[0]):
    tmp = components_df.iloc[topic]
    print(f'For topic {topic+1} the words with the highest value are:')
    print(tmp.nlargest(4))
    print('\n')
# %%
