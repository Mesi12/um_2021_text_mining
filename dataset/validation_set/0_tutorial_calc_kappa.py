import pandas as pd
import random
import re

"""
kappa distance
-   measures the distance of different judges' opinions on the
    relevance of documents to a query.
-   κ = (P(A) − P(E))/(1 − P(E))

"""

def calculation_trial_binary():
#%%

    # example from book
    # 0 not relevant
    # 1 relevant

    df_bad = pd.DataFrame(
        data=[
            [1, 0, 0],
            [2, 0, 0],
            [3, 1, 1],
            [4, 1, 1],
            [5, 1, 0],
            [6, 1, 0],
            [7, 1, 0],
            [8, 1, 0],
            [9, 0, 1],
            [10, 0, 1],
            [11, 0, 1],
            [12, 0, 1],
            ],
        columns=["doc", "judge1", "judge2"])

    df_good = pd.DataFrame(
        data=[
            [1, 0, 0],
            [2, 0, 0],
            [3, 1, 1],
            [4, 1, 1],
            [5, 0, 0],
            [6, 0, 0],
            [7, 1, 1],
            [8, 1, 0],
            [9, 0, 1],
            [10, 1, 1],
            [11, 1, 1],
            [12, 1, 1],
            ],
        columns=["doc", "judge1", "judge2"])
    
    df = df_good
    print(df)

    # Observed proportion of the times the judges agreed
    p_a = sum(df.judge1 == df.judge2) / df.shape[0]

    # Pooled marginals
    p_0 = (sum(df.judge1 == 0) + sum(df.judge2 == 0)) / (2*df.shape[0])
    p_1 = (sum(df.judge1 == 1) + sum(df.judge2 == 1)) / (2*df.shape[0])

    # Probability that the two judges agreed by chance
    p_e = p_0**2 + p_1**2

    # Kappa statistic
    k = (p_a - p_e) / (1 - p_e)

    print(f"agreed: {p_a:.2f}, by chance {p_e:.2f}")
    print(f"kappa: {k:.2f}")
#%%

def calculation_trial_multiclass():
#%%
    import pandas as pd

    # example from book
    # 0 not relevant
    # 1 relevant

    df = pd.DataFrame(
        data=[
            [1, 0, 0],
            [2, 0, 0],
            [3, 1, 1],
            [4, 1, 1],
            [5, 1, 0],
            [6, 1, 0],
            [7, 1, 0],
            [8, 1, 0],
            [9, 0, 1],
            [10, 0, 1],
            [11, 0, 1],
            [12, 0, 2],
            ],
        columns=["doc", "judge1", "judge2"])
    
    print(df)

    # Observed proportion of the times the judges agreed
    p_a = sum(df.judge1 == df.judge2) / df.shape[0]

    # Pooled marginals
    p_0 = (sum(df.judge1 == 0) + sum(df.judge2 == 0)) / (2*df.shape[0])
    p_1 = (sum(df.judge1 == 1) + sum(df.judge2 == 1)) / (2*df.shape[0])
    p_2 = (sum(df.judge1 == 2) + sum(df.judge2 == 2)) / (2*df.shape[0])

    # Probability that the two judges agreed by chance
    p_e = p_0**2 + p_1**2 + p_2**2

    # Kappa statistic
    k = (p_a - p_e) / (1 - p_e)

    print(k)


# %%

# tutorial from:
# https://towardsdatascience.com/multi-class-metrics-made-simple-the-kappa-score-aka-cohens-kappa-coefficient-bdea137af09c

from sklearn.metrics import confusion_matrix, cohen_kappa_score
import pandas as pd
import numpy as np


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
    print(k_measure)
    print(f"For comparison with cohen sklearn: {cohen_kappa_score(df_characters.judge1, df_characters.judge2):.4f}")
    return k_measure

df_ex = pd.read_csv("tmp_example.csv")
calculate_kappa(df_ex.professor_a, df_ex.professor_b)
print(f"cohen sklearn: {cohen_kappa_score(df_ex.professor_a, df_ex.professor_b)}")

