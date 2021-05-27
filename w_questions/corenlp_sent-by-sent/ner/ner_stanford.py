#%%
#setup
import nltk
from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
import re

import sys, os, subprocess
repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
sys.path.insert(1, os.path.join(sys.path[0], repo_dir))
from helper.HolmesReader import HolmesReader
holmesReader = HolmesReader()
#%%
server_url = 'http://localhost:9100'

# Lexical Parser
parser = CoreNLPParser(url=server_url)
# POS tagger
pos_tagger = CoreNLPParser(url=server_url, tagtype='pos')
# NER Tagger
ner_tagger = CoreNLPParser(url=server_url, tagtype='ner')
# Neural Dependency Parser
dep_parser = CoreNLPDependencyParser(url=server_url)

#%%
# sentence as example
sentence = "John and Jane Smith lives in New York and works at the Central Bank of America."
print(sentence)

tokens = list(parser.tokenize(sentence))

pos_tags = list(pos_tagger.tag(tokens))

ner_tags = list(ner_tagger.tag(tokens))
print(ner_tags)

#%%
def find_named_entites(ner_tags):
    """
    Joins entites that belong together and returns all named entities.
    """
    previous_tag = 'O'
    previous_entity = ''
    combined_entity = ''
    named_entites = []
 
    for entity in ner_tags:
        if entity[1] != "O":
            if entity[1] == previous_tag:
                if combined_entity:
                    combined_entity.append(entity[0])              
                else:
                    combined_entity = [previous_entity, entity[0]]           
        else:
            if combined_entity:
                joined_entity = ' '.join(combined_entity)
                named_entites.append((joined_entity,previous_tag))
                combined_entity = ''
            elif previous_tag !='O':
                named_entites.append((previous_entity,previous_tag))

        previous_entity = entity[0]
        previous_tag  = entity[1]

    #print(f"Named entites: {named_entites}")

    [person,location,organization,time,cause_of_death,criminal_charge,duration,title] = classify_entity(named_entites)
    
    return person,location,organization,time,cause_of_death,criminal_charge,duration,title

# %%
def classify_entity(named_entites):
    """
    Classifies the named entites into different predefined categories.
    """
    person = []
    location = []
    organization = []
    time = []
    cause_of_death = []
    criminal_charge = []
    duration = []
    title = []
    for entity,tag in named_entites:
        if tag == "PERSON":
            person.append(entity)
        elif tag == "ORGANIZATION":
            organization.append(entity)
        elif (tag == "STATE_OR_PROVINCE" or tag == "LOCATION" or tag == "CITY" or tag == "COUNTRY"):
            location.append(entity)
        elif (tag == "DATE" or tag == "TIME"):
            time.append(entity)
        elif tag == "CAUSE_OF_DEATH":
            cause_of_death.append(entity)
        elif tag == "CRIMINAL_CHARGE":
            criminal_charge.append(entity)
        elif tag == "DURATION":
            duration.append(entity)
        elif tag == "TITLE":
            title.append(entity)
        else:
            print(entity, tag)
    
    return(person,location,organization,time,cause_of_death,criminal_charge,duration,title)

#%%
[person,location,organization,time] = find_named_entites(ner_tags)


#%%
#try it on one story
story = holmesReader.get_story("the_final_problem")
text = story["text"]

#%%
#break text down into paragraphs
re_grep_paragraph = '(.*\n)'
paragraphs = re.findall(re_grep_paragraph, text, re.IGNORECASE)

person = []
location = []
organization = []
time = []
cause_of_death = []
criminal_charge = []
duration= []
title = []

for paragraph in paragraphs:
    paragraph = paragraph.strip()
    tokens = list(parser.tokenize(paragraph))
    ner_tags = list(ner_tagger.tag(tokens))
    [p,l,o,t,c,cr,d,tt] = find_named_entites(ner_tags)
    person.append(p)
    location.append(l)
    organization.append(o)
    time.append(t)
    cause_of_death.append(c)
    criminal_charge.append(cr)
    duration.append(d)
    title.append(tt)
    
print(person,location,organization,time,cause_of_death,criminal_charge,duration,title)

#%%
sentences = list(parser.tokenize_sents(text))
sents = nltk.tokenize.sent_tokenize(text)
person = []
location = []
organization = []
time = []
cause_of_death = []
criminal_charge = []
duration= []
title = []
for i, sentence in enumerate(sents):
    if i % 20 ==0:
        print(i)
    tokens = list(parser.tokenize(sentence))
    ner_tags = list(ner_tagger.tag(tokens))
    [p,l,o,t,c,cr,d,tt] = find_named_entites(ner_tags)
    person.append(p)
    location.append(l)
    organization.append(o)
    time.append(t)
    cause_of_death.append(c)
    criminal_charge.append(cr)
    duration.append(d)
    title.append(tt)

#print(person,location,organization,time,cause_of_death,criminal_charge,duration,title)
#%%
print(person)
#%%
#apply for all stories and novel chapters -> use helper
