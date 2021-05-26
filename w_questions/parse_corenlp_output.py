# %%
import os
import json
import pandas as pd

DEBUG_MODE = False
FOLDER_INPUT = "output"
FOLDER_OUTPUT = "output_parsed"

def extract_named_entities(annots):
    """
    Extract named entities and return list of them
    """
    entities = []
    for sentence in annots['sentences']:
        for entity in sentence['entitymentions']:
            entities.append([
                entity['docTokenBegin'],
                entity['text'],
                entity['ner'],
                entity.get('nerConfidences', None)
            ])

    return entities


def extract_tokens(annots):
    """
    Extract tokens and POS tags to return a list
    """
    tokens = []
    for sentence in annots['sentences']:
        for token in sentence['tokens']:
            tokens.append([
                token['lemma'],
                token['pos'],
                token['ner']
            ])

    return tokens


def extract_relations(annots):
    """
    Extract relations and return list of relations
    """
    kbps = []
    for sentence in annots['sentences']:
        if "kbp" in sentence.keys():
            for kbp in sentence['kbp']:
                kbps.append([
                    kbp['subject'],
                    kbp['relation'],
                    kbp['object']
                ])

    return kbps


def extract_quotes(annots):
    """
    Extract quotes and return list of quote and speaker
    returns list [speaker, canonicalSpeaker, text]
    """
    quotes = []
    for quote in annots['quotes']:

        quotes.append([
            quote['id'],
            quote['speaker'],
            quote['canonicalSpeaker'],
            quote['text'].strip('"')])

    return quotes


def concat_csvs(folder_path):
    print(f"merge csv files for {folder_path}")
    frames = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        if os.path.isfile(filepath) and filepath.endswith(".csv") and filename != "_merged_.csv":
            df_sub = pd.read_csv(filepath)
            df_sub['title'] = filename.replace(".csv", "")
            frames.append(df_sub)

    df = pd.concat(frames)
    df.to_csv(os.path.join(folder_path, "_merged_.csv"), index=False)

    return os.path.join(folder_path, "_merged_.csv")


def clean_names(filepath):
    print(f"clean dataframe for {filepath}")

    # normalize persons
    import pandas as pd
    df_mapping = pd.read_csv(os.path.join("name_normalization", "mapping_character_normalization.csv"))
    df_mapping = df_mapping[['dirty_character', 'final_decision']].rename(
        {"dirty_character":"from", "final_decision":"clean_text"},
        axis=1)

    ### NER dataset
    df_ner = pd.read_csv(filepath)
    # clean dataset from pronouns
    pronouns = "he,him,his,she,her".split(",")
    df_ner = df_ner[~df_ner['text'].str.lower().isin(pronouns)].reset_index(drop=True)
    # join with mapping dataset to get clean name, remove "from" column -> adds column "clean_text"
    df_ner = df_ner.merge(df_mapping, left_on="text", right_on="from", how="left")
    df_ner = df_ner.drop(columns="from")
    # duplicate clean_text for others and fill remaining PERSON with others
    df_ner['clean_text_others'] = df_ner['clean_text'].copy()
    df_ner.loc[df_ner.ner == "PERSON", "clean_text_others"] = df_ner.loc[df_ner.ner == "PERSON", "clean_text_others"].fillna("other")
    # fill remaining NaNs from original text
    df_ner['clean_text'] = df_ner['clean_text'].fillna(df_ner['text'])
    df_ner['clean_text_others'] = df_ner['clean_text_others'].fillna(df_ner['text'])
    df_ner.to_csv(filepath, index=False)



if __name__ == "__main__":

    #folder = os.path.join(FOLDER_INPUT, "novel_a_study_in_scarlet")
    #output_folder = os.path.join(FOLDER_OUTPUT, "novel_a_study_in_scarlet")
    folder = os.path.join(FOLDER_INPUT)
    output_folder = os.path.join(FOLDER_OUTPUT)
    os.makedirs(output_folder, exist_ok=True)

    all_relations = []
    for file_name in os.listdir(folder):
        filepath = os.path.join(folder, file_name)


        if os.path.isfile(filepath) and filepath.endswith(".json"):

            with open(filepath, "r") as f:
                annots = json.load(f)
                story = file_name.replace(".txt.json", "")

                # logging
                print(f"#### {file_name}")
                
                # extract entitymentions
                entities = extract_named_entities(annots)
                output_path = os.path.join(output_folder, "ner")
                os.makedirs(output_path, exist_ok=True)
                pd.DataFrame(
                    data=entities,
                    columns="docTokenBegin,text,ner,nerConfidences".split(","),
                ).to_csv(
                    os.path.join(output_path, f"{story}.csv"),
                    index=False
                )

                # extract tokens
                tokens = extract_tokens(annots)
                output_path = os.path.join(output_folder, "tokens")
                os.makedirs(output_path, exist_ok=True)
                pd.DataFrame(
                    data=tokens,
                    columns="lemma,pos,ner".split(","),
                ).to_csv(
                    os.path.join(output_path, f"{story}.csv"),
                    index=False
                )

                # extract relations
                kbps = extract_relations(annots)
                all_relations.extend([[story] + i for i in kbps])


                # extract quotes + speaker
                if "quotes" in annots.keys():
                    quotes = extract_quotes(annots)
                    output_path = os.path.join(output_folder, "quotes")
                    os.makedirs(output_path, exist_ok=True)
                    pd.DataFrame(
                        data=quotes,
                        columns="occurence,speaker,canonicalSpeaker,text".split(","),
                    ).to_csv(
                        os.path.join(output_path, f"{story}.csv"),
                        index=False
                    )
        if DEBUG_MODE:
            break


    if all_relations:
        output_path = os.path.join(output_folder, "relation")
        os.makedirs(output_path, exist_ok=True)
        pd.DataFrame(
            data=all_relations,
            columns="story,subject,relation,object".split(","),
        ).to_csv(
            os.path.join(output_path, "all_stories.csv"),
            index=False
        )

    # concat all dataframes
    ner_merged_file = concat_csvs(os.path.join(FOLDER_OUTPUT, "ner"))
    token_merged_file = concat_csvs(os.path.join(FOLDER_OUTPUT, "tokens"))

    # clean names
    clean_names(ner_merged_file)

    print("done")

# %%
