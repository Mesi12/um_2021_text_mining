# %%
import os
import json
import pandas as pd


def load_corenlp_annotations():

    corenlp_annots = []
    corenlp_annots_cols = "doc,person,location".split(",")
    pronouns = "he,him,his,she,her,hers".split(",")
    for filename in os.listdir("tagtog_docs_coreNLP_output"):
        filepath = os.path.join("tagtog_docs_coreNLP_output", filename)
        if os.path.isfile(filepath) and filepath.endswith(".json"):
            with open(filepath, "r") as f:
                annots = json.load(f)

            person = []
            location = []
            for sentence in annots['sentences']:
                for entity in sentence['entitymentions']:
                    if entity['ner'] == 'PERSON' and entity['text'].lower() not in pronouns:
                        person.append(entity['text'])
                        continue

                    if entity['ner'] == 'LOCATION':
                        location.append(entity['text'])
                        continue

            corenlp_annots.append([
                filename.replace(".txt.json", ""),
                " | ".join(sorted(person)),
                " | ".join(sorted(location))
            ])
    
    return pd.DataFrame(corenlp_annots, columns=corenlp_annots_cols)


def calculate_quality_measures(y_true, y_pred):
    # actual: judge vs predicted: nltk
    # 1.1 -> TP
    TP = sum(y_pred)    # because all y_true are 1
    # 0.0 -> TN
    TN = 0              # because all y_true are 1
    # 1.0 -> FN
    FN = 100 - sum(y_pred)
    # 0.1 -> FP
    FP = 0
    # precision
    precision = TP / (TP + FP)
    # recall
    recall = TP / (TP + FN)
    # f1 scores
    f1_score = 2 * (recall * precision) / (recall + precision)

    return f"precision: {precision:.4f}, recall: {recall:.4f}, f1 score: {f1_score:.4f}"


if __name__ == "__main__":

    df_corenlp = load_corenlp_annotations()
    df_corenlp.replace("", "no_entity", inplace=True)

    # person
    df_person = pd.read_csv("output_person.csv")
    df_person = df_person.merge(df_corenlp[['doc', 'person']], on="doc", how="left")
    df_person = df_person.rename({"person": "corenlp"}, axis=1)
    df_person = df_person[(df_person.judge1 == df_person.judge2) & (df_person.judge2 == df_person.judge3) & (df_person.judge3 == df_person.judge4)]
    # analysis: df_person[(df_person.judge1 != df_person.judge2) | (df_person.judge2 != df_person.judge3) | (df_person.judge3 != df_person.judge4)]

    # location
    df_location = pd.read_csv("output_location.csv")
    df_location = df_location.merge(df_corenlp[['doc', 'location']], on="doc", how="left")
    df_location = df_location.rename({"location": "corenlp"}, axis=1)
    df_location = df_location[(df_location.judge1 == df_location.judge2) & (df_location.judge2 == df_location.judge3) & (df_location.judge3 == df_location.judge4)]
    # analysis: df_location[(df_location.judge1 != df_location.judge2) | (df_location.judge2 != df_location.judge3) | (df_location.judge3 != df_location.judge4)]


    # calcuate measures
    print_output = []
    y_true = [1] * len(df_person)
    y_pred = list((df_person.judge1 == df_person.corenlp).astype(int))
    out = calculate_quality_measures(y_true, y_pred)
    print_output.append("Persons:")
    print_output.append(out)

    y_true = [1] * len(df_location)
    y_pred = list((df_location.judge1 == df_location.corenlp).astype(int))
    out = calculate_quality_measures(y_true, y_pred)
    print_output.append("\nLocations:")
    print_output.append(out)

    with open("output_corenlp_quality.txt", "w") as f:
        f.write("\n".join(print_output))

# %%
