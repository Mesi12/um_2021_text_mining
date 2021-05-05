#%%
import os
import re
import nltk
#%%
#config
PATH_DATASET = "dataset"
PATH_INPUT = "processed"
PATH_STORIES = "stories"
#%%

def story_named_entities():
    """
    Finds named entities in stories. 
    """
    FOLDER_PATH = os.path.join(PATH_DATASET,PATH_INPUT,PATH_STORIES)
    for collection in os.listdir(FOLDER_PATH):
        PATH_COLLECTION = os.path.join(FOLDER_PATH,collection)
        try:
            collection_title = make_title(collection)
        except NameError:
            continue

        print(f"Process collection: {collection_title}")

        for f in os.listdir(PATH_COLLECTION):
            filepath = os.path.join(PATH_COLLECTION,f)

            if os.path.isfile(filepath) and f.endswith(".txt"):
                print(f"Process file: {filepath}")

                with open(filepath, "r") as fp:
                    content = fp.read()
                    #Tokenize content
                    content_sent = nltk.tokenize.sent_tokenize(content)
                    content_word = nltk.tokenize.word_tokenize(content)

                    #Pos tagging
                    tagged_content = nltk.pos_tag(content_word)

                    #Shallow parsing
                    parsed_content = nltk.chunk.ne_chunk(tagged_content)

                    #Find named entities
                    named_entities = find_named_entities(parsed_content)

                    #find characters
                    locations = extract_entities(named_entities,"location")
                
            else:
                print('File not found.')

#%%
"""
For running the function only on one specific story
"""
PATH_COLLECTION = "3_the_return_of_sherlock_holmes"
FOLDER_PATH = os.path.join(PATH_DATASET,PATH_INPUT,PATH_STORIES,PATH_COLLECTION)
f = "the_adventure_of_the_golden_pince_nez.txt"
filepath = os.path.join(FOLDER_PATH,f)

if os.path.isfile(filepath) and f.endswith(".txt"):
    print(f"Process file: {filepath}")

    with open(filepath, "r") as fp:
                    content = fp.read()
                    #Tokenize content
                    content_sent = nltk.tokenize.sent_tokenize(content)
                    content_word = nltk.tokenize.word_tokenize(content)

                    #Pos tagging
                    tagged_content = nltk.pos_tag(content_word)

                    #Shallow parsing
                    parsed_content = nltk.chunk.ne_chunk(tagged_content)

                    #Find named entities
                    named_entities = find_named_entities(parsed_content)
                    print(named_entities)

                    #find characters
                    characters = extract_entities(named_entities,"person")
                
else:
    print('File not found.')
    
#%%
def make_title(collection):
    if collection == "1_the_adventures_of_sherlock_holmes":
        original_title = "The Adventures of Sherlock Holmes"
    elif collection == "2_the_memoirs_of_sherlock_holmes":
        original_title = "The Memoirs of Sherlock Holmes"
    elif collection == "3_the_return_of_sherlock_holmes":
        original_title = "The Return of Sherlock Holmes"
    elif collection == "4_his_last_bow":
        original_title = "His Last Bow"
    elif collection == "5_the_case_book_of_sherlock_holmes":
        original_title = "The Case-Book of Sherlock Holmes"
    else:
        raise NameError(f"Provided name {collection} is not valid. Skip it.")
    return original_title
#%%
def find_named_entities(parsed):
    named_entities = []
    for chunk in parsed:
        if hasattr(chunk, 'label'):
            entity = chunk.label(), ' '.join(c[0] for c in chunk)
            if entity not in named_entities:
                named_entities.append(entity)
    return named_entities

#%%
def extract_entities(entities,tp):
    """
    Possible tp values: "person", "facility", "organization", "gpe", "gsp", "location"
    """
    characters = []
    facilities = []
    geopolitical_entities = []
    organizations = []
    gsp = []
    locations = []
    for e in entities:
        if e[0] == "PERSON":
            characters.append(e[1])
        elif e[0] == "FACILITY":
            facilities.append(e[1])
        elif e[0] == "GPE":
            geopolitical_entities.append(e[1])
        elif e[0] == "ORGANIZATION":
            organizations.append(e[1])
        elif e[0] == "GSP":
            gsp.append(e[1])
        elif e[0] == "LOCATION":
            locations.append(e[1])
        else:
            print(e[0],'is missing!!!!!!')
    if tp == "person":
        if characters:
            print("Characters: ",characters)
            return characters
    if tp == "facility":
        if facilities:
            print('Facilities: ',facilities)
            return facilities
    if tp == "organization":
        if organizations:
            print('Organizations: ',organizations)
            return organizations
    if tp == "gpe":
        if geopolitical_entities:
            print('Geopolitical entities: ',geopolitical_entities)
            return geopolitical_entities
    if tp == "gsp":
        if gsp:
            print('Geographical-Social-Political Entities: ', gsp)
            return gsp
    if tp == "location":
        if locations:
            print("Locations: ", locations)
            return locations
    
#%%
if __name__ == "__main__":
    print("start")
    story_named_entities()
    #todo save results to some output file???
# %%
