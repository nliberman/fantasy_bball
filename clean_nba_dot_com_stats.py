import pandas as pd
import numpy as np
import sys

f = sys.argv[1]
csv = "stats19_post_break.csv"

def clean_txt_file(f, csv):
    with open(f) as f1:
        lines = f1.readlines()

    df = []
    counter = 1
    for enum, line in enumerate(lines[1:], start=1):
        if counter==2:
            name = line.strip() + "\\"
        if counter==3:
            line = line.split()
            line = [int(enum/3), name, "pos", "age", "Tm", line[2], "GS",line[5],"FG",line[8], line[9],line[10],"3PA","3P%","2P","2PA","2P%","eFG%","FT",line[14],line[15], "ORB", "DRB", line[18], line[19], line[21], line[22], "TOV", "PF", line[6]]
            df.append(line)
            counter = 0
        counter +=1


    cols = ["Rk","Player","Pos","Age","Tm","G","GS","MP","FG","FGA","FG%","3P","3PA","3P%","2P","2PA","2P%","eFG%","FT","FTA","FT%","ORB","DRB","TRB","AST","STL","BLK","TOV","PF","PTS"]
    df = pd.DataFrame(df, columns=cols)
    print(df.head())
    df.to_csv(csv, index=False)

clean_txt_file(f, csv)
