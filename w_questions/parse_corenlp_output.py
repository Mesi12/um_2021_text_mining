# %%
import os
import json
import pandas as pd


def extract_named_entities(annots):
    """
    Extract named entities and return list of them
    """
    entities = []
    for sentence in annots['sentences']:
        for entity in sentence['entitymentions']:
            entities.append([
                entity['text'],
                entity['ner'],
                entity.get('normalizedNER')
            ])

    return entities


def extract_relations(annots):
    """
    Extract relations and return list of relations
    """
    kbps = []
    for sentence in annots['sentences']:
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


if __name__ == "__main__":

    all_relations = []
    for file_name in os.listdir("output"):
        filepath = os.path.join("output", file_name)

        if file_name != "a_case_of_identity.txt.json":
            continue

        if os.path.isfile(filepath) and filepath.endswith(".json"):

            with open(filepath, "r") as f:
                annots = json.load(f)
                story = file_name.replace(".txt.json", "")

                # logging
                print(f"#### {file_name}")
                
                # extract entitymentions
                entities = extract_named_entities(annots)
                pd.DataFrame(
                    data=entities,
                    columns="text,ner,normalizedner".split(","),
                ).to_csv(
                    os.path.join("output_parsed", "ner", f"{story}.csv"),
                    index=False
                )

                # extract relations
                kbps = extract_relations(annots)
                all_relations.extend([[story] + i for i in kbps])


                # extract quotes + speaker
                quotes = extract_quotes(annots)
                pd.DataFrame(
                    data=quotes,
                    columns="occurence,speaker,canonicalSpeaker,text".split(","),
                ).to_csv(
                    os.path.join("output_parsed", "quotes", f"{story}.csv"),
                    index=False
                )

    pd.DataFrame(
        data=all_relations,
        columns="story,subject,relation,object".split(","),
    ).to_csv(
        os.path.join("output_parsed", "relation", "all_stories.csv"),
        index=False
    )

    


# %%
