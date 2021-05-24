#%%
import nltk
from nltk.parse import CoreNLPParser
from nltk.parse.corenlp import CoreNLPDependencyParser
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
def mymagic(ner_tags):
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

    print(f"Named entites: {named_entites}")

    [person,location,organization,time] = classify_entity(named_entites)
    
    return person,location,organization,time

# %%
def classify_entity(named_entites):
    """
    Classifies the named entites into different predefined categories.
    """
    person = []
    location = []
    organization = []
    time = []
    for entity,tag in named_entites:
        if tag == "PERSON":
            person.append(entity)
        elif tag == "ORGANIZATION":
            organization.append(entity)
        elif tag == "STATE_OR_PROVINCE":
            location.append(entity)
        elif (tag == "DATE" or tag == "TIME"):
            time.append(entity)
    return(person,location,organization,time)

#%%
[person,location,organization,time] = mymagic(ner_tags)
print("person:",person)
print("location:",location)
print("organization:",organization)
print("time:",time)

# %%
