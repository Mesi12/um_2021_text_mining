# %%
import os
import nltk
import pandas as pd

from nltk.parse import CoreNLPParser, corenlp

SERVER_URL = 'http://localhost:9000'


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


#%%

PATH_TAGTOG_DOCS = os.path.join('..',PATH_DATASET,PATH_VALIDATION,"tagtog_docs")
sentences = []
#get sentences of the validation set
for f in os.listdir(PATH_TAGTOG_DOCS):
    filepath = os.path.join(PATH_TAGTOG_DOCS, f)
    if os.path.isfile(filepath) and f.endswith(".txt"):
        with open(filepath, "r") as fp:
            sentences.append([f.split(".")[0], fp.read()])

df_stanford = pd.DataFrame(sentences, columns=["doc","sentences"])

#find characters in validation set with our NER method
tagtog_characters = []
for sentence in df_stanford["sentences"]:
    token = nltk.tokenize.word_tokenize(sentence)
    postag = nltk.pos_tag(token)
    ne_tagged = st.tag(token)
    triples = [[name, pos, tp[1]] for (name,pos), tp in zip(postag, ne_tagged)]
    tree = IOB_to_tree(triples)
    [person,location,time] = get_entities(tree)
    if person: 
        person = " | ".join(sorted(person))
    tagtog_characters.append(person)

df_stanford["nltk_characters"] = tagtog_characters
print(df_stanford.shape)


# %%

if __name__ == "__main__":
    # Lexical Parser
    parser = CoreNLPParser(url=SERVER_URL)
    # POS tagger
    pos_tagger = CoreNLPParser(url=SERVER_URL, tagtype='pos')
    # NER Tagger
    ner_tagger = CoreNLPParser(url=SERVER_URL, tagtype='ner')


    df = pd.read_csv("output_person.csv")
    corenlp_tags = []
    for sentence in df['sentences']:
        tokens = list(parser.tokenize(sentence))
        pos_tags = list(pos_tagger.tag(tokens))
        ner_tags = list(ner_tagger.tag(tokens))
        triples = [[name, pos, tp[1]] for (name,pos), tp in zip(pos_tags, ner_tags)]
        tree = IOB_to_tree(triples)
        [person,location,time] = get_entities(tree)
        person = " | ".join(sorted(person))
        corenlp_tags.append(person)

    df['coreNLP'] = corenlp_tags
    df['coreNLP'].replace("", np.nan, inplace=True)
    df['coreNLP'].fillna('no_entity', inplace=True)
    
    
    
    # location = " | ".join(sorted(location))



# %%
df_val = pd.read_csv("../dataset/validation_set/output_characters.csv")
# merge with nltk output
df_val = pd.merge(df_val, df_stanford[['doc', 'nltk_characters']], on="doc", how="left")
# remove rows with agreement False
df_val = df_val[df_val.judge1 == df_val.judge2]
# translate nltk into 0/1
df_val['nltk_text'] = df_val.nltk_characters
df_val.nltk_characters.fillna("0", inplace=True)
df_val.loc[df_val['nltk_characters'] != "0", "nltk_characters"] = "1"
df_val = df_val.astype({"nltk_characters":int})
# actual: judge vs predicted: nltk
# 1.1 -> TP
TP = len(df_val[(df_val.judge1 == 1) & (df_val.nltk_characters == 1)])
# 0.0 -> TN
TN = len(df_val[(df_val.judge1 == 0) & (df_val.nltk_characters == 0)])
# 1.0 -> FN
FN = len(df_val[(df_val.judge1 == 1) & (df_val.nltk_characters == 0)])
# 0.1 -> FP
FP = len(df_val[(df_val.judge1 == 0) & (df_val.nltk_characters == 1)])
# precision
precision = TP / (TP + FP)
# recall
recall = TP / (TP + FN)
# f1 scores
f1_score = 2 * (recall * precision) / (recall + precision)

df_val.to_csv("output_stanford_characters.csv", index=False)
with open("output_stanford_characters_quality.txt", "w") as fp:
    fp.write(f"Precision: {precision:.3f}\nrecall: {recall:.3f}\nf1 score: {f1_score:.3f}")


print(f"Precision: {precision:.3f}")
print(f"recall: {recall:.3f}")
print(f"f1 score: {f1_score:.3f}")

# %%


