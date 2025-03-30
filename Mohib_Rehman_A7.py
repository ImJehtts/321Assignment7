import pandas as pd

#Set-up table with all values and renaming
url = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"

tables = pd.read_html(url)

df = tables[3]
df = df.iloc[:, [0, 1, 3]].copy()
df.columns = ["Year", "Winners", "Runners-up"]
df.loc[:, "Winners"] = df["Winners"].replace({"West Germany": "Germany"})
df.loc[:, "Runners-up"] = df["Runners-up"].replace({"West Germany": "Germany"})
df.to_csv("world_cup_winners.csv", index=False)
#Done Set-up
print(df.head())



