#%%
from sklearn.metrics import cohen_kappa_score
from itertools import combinations
import zipfile
import json
import os
import re
import pandas as pd
import numpy as np

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


def transform_to_dataframe(legend, annotations, annotators):
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
        df_entity_class = df_entity_class.rename(columns=annotators)
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


def calculate_kappa(col1, col2):
    num_samples = col1.shape[0]

    # extract all possible classes for multiclass problem
    classes = set()
    classes.update(list(col1.unique()))
    classes.update(list(col2.unique()))

    # Observed proportion of the times the judges agreed
    p_a = sum(col1 == col2) / num_samples

    # Probability that the two judges agreed by chance
    # Pooled marginals
    p_e_factors = []
    for c in classes:
        p_c = (sum(col1 == c) / num_samples) * (sum(col2 == c) / num_samples)
        p_e_factors.append(p_c)
    p_e = sum([p_e for p_e in p_e_factors])

    # Kappa statistic
    k = (p_a - p_e) / (1 - p_e)

    k_measure = f"agreed: {p_a:.4f}, by chance {p_e:.4f}, kappa: {k:.4f}"
    #print(f"For comparison with cohen sklearn: {cohen_kappa_score(col1, col2):.4f}")
    return (p_a, p_e, k, k_measure)




if __name__ == "__main__":

    annotators = {
        "MerlinKoehler": "judge1",
        "Mesi":"judge2",
        "accordionmonkey":"judge3",
        "gecco": "judge4"
    }

    extract_zip()
    (legend, annotations) = load_annotations()
    dfs = transform_to_dataframe(legend, annotations, annotators)
    dfs_output = add_sentences(dfs)

    # kappa measure
    pairs = list(combinations(list(annotators.values()), 2))
    for entity in dfs_output.keys():
        print(f"# entity: {entity}")
        df = dfs_output[entity]
        df[list(annotators.values())] = df[list(annotators.values())].fillna("no_entity")

        p_a_measures = []
        p_e_measures = []
        k_measures = []
        k_outputs = []
        for pair in pairs:
            p_a, p_e, k, k_output = calculate_kappa(df[pair[0]], df[pair[1]])
            p_a_measures.append(p_a)
            p_e_measures.append(p_e)
            k_measures.append(k)
            k_outputs.append(str(pair))
            k_outputs.append(k_output)
            print(pair)
            print(k_output)
        
        print(np.mean(k_measures))
        k_outputs.append(f"\ntotal p_a: {np.mean(p_a_measures)}")
        k_outputs.append(f"\ntotal p_e: {np.mean(p_e_measures)}")
        k_outputs.append(f"\ntotal k: {np.mean(k_measures)}")

        print(f"export to output_{entity}.csv")
        df.to_csv(f"output_{entity}.csv", index=False)
        with open(f"output_{entity}_kappa.txt", "w") as fp:
            fp.write("\n".join(k_outputs))

# %%
