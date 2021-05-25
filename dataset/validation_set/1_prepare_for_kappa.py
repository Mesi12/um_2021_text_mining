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
    sentences = [sent for sent in sentences if len(nltk.tokenize.word_tokenize(sent)) >= 10]
    print(f"{len(sentences)} - sentences after deleting sentences < 9 words incl. punctuation")
    sentences = [sent for sent in sentences if len([word for word in nltk.tokenize.word_tokenize(sent) if not word in string.punctuation]) >= 10]
    print(f"{len(sentences)} - sentences after deleting sentences < 9 words ignoring punctuation")

    print("shuffle...")
    random.shuffle(sentences)
    chosen_sentences = sentences[:50]

    with open("tmp.txt", "w") as fp:
        fp.write("\n".join(chosen_sentences))

    # export sentences for tagtog
    print("export...")
    os.makedirs(EXPORT_PATH, exist_ok=True)
    for i, sentence in enumerate(chosen_sentences):
        sentence = sentence.strip('""')
        with open(os.path.join(EXPORT_PATH, f"doc_{i+1:02.0f}.txt"), "w") as fp:
            fp.write(sentence)

# %%
