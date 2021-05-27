# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.stats as stats






def plot_hist(df_distances2):
    df_distances2["distance"].hist(bins=100)
    plt.show()


def plot_half_gaussian():
    plt.xlim((0,max_token))

    mean = 0
    variance = np.var(df_distances2["distance"])
    sigma = np.sqrt(variance)
    x = np.linspace(0,max_token,1000)
    plt.plot(x, mlab.normpdf(x,mean,sigma))

    plt.show()


def smooth_metric(distance, MU, SIGMA, DIST_PEAK):
    """
    # plot
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma) / stats.norm.pdf(0, mu, sigma))
    plt.show()

    #variance = 100
    #sigma = math.sqrt(variance)
    """
    return stats.norm.pdf(distance, MU, SIGMA) / DIST_PEAK


def generate_nodes_edges(df):

    #extract characters
    df_person = df[df["ner"]=="PERSON"].drop_duplicates(subset=COL_FOR_GRAPH)
    df_person = df_person.sort_values(by=COL_FOR_GRAPH, ascending=True)
    df_person = df_person.reset_index(drop=True).reset_index()

    #group by stories
    df_grouped = df[df["ner"]=="PERSON"].groupby(by="title",sort="False")
    stories = list(df['title'].unique())
    edges_frames = []
    
    for story_i, story_name in enumerate(stories):
        print(f"{story_i+1}/{len(stories)} - {story_name}")
        data = []
        df_story = df_grouped.get_group(story_name)
        positions = list(df_story["docTokenBegin"])
        max_token = max(positions)
        characters = list(df_story[COL_FOR_GRAPH])
        for i in range(len(positions)):
            for j in range(i+1,len(positions)):
                if (characters[i] != characters[j]):
                    dist = abs(positions[i]-positions[j])
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

        MU = 0
        SIGMA = df_dist_group.distance.median()
        #SIGMA = df_dist_group.distance.quantile(q=0.25)
        DIST_PEAK = stats.norm.pdf(0, MU, SIGMA)
        df_dist_group["distanceNorm"] = df_dist_group['distance'].apply(lambda x: smooth_metric(x, MU, SIGMA, DIST_PEAK))

        
        df_edges = df_dist_group.groupby(by="merged").agg({"distanceNorm": np.sum})
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

        edges_frames.append(df_edges)


    df_edges = pd.concat(edges_frames)

    return (df_person, df_edges)


if __name__ == "__main__":

    """
    nodes.csv -> index, label (, modularity)
    edges.csv -> id, source, target, type (undirected), weigth
    """


    COL_FOR_GRAPH = "clean_text_others" # clean_text, clean_text_others
    REMOVE_OTHERS = True

    file = os.path.join('..', 'w_questions', 'output_parsed', 'ner', '_merged_.csv')
    df = pd.read_csv(file)
    df = df.drop("nerConfidences", axis=1)

    df_person, df_edges = generate_nodes_edges(df)


    # export
    if REMOVE_OTHERS and COL_FOR_GRAPH == "clean_text_others":
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

# Analyse distibution of norm distance
import seaborn as sns
sns.histplot(df_edges.distanceNorm)


"""
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
"""
# %%
