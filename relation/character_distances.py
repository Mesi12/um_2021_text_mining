#%%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

file = os.path.join('..','w_questions','output_parsed','ner','_merged_.csv')
df =  pd.read_csv(file)

# %%
#extract person types
df_person = df[df["ner"]=="PERSON"]
# %%
#group by stories
df_grouped = df_person.groupby(by="title",sort="False")
#%%
data = []
for story_name in df_grouped.groups.keys():
    df_story = df_grouped.get_group(story_name)
    position = list(df_story["docTokenBegin"])
    max_token = max(position)
    characters = list(df_story["clean_text"])
    for i in range(len(position)):
        for j in range(i+1,len(position)):
            if (characters[i] != characters[j]):
                dist = abs(position[i]-position[j])
                data.append([characters[i],characters[j],dist,story_name,max_token])
df_distances = pd.DataFrame(data, columns = ["character1", "character2","distance","story","max_token"])
df_distances

#%%
data = []
story_name= "the_hound_of_the_baskervilles"
df_story = df_grouped.get_group(story_name)
position = list(df_story["docTokenBegin"])
max_token = max(position)
characters = list(df_story["clean_text"])
for i in range(len(position)):
    for j in range(i+1,len(position)):
        if (characters[i] != characters[j]):
            dist = abs(position[i]-position[j])
            data.append([characters[i],characters[j],dist,story_name,max_token])
df_distances2 = pd.DataFrame(data, columns = ["character1", "character2","distance","story","max_token"])

#%%
df_distances2["distance"].hist(bins=100)
plt.show()

#%%
#merge first two columns of df_distances2
a = df_distances2["character1"]
b = df_distances2["character2"]
merged = []
for i in range(len(a)):
    merged.append((" | ".join(sorted([a[i],b[i]]))))
merged
df_distances2["merged"] = merged
df_dist_group = df_distances2.groupby(["story","merged"]).agg({"distance": "sum"})
df_dist_group
#%%
df_dist_group.reset_index()
df_dist_group.rename({level_1: ....})
#df_distances2["distanceNorm"] = 
#%%
plt.xlim((0,max_token))

mean = 0
variance = np.var(df_distances2["distance"])
sigma = np.sqrt(variance)
x = np.linspace(0,max_token,1000)
plt.plot(x,mlab.normpdf(x,mean,sigma))

plt.show()


# %%
df_distances.to_csv('characterDistances.csv',index=False)
# %%
