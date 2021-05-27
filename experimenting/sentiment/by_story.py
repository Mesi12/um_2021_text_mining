# %%

from nltk.tokenize import sent_tokenize
import numpy as np
import sys, os, subprocess
repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
sys.path.insert(1, os.path.join(sys.path[0], repo_dir))
from helper.HolmesReader import HolmesReader
from helper.CoreNLPHelper import CoreNLPHelper

holmesReader = HolmesReader()
collections = holmesReader.get_collections(as_dataframe=True)

coreNLPHelper = CoreNLPHelper("http://localhost:9000")


# %%
collections.head()
# %%

sentiments = []

# split into sentences + count
for index, row in collections.iterrows():
    sentences = sent_tokenize(row['text'])
    story_sentiments = []

    # get sentiment per sentences
    for sent in sentences:
        sentiment = coreNLPHelper.get_sentiment_value(sent)
        story_sentiments.append(sentiments)

    # calculate weighted mean for story
    weighted_sentiment = sum(story_sentiments)
    variance = np.var(story_sentiments)

    # save to list -> to dataframe
    sentiments.append((weighted_sentiment, variance))
    
    break

print(sentiments)
# %%
