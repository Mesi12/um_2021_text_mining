#%%
import os
import re

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

#%%

PATH_INPUT = "processed"
PATH_NOVELS = "novels"
FOLDER_PATH = os.path.join(PATH_INPUT,PATH_NOVELS)
f = "a_study_in_scarlet.txt"
filepath = os.path.join(FOLDER_PATH,f)

if os.path.isfile(filepath) and f.endswith(".txt"):
    print(f"Process file: {filepath}")

    with open(filepath, "r") as fp:
        content = fp.read()

#%%
#regexp to get all words separately without punctuation
tokenizer = RegexpTokenizer(r'\w+')
content_removed_punct = tokenizer.tokenize(content)

#make words lowercase
content_lower = []
for word in content_removed_punct:
    content_lower.append(word.lower())
#print(content_lower)  

#%%
#count frequency of words and print 100 most common
frequency = {}
for word in content_lower:
    frequency[word] = frequency.get(word,0) + 1
    
#sort dictionary according to value (descending order)  
sorted_freq = sorted(frequency.items(), key = lambda x: x[1], reverse = True)

#print 100 most common words
print(sorted_freq[:100])

#%%
#tokenize content by sentences and remove newlines
content = content.replace('     ','')
content_sent = sent_tokenize(content)

new_content = []
for sub in content_sent:
    new_content.append(re.sub('\n', '', sub))
#print(new_content)

#%%
#count average sentence length
summ = 0
n = 0
for sentence in new_content:
    n += 1
    summ += len(sentence)
avg = summ/n
print(f"Average sentence length: {avg}")
