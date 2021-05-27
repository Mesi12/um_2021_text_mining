#%%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab



#%%

# all stories
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




#%%
#df_distances2["distance"].hist(bins=100)
#plt.show()

#%%


#%%


def plot_half_gaussian():
    plt.xlim((0,max_token))

    mean = 0
    variance = np.var(df_distances2["distance"])
    sigma = np.sqrt(variance)
    x = np.linspace(0,max_token,1000)
    plt.plot(x,mlab.normpdf(x,mean,sigma))

    plt.show()



# %%




if __name__ == "__main__":

    """
    nodes.csv -> index, label (, modularity)
    edges.csv -> id, source, target, type (undirected), weigth
    """

    COL_FOR_GRAPH = "clean_text_others" # clean_text, clean_text_others
    REMOVE_OTHERS = True

    file = os.path.join('..', 'w_questions', 'output_parsed', 'ner', '_merged_.csv')
    df = pd.read_csv(file)

    #extract characters
    df_person = df[df["ner"]=="PERSON"].drop_duplicates(subset=COL_FOR_GRAPH)
    df_person = df_person.sort_values(by=COL_FOR_GRAPH, ascending=True)
    df_person = df_person.reset_index(drop=True).reset_index()

    #group by stories
    df_grouped = df[df["ner"]=="PERSON"].groupby(by="title",sort="False")
    data = []
    story_name= "the_hound_of_the_baskervilles"
    df_story = df_grouped.get_group(story_name)
    position = list(df_story["docTokenBegin"])
    max_token = max(position)
    characters = list(df_story[COL_FOR_GRAPH])
    for i in range(len(position)):
        for j in range(i+1,len(position)):
            if (characters[i] != characters[j]):
                dist = abs(position[i]-position[j])
                data.append([characters[i],characters[j],dist,story_name,max_token])
    df_distances2 = pd.DataFrame(data, columns = ["character1", "character2","distance","story","max_token"])

    #merge first two columns of df_distances2
    a = df_distances2["character1"]
    b = df_distances2["character2"]
    merged = []
    for i in range(len(a)):
        merged.append((" | ".join(sorted([a[i],b[i]]))))
    merged
    df_distances2["merged"] = merged


    df_dist_group = df_distances2.groupby(["story","merged"]).agg({"distance": "sum"})
    df_dist_group = df_dist_group.reset_index()

    df_dist_group["distanceNorm"] = df_dist_group['distance'] / max_token

    
    df_edges = df_dist_group.groupby(by="merged").agg({"distanceNorm": np.mean})
    df_edges = df_edges.reset_index()
    df_edges[['source_name', 'target_name']] = pd.DataFrame(
        df_edges['merged'].str.split('|').tolist(),
        columns = ['source_name','target_name'])
    df_edges['source_name'] = df_edges['source_name'].str.strip()
    df_edges['target_name'] = df_edges['target_name'].str.strip()

    df_edges = df_edges.merge(
        df_person[['index', COL_FOR_GRAPH]],
        left_on="source_name",
        right_on=COL_FOR_GRAPH)
    df_edges = df_edges.rename(columns={"index": "source"}).drop(COL_FOR_GRAPH, axis=1)

    df_edges = df_edges.merge(
        df_person[['index', COL_FOR_GRAPH]],
        left_on="target_name",
        right_on=COL_FOR_GRAPH)
    df_edges = df_edges.rename(columns={"index": "target"}).drop(COL_FOR_GRAPH, axis=1)



    # export
    if REMOVE_OTHERS:
        index_other = df_person[df_person[COL_FOR_GRAPH].str.lower() == "other"].iloc[0]['index']
        print(f"removing 'other' with index: {index_other}")
        df_person = df_person[df_person[COL_FOR_GRAPH].str.lower() != "other"]
        df_edges = df_edges[(df_edges["source"] != index_other) & (df_edges["target"] != index_other)]
    # nodes
    df_person[['index',COL_FOR_GRAPH]].to_csv("nodes.csv", index=False)
    # edges
    df_edges = df_edges.reset_index()
    df_edges[['index', 'source', 'target', 'distanceNorm']].to_csv(
        "edges.csv", index=False
    )

    print("done")





# %%
