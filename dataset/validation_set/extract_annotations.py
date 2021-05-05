#%%
import zipfile
import json
import os
import re
import pandas as pd

PATH_ANNOT = "tagtog_annotations"
PATH_TAGTOG_DOCS = "tagtog_docs"
TMP = "tmp"


def extract_zip():
    zip_path = os.path.join(PATH_ANNOT, "tagtog_textmining-project.zip")
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(PATH_ANNOT, TMP))
    
        os.remove(zip_path)


def parse_doc_id(annot_file):
    return annot_file.split("-")[1].split(".")[0]


def load_annotations():
    legend = ""
    annotations = {}

    with open(os.path.join(PATH_ANNOT, TMP, "textmining-project", "annotations-legend.json"), "r") as fp:
        legend = json.load(fp)

    members_path = os.path.join(PATH_ANNOT, TMP, "textmining-project", "ann.json", "members")
    for member in os.listdir(members_path):
        member_path = os.path.join(members_path, member)
        if os.path.isdir(member_path):
            annotations[member] = {}
            annot_file_path = os.path.join(member_path, "pool", "project")

            for annot_file in os.listdir(annot_file_path):

                if os.path.isfile(os.path.join(annot_file_path,annot_file)) and annot_file.endswith(".json"):

                    doc_id = parse_doc_id(annot_file)

                    with open(os.path.join(annot_file_path, annot_file), "r") as fp:
                        annotations[member][doc_id] = json.load(fp)

    return (legend, annotations)


def transform_to_dataframe(legend, annotations):
    flatten = []
    for member, docs in annotations.items():
        for doc, metadata in docs.items():
            for entity in metadata['entities']:
                entity_class = legend[entity['classId']]
                text = entity['offsets'][0]['text']
                flatten.append([entity_class, doc, member, text])
    df = pd.DataFrame(flatten, columns=["entity_class", "doc", "judge", "entity"])

    entity_classes = list(legend.values())
    dfs = {}
    for entity_class in entity_classes:
        df_entity_class = df[df.entity_class == entity_class]
        df_entity_class = df_entity_class.pivot_table(index='doc', columns='judge', values='entity', aggfunc=(lambda x: " | ".join(sorted(x, reverse=False))))
        df_entity_class.columns.name = None
        df_entity_class = df_entity_class.reset_index()
        dfs[entity_class] = df_entity_class

    return dfs


def add_sentences(dfs):

    sentences = []
    for f in os.listdir(PATH_TAGTOG_DOCS):
        filepath = os.path.join(PATH_TAGTOG_DOCS, f)
        if os.path.isfile(filepath) and f.endswith(".txt"):
            with open(filepath, "r") as fp:
                sentences.append([f.split(".")[0], fp.read()])
    
    df_sentences = pd.DataFrame(sentences, columns=["doc","sentences"])

    for entity_class in dfs.keys():
        if dfs[entity_class].shape[0] == 0:
            continue
        dfs[entity_class] = pd.merge(dfs[entity_class], df_sentences, on='doc', how="right")

    return dfs


def calculate_kappa(df):
    # Observed proportion of the times the judges agreed
    p_a = sum(df.judge1 == df.judge2) / df.shape[0]

    # Pooled marginals
    p_0 = (sum(df.judge1 == 0) + sum(df.judge2 == 0)) / (2*df.shape[0])
    p_1 = (sum(df.judge1 == 1) + sum(df.judge2 == 1)) / (2*df.shape[0])

    # Probability that the two judges agreed by chance
    p_e = p_0**2 + p_1**2

    # Kappa statistic
    k = (p_a - p_e) / (1 - p_e)

    k_measure = f"agreed: {p_a:.2f}, by chance {p_e:.2f}\nkappa: {k:.2f}"

    print(k_measure)
    return k_measure


if __name__ == "__main__":

    extract_zip()

    (legend, annotations) = load_annotations()

    dfs = transform_to_dataframe(legend, annotations)

    dfs_output = add_sentences(dfs)

    df_characters = dfs_output['character']
    df_characters['judge1'] = df_characters['Mesi']
    df_characters['judge2'] = df_characters['accordionmonkey']
    df_characters['judge1'].fillna('0', inplace=True)
    df_characters['judge2'].fillna('0', inplace=True)
    df_characters.loc[df_characters['judge1'] != "0", "judge1"] = "1"
    df_characters.loc[df_characters['judge2'] != "0", "judge2"] = "1"
    df_characters = df_characters.astype({"judge1":int, "judge2":int})

    cols = ['doc', 'sentences', 'Mesi', 'accordionmonkey', 'judge1', 'judge2']
    df_characters = df_characters[cols]

    
    k_measure = calculate_kappa(df_characters)

    print("export to output_characters.csv")
    df_characters.to_csv("output_characters.csv", index=False)
    with open("output_characters_kappa.txt", "w") as fp:
        fp.write(k_measure)

    #exporting overview table
    #df_overview = pd.concat(dfs, axis=1, keys=entity_classes)
    


# %%





# %%
