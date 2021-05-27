#%%
import pandas as pd
import os
import random
import re
import nltk
import string

def collect_stories_by_collection(collections):
    """
    Returns text from all stories of given collections.
    """
    stories = []

    for collection in collections:

        FOLDER_PATH = os.path.join("..", "processed", "stories", collection)
        for f in os.listdir(FOLDER_PATH):
            filepath = os.path.join(FOLDER_PATH,f)
            if os.path.isfile(filepath) and f.endswith(".txt"):

                with open(filepath, "r") as fp:
                    stories.append(fp.read())
    
    return stories



if __name__ == "__main__":

    DEBUG_MODE = True

    # copyright footer: https://sherlock-holm.es/ascii/
    copyright_safe_collections = [
        '1_the_adventures_of_sherlock_holmes',
        '2_the_memoirs_of_sherlock_holmes',
        '3_the_return_of_sherlock_holmes',
        '4_his_last_bow']
    EXPORT_PATH = "tagtog_docs"
    
    # prepare random selection of sentences
    print("collect sentences...")
    stories = collect_stories_by_collection(copyright_safe_collections)
    full_text = "\n".join(stories).replace("\n", "")
    print("tokenize...")
    sentences = nltk.tokenize.sent_tokenize(full_text)
    print("filter...")
    
    print(f"{len(sentences)} - sentences total")
    sentences = [sent for sent in sentences if len([word for word in nltk.tokenize.word_tokenize(sent) if not word in string.punctuation]) >= 20]
    print(f"{len(sentences)} - sentences after deleting sentences < 9 words ignoring punctuation")

#%%
    print("shuffle...")
    random.shuffle(sentences)
    chosen_sentences = sentences[:100]

    with open("tmp.txt", "w") as fp:
        fp.write("\n".join(chosen_sentences))

    # export sentences for tagtog
    if DEBUG_MODE:
        print("no export .. DEBUG mode")
    else:
        print("export...")
        os.makedirs(EXPORT_PATH, exist_ok=True)
        for i, sentence in enumerate(chosen_sentences):
            sentence = sentence.strip('""')
            with open(os.path.join(EXPORT_PATH, f"doc_{i+1:03.0f}.txt"), "w") as fp:
                fp.write(sentence)


    


# %%
# following code can be used to increase the chance of adding PERSON and LOCATION
# to the validation set.
"""
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos,lemma,ner -status_port 9000 -port 9000 -timeout 15000 -quiet
"""
import numpy as np
from nltk.parse import CoreNLPParser
server_url = 'http://localhost:9000'
# Lexical Parser
parser = CoreNLPParser(url=server_url)
# NER Tagger
ner_tagger = CoreNLPParser(url=server_url, tagtype='ner')

try:
    sent_character
    sent_location
except NameError:
    sent_character = set()
    sent_location = set()

num_PERSON = []
num_LOCATION = []
for i, sentence in enumerate(chosen_sentences):
    sentence = sentence.strip('""')
    tokens = list(parser.tokenize(sentence))
    ner_tags = list(ner_tagger.tag(tokens))

    tag_person = [tag for token,tag in ner_tags if tag == "PERSON"]
    tag_location = [tag for token,tag in ner_tags if tag == "LOCATION"]

    num_PERSON.append(len(tag_person))
    num_LOCATION.append(len(tag_location))

    if tag_person:
        sent_character.add(sentence)
    
    if tag_location:
        sent_location.add(sentence)

num_PERSON = [i for i in num_PERSON if i != 0]
num_LOCATION = [i for i in num_LOCATION if i != 0]

print(f"person: {len(num_PERSON)}, {np.mean(num_PERSON)}")
print(f"location: {len(num_LOCATION)}, {np.mean(num_LOCATION)}")

print(len(sent_character))
print(len(sent_location))


# %%
# special select of 100 sentences with high number of person and location NERs
# all locations (due to minority)
export_sentences = sent_location.copy()
print(len(export_sentences))

# fill up until 80 with characters
character_list = list(sent_character.copy())
while len(export_sentences) < 80:
    print(len(export_sentences))
    export_sentences.add(character_list.pop())

# fill up remaining 20 with totally random sentences
random.shuffle(sentences)
while len(export_sentences) < 100:
    print(len(export_sentences))
    export_sentences.add(sentences.pop())

print(len(export_sentences))
# %%

# export them
with open("tmp.txt", "w") as fp:
    fp.write("\n".join(export_sentences))
# %%
# export sentences for tagtog
print("export...")
os.makedirs(EXPORT_PATH, exist_ok=True)
for i, sentence in enumerate(export_sentences):
    sentence = sentence.strip('""')
    with open(os.path.join(EXPORT_PATH, f"doc_{i+1:03.0f}.txt"), "w") as fp:
        fp.write(sentence)
