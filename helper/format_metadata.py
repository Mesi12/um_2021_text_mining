# %%
import json
import os
from datetime import date, datetime


def get_date(data):
    year = data['year']
    month = datetime.strptime(data['month'], '%B')
    return date(int(year), int(month.month), 1)


if __name__ == "__main__":

    with open("metadata.json", "r") as f:
        metadata = json.load(f)

    for n, novel in metadata['novels'].items():
        publish_date = get_date(novel)
        novel['publish_date'] = publish_date.strftime('%Y-%m-%d')

    for c, collection in metadata['collections'].items():
        for s, story in collection['stories'].items():
            publish_date = get_date(story)
            story['publish_date'] = publish_date.strftime('%Y-%m-%d')

    with open("metadata.json", "w") as f:
        pretty_print = json.dumps(metadata, indent=4, sort_keys=True)
        f.write(pretty_print)

# %%

import json
import os
import pandas as pd


if __name__ == "__main__":

    with open("metadata.json", "r") as f:
        metadata = json.load(f)

    flatten = []
    cols = "collection,title,publishdate,setdate".split(",")

    for n, novel in metadata['novels'].items():
        flatten.append([
            "novel",
            n,
            novel['publish_date'],
            novel['plot']['start_date']
        ])


    for c, collection in metadata['collections'].items():
        for s, story in collection['stories'].items():
            flatten.append([
                c,
                s,
                story['publish_date'],
                story['plot']['start_date']
            ])


    df_flatten = pd.DataFrame(flatten, columns=cols)
    df_flatten.to_csv("metadata_flatten.csv", index=False)
# %%
