#%%
import nltk
import json
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap
#%%
with open("../story_characters.json", "r") as fp:
    data = json.load(fp)
data

#%%
with open("../dataset/metadata.json", "r") as fp:
    metadata = json.load(fp)
metadata

# %%
combined_names=[]
for i in data.values():
  for j in i:
    combined_names.append(j)
print (combined_names)

# %%

distinct_names = []
for name in combined_names:
    if name not in distinct_names:
        distinct_names.append(name)
print(distinct_names)
r = re.compile("'Sherlock'")
a = list(filter(r.match,distinct_names))
print(a) #none =)
# %%
#count number of Holmes appearance in each story 
counts = []
for v in data.values():
    s = sum('Holmes' in name for name in v)
    counts.append(s)
print(counts)

# %%
story_collection = {}

for collection_id, collection in metadata['collections'].items():
    for story in collection["stories"].keys():
        story_collection[story] = collection["title"]
print(story_collection)
# %%
# %%
stories = data.keys()
df = pd.DataFrame(stories, columns = ['Story'])
df["Counts of Holmes"] = counts
collections = []
for story in stories:
    collections.append(story_collection[story])
df["Collection"] = collections
print(df)

# %%
order=["The Adventures of Sherlock Holmes", 
"The Memoirs of Sherlock Holmes", 
"The Return of Sherlock Holmes", 
"His Last Bow", 
"The Case-Book of Sherlock Holmes"]
plt.figure()
sns.set_style("whitegrid")
g = sns.boxplot( x=df["Collection"], y=df["Counts of Holmes"], width=0.3, order = order)
g.set_ylabel("Appearance of 'Holmes'")
g.set_xticklabels(g.get_xticklabels(),rotation=90)
g.set_xticklabels(textwrap.fill(x.get_text(), 20) for x in g.get_xticklabels())
g.set_title('Number of appearances of Sherlock in different collecions')
plt.tight_layout()
plt.savefig('appearances_of_Sherlock.png')
# %%
