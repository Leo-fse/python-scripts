import pandas as pd 
import numpy as np
from collections import defaultdict
import pprint

df = pd.read_csv("test.csv")
df.head()

def createDict(df):
    '''
    { unitcode1: [{part1 : [code1, code2, code3]},
                  {part2 : [code4, code5]}
                  ],
      unitcode2: [{part1 : [code1, code2, code3]},
                  {part2 : [code4, code5]},
                  ], 
    }
    '''
    grouped = df.groupby(by=["unitcode","parts"])
    unitcodeParts = defaultdict(list)
    for u in df["unitcode"].unique():
        #unitcode毎に部品種別とGコードのdictを初期化    
        partsGcode = defaultdict(list)
        for p in df[df["unitcode"]==u]["parts"].unique():
            gcode = sorted(list(set(grouped.get_group((u, p))["code"].values)))
            partsGcode[p] = gcode
        unitcodeParts[u] = partsGcode
    return unitcodeParts

def createDataFrame(data):
    df = pd.DataFrame()
    for u in data.keys():
        temp_df = pd.DataFrame()
        for p in data[u].keys():
            parts_df = pd.DataFrame(columns=[p],data=data[u][p])
            temp_df = parts_df.copy() if temp_df.empty \
                else pd.merge(temp_df, parts_df, left_index=True, right_index=True, how="outer")
        temp_df["unitcode"] = [u]*len(temp_df)
        temp_df.set_index("unitcode", inplace=True)
        df = pd.concat([df, temp_df])
    return df

data = createDict(df)

createDataFrame(data)