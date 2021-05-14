#%%
import os
import nltk
import json

#config
PATH_DATASET = "dataset"
PATH_INPUT = "processed"
PATH_STORIES = "stories"
PATH_VALIDATION = "validation_set"
FILENAME_NAMED_ENTITIES = "story_named_entities.json"
NAMED_ENTITIES = {}
PATH_STANFORD_NER = os.path.join('..',"libraries","stanford-ner-4.2.0","stanford-ner-2020-11-17")

#define the Stanford NER tagger
classifier = os.path.join(PATH_STANFORD_NER,"classifiers","english.muc.7class.distsim.crf.ser.gz")
jar = os.path.join(PATH_STANFORD_NER,"stanford-ner.jar")
st = nltk.tag.StanfordNERTagger(classifier, jar, encoding='utf-8')

#%%
def named_entities():
    """
    Finds named entities in stories. 
    """
    FOLDER_PATH = os.path.join('..',PATH_DATASET,PATH_INPUT,PATH_STORIES)
    for collection in os.listdir(FOLDER_PATH):
        PATH_COLLECTION = os.path.join(FOLDER_PATH,collection)

        for f in os.listdir(PATH_COLLECTION):
            filepath = os.path.join(PATH_COLLECTION,f)

            if os.path.isfile(filepath) and f.endswith(".txt"):
                print(f"Process file: {filepath}")

                with open(filepath, "r") as fp:
                    content = fp.read()
                    #tokenize text by words
                    tokenized_content = nltk.tokenize.word_tokenize(content)
                    #tag content by Stanford NER tool
                    tagged_content = st.tag(tokenized_content)
                    #POS tagging
                    pos_tags = nltk.pos_tag(tokenized_content)
                    #join info about POS tag and named entity tag
                    triples = [[name, pos, tp[1]] for (name,pos), tp in zip(pos_tags, tagged_content)]
                    #create tree from the tuples
                    tree = IOB_to_tree(triples)
                    #extract named entities (persons, locations, times)
                    [person, location, time] = get_entities(tree)
                    #save named entites to dictionary
                    filename = f.replace('.txt','')
                    NAMED_ENTITIES[filename] = {}
                    NAMED_ENTITIES[filename]["characters"] = person
                    NAMED_ENTITIES[filename]["locations"] = location
                    NAMED_ENTITIES[filename]["dates and times"] = time


#%%
def get_entities(tree):
    """
    Finds named entities of the tree created from the tagged content.
    """

    person = []
    location = []
    time = []

    for chunk in tree:
        if hasattr(chunk, 'label'):
            entity = " ".join(part[0] for part in chunk.leaves())
            if chunk.label() == "PERSON":
                person.append(entity)
            elif chunk.label() == "LOCATION":
                location.append(entity)
            elif (chunk.label() == "DATE") or (chunk.label() == "TIME"):
                time.append(entity)

    return person, location, time


#%%
def IOB_to_tree(iob_tagged):
    """
    From the given tuples (entity name, POS tag, entity type) creates a tree.
    """
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


#%%
def save_entities(ENTITIES):
    """
    Saves named entities into the json file.
    """
    with open(FILENAME_NAMED_ENTITIES, "w") as fp:
        parsed = json.dumps(ENTITIES, indent=4, sort_keys=True)
        fp.write(parsed)

#%%
if __name__ == "__main__":
    print("start")
    named_entities()
    save_entities(NAMED_ENTITIES)
# %%
