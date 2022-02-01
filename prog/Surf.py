from email import header
import numpy as np
from numpy.core.fromnumeric import prod
from numpy.lib.shape_base import column_stack
import pandas as pd 

ent=pd.read_csv("./doc/potcantonsale.csv",header=13,index_col=2,encoding="latin_1")
ent=ent[:-4]
ent=ent.drop(columns=["Canton","Nom.de.canton","Intitule"])
ent=ent.fillna(0)
ent=ent.replace({',': '.'}, regex=True)

crop_list=["Ble.tendre","Ble.dur","Triticale","Mais.grain","Mais.ensilage","Orge","Avoin","Sorgho","Seigle","Betterave","Pomme.de.terre","Tournesol","Colza","Soja"]

## Surfaces

surf2010_list=[]
for i in range(len(crop_list)):
    surf2010_list.append("Surf.2010."+crop_list[i])
surfdf = ent[surf2010_list].copy()

print(ent["SAU 2010"]==ent[surf2010_list].sum(axis=1))

evolu=pd.read_csv("./ress/evolu.csv",index_col=[0],header=[0,1],encoding="latin_1")

for c in crop_list:
    surfdf["Surf.2050."+c]=0
    for i in surfdf.index:
        surfdf.loc[i,"Surf.2050."+c]= surfdf.loc[i,"Surf.2010."+c] * evolu.loc[ent.loc[i,"Nom.de.region"],(c,"Evolu.surf")]

newcolumns=[]
for c in crop_list:
    newcolumns.append("Surf.2010."+c)
    newcolumns.append("Surf.2050."+c)
surfdf=surfdf.reindex(columns=newcolumns)

iterables = [crop_list,["2010","2050"]]
mI=pd.MultiIndex.from_product(iterables, names=["Crop", "Year"])
surfdf.columns = mI

surfdf.to_csv("./ress/surf.csv")