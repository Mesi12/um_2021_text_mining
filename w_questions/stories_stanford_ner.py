# %%
import os
import nltk
import json

# https://stackoverflow.com/questions/22081209/find-the-root-of-the-git-repository-where-the-file-lives#comment44778829_22081487
import sys, subprocess
repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
sys.path.insert(1, os.path.join(sys.path[0], repo_dir))
from helper.HolmesReader import HolmesReader

# config
PATH_DATASET = "dataset"
PATH_INPUT = "processed"
PATH_STORIES = "stories"
PATH_VALIDATION = "validation_set"
FILENAME_NAMED_ENTITIES = "story_named_entities.json"
PATH_STANFORD_NER = os.path.join(
    '..', "libraries", "stanford-ner-4.2.0", "stanford-ner-2020-11-17")

# define the Stanford NER tagger
classifier = os.path.join(PATH_STANFORD_NER, "classifiers",
                          "english.muc.7class.distsim.crf.ser.gz")
jar = os.path.join(PATH_STANFORD_NER, "stanford-ner.jar")
st = nltk.tag.StanfordNERTagger(classifier, jar, encoding='utf-8')

# helper for reading stories & novels
holmesReader = HolmesReader()

# %%


def named_entities():
    """
    Finds named entities in stories. 
    """
    NAMED_ENTITIES = {}

    collections = holmesReader.get_collections()

    for collection_id, collection in collections.items():
        if len(NAMED_ENTITIES.keys()) > 0:
            continue
        for story_id, story in collection['stories'].items():
            if len(NAMED_ENTITIES.keys()) > 0:
                continue
            print(f"Collection {collection_id}: story {story_id}")
            content = story['text']

            # tokenize text by words
            tokenized_content = nltk.tokenize.word_tokenize(content)
            # tag content by Stanford NER tool
            tagged_content = st.tag(tokenized_content)
            # POS tagging
            pos_tags = nltk.pos_tag(tokenized_content)
            # join info about POS tag and named entity tag
            triples = [[name, pos, tp[1]] for (name, pos), tp in zip(pos_tags, tagged_content)]
            # create tree from the tuples
            tree = IOB_to_tree(triples)
            # extract named entities (persons, locations, times)
            [person, location, time] = get_entities(tree)
            # save named entites to dictionary
            NAMED_ENTITIES[story_id] = {}
            NAMED_ENTITIES[story_id]["characters"] = person
            NAMED_ENTITIES[story_id]["locations"] = location
            NAMED_ENTITIES[story_id]["dates and times"] = time
    return NAMED_ENTITIES


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


def save_entities(ENTITIES):
    """
    Saves named entities into the json file.
    """
    with open(FILENAME_NAMED_ENTITIES, "w") as fp:
        parsed = json.dumps(ENTITIES, indent=4, sort_keys=True)
        fp.write(parsed)


# %%
if __name__ == "__main__":
    print("start")
    entities = named_entities()
    save_entities(entities)
    print("done")
# %%
