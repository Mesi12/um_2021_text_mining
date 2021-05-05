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
        dfs[entity_class] = pd.merge(dfs[entity_class], df_sentences, on='doc')
        
    return dfs


if __name__ == "__main__":

    extract_zip()

    (legend, annotations) = load_annotations()

    dfs = transform_to_dataframe(legend, annotations)

    dfs_output = add_sentences(dfs)

    #exporting overview table
    #df_overview = pd.concat(dfs, axis=1, keys=entity_classes)
    


# %%





# %%
