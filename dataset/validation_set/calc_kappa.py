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
