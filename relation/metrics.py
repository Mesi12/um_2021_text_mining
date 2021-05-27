#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.stats import norm
#%%

file = os.path.join('..', 'w_questions', 'output_parsed', 'ner', '_merged_.csv')
df = pd.read_csv(file)

#%%
df_grouped = df[df["ner"]=="PERSON"].groupby(by="title",sort="False")
data = []
story_name= "a_case_of_identity"
df_story = df_grouped.get_group(story_name)
position = list(df_story["docTokenBegin"])
max_token = max(position)
characters = list(df_story["clean_text_others"])
for i in range(len(position)):
    for j in range(i+1,len(position)):
        if (characters[i] != characters[j]):
            dist = abs(position[i]-position[j])
            data.append([characters[i],characters[j],dist,story_name,max_token])
df_distances2 = pd.DataFrame(data, columns = ["character1", "character2","distance","story","max_token"])

plot_hist(df_distances2)

#%%
def plot_hist(df_distances2):
    fig = plt.figure()
    df_distances2["distance"].hist(bins=100)
    x = np.linspace(0,max_token,1000)
    mu = 0
    variance = np.var(df_distances2["distance"])
    sigma = np.sqrt(variance)
    #sigma=1000
    y = norm.pdf(x,mu,sigma)*600000
    plt.title("Frequency of different distances between character mentions \n in the story 'A case of identity'")
    plt.xlabel("Number of tokens (distance) between different character mentions")
    plt.ylabel("Frequency")
    plt.plot(x,y,"r")
    plt.show()
# %%