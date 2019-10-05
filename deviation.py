import pandas as pd
from scipy.stats import median_absolute_deviation
from sklearn.preprocessing import StandardScaler
import numpy as np
import sys

csv = sys.argv[1]
num_teams = int(sys.argv[2])
bench_players_valued = 1
budget = 160 - (4 - bench_players_valued)

def clean_df(csv, keep_players):
    df = pd.read_csv(csv)
    df['Player'] = df.Player.apply(lambda x: x.split("\\")[0])
    df = df[['Rk','Player','Tm','G','MP','FGA','FG%', '3P','FTA','FT%','TRB','AST','STL','BLK','PTS']]
    dupes = list(df[df.duplicated(subset=["Rk"], keep="first")].Rk)

    keep_rows = []
    for rk in dupes:
        temp = list(df[(df.Rk == rk) & (df.Tm=="TOT")].values[0])
        keep_rows.append(temp)
    temp = pd.DataFrame(keep_rows, columns=['Rk','Player','Tm','G','MP','FGA','FG%', '3P','FTA','FT%','TRB','AST','STL','BLK','PTS'])

    df = df.append(temp)
    df = df.drop_duplicates(subset=["Rk"], keep="last")
    df = df[df.MP > 10]
    if len(keep_players) != 0:
        df = df[df.Rk.isin(keep_players)]
    df = df.dropna()
    return df


def get_average_deviation(column):
    n = float(len(column))
    mu = np.mean(column)
    devs = []
    for x in column:
        devs.append(abs(mu - x))
    return sum(devs) / (n-1)


def fit_avg_dev(x, mu, ad):
    return (x - mu) / ad


def quantify_value(df, num_teams):
    non_pcts = ['3P','TRB','AST','STL','BLK','PTS']
    pcts = ['FG%', 'FT%']
    pct_multiples = ['FGA', 'FTA']

    for cat in non_pcts:
        ad = get_average_deviation(list(df[cat]))
        mu = np.mean(df[cat])
        df[cat] = df[cat].apply(lambda x: fit_avg_dev(x, mu, ad))

    for pct, multiple in zip(pcts, pct_multiples):
        print("pct col: ", pct)
        ad = get_average_deviation(list(df[pct]))
        mu = np.mean(df[pct])
        print("mu: ", mu)
        print("ad: ", ad)
        df[pct] = df[pct].apply(lambda x: fit_avg_dev(x, mu, ad))
        df[pct] = df[pct] * df[multiple]
        ad = get_average_deviation(list(df[pct]))
        mu = np.mean(df[pct])
        df[pct] = df[pct].apply(lambda x: fit_avg_dev(x, mu, ad))

    df["value"] = df['3P'] + df['TRB'] + df['AST'] + df['STL'] + df['BLK'] + df['PTS'] + df['FG%'] + df['FT%']
    shift = np.min(df.value)
    if shift > 0:
        shift = 0
    else:
        shift = abs(shift) + 0.1
    print("shift: ", shift)
    df["value"] = df.value + shift
    df = df.sort_values("value", ascending=False).reset_index().drop(["index"], axis=1)
    return df


def get_dollar_value(df, num_teams, budget):
    total_dollars = float(num_teams * budget)
    total_value = float(df.value.sum())
    df['dollar'] = df.value.apply(lambda x: round(x / total_value * total_dollars, 2))
    return df



## return df of all players
df = clean_df(csv, [])
df = quantify_value(df, num_teams)
if num_teams >= 14:
    num_players = 10 + bench_players_valued
else:
    num_players = 11 + bench_players_valued
total_starters_drafted = num_teams * num_players
df = df[df.index < total_starters_drafted] 

## Rerun valuation considering only starters
df = clean_df(csv, list(df.Rk))
print("len df: ", len(df))
df = quantify_value(df, num_teams)
df = get_dollar_value(df, num_teams, budget)
df = df[['Player','dollar','value','G','MP','PTS','FG%','FT%','3P','TRB','AST','STL','BLK',]]
df.to_csv("output.csv")
print(df.head(20))
print(df.tail(20))
print(df.value.sum())
print("total dollars: ", num_teams*budget)
print("FG: ", df["FG%"].sum())
print("FT: ", df["FT%"].sum())
print("total std value: ", df.value.sum())
