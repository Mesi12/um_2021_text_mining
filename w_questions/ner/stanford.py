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
sentence = "John Smith Jane Smith lives in New York and works at the Central Bank of America."

tokens = list(parser.tokenize(sentence))
print(tokens)

pos_tags = list(pos_tagger.tag(tokens))
print(pos_tags)

ner_tags = list(ner_tagger.tag(tokens))
print(ner_tags)
# %%
def get_entities(tree):
    """
    Finds named entities of the tree created from the tagged content.
    """

    person = []
    location = []
    time = []
    organization = []

    for chunk in tree:
        if hasattr(chunk, 'label'):
            entity = " ".join(part[0] for part in chunk.leaves())
            if chunk.label() == "PERSON":
                person.append(entity)
            elif chunk.label() == "LOCATION":
                location.append(entity)
            elif (chunk.label() == "DATE") or (chunk.label() == "TIME"):
                time.append(entity)
            elif (chunk.label() == "ORGANIZATION"):
                organization.append(entity)

    return person, location, time, organization


def IOB_to_tree(iob_tagged):
    """
    From the given tuples (entity name, POS tag, entity type) creates a tree.
    """
    #credit: https://stackoverflow.com/questions/27629130/chunking-stanford-named-entity-recognizer-ner-outputs-from-nltk-format
    
    root = nltk.Tree('S', [])
    for token in iob_tagged:
        if token[2] == 'O':
            root.append((token[0], token[1]))
        else:
            try:
                if root[-1].label() == token[2]:
                    root[-1].append((token[0], token[1]))
                else:
                    root.append(nltk.Tree(token[2], [(token[0], token[1])]))
            except:
                root.append(nltk.Tree(token[2], [(token[0], token[1])]))
    return root

def magic(ner_output):
    chunked, pos = [], ""
    prev_tag = 0
    for i, word_pos in enumerate(ner_output):
        word, pos = word_pos
        if pos in ['PERSON', 'ORGANIZATION', 'LOCATION'] and pos == prev_tag:
            chunked[-1]+=word_pos
        else:
            chunked.append(word_pos)
        prev_tag = pos  

    clean_chunked = [tuple([" ".join(wordpos[::2]), wordpos[-1]]) if len(wordpos)!=2 else wordpos for wordpos in chunked]

    print(clean_chunked)

#%%
triples = [[name, pos, tp[1]] for (name, pos), tp in zip(pos_tags, ner_tags)]
print(triples)
tree = IOB_to_tree(triples)
[person, location, time, organization] = get_entities(tree)
#%%
magic(ner_tags)
# %%
person
# %%
location
# %%
organization
# %%
time
# %%
def rechunk(ner_output):
    chunked, pos = [], ""
    prev_tag = 0
    for i, word_pos in enumerate(ner_output):
        word, pos = word_pos
        if pos in ['PERSON', 'ORGANIZATION', 'LOCATION'] and pos == prev_tag:
            chunked[-1]+=word_pos
        else:
            chunked.append(word_pos)
        prev_tag = pos


    clean_chunked = [tuple([" ".join(wordpos[::2]), wordpos[-1]]) 
                    if len(wordpos)!=2 else wordpos for wordpos in chunked]

    return clean_chunked


print(rechunk(ner_tags))
# %%
