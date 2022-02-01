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

## Rendements

rend2010_list=[]
for i in range(len(crop_list)):
    rend2010_list.append("Rend.2010."+crop_list[i])
renddf = ent[rend2010_list].copy()
renddf=renddf.astype("float64")

evolu=pd.read_csv("./ress/evolucrop.csv",index_col=[0],header=[0,1],encoding="latin_1")

for c in crop_list:
    renddf["Rend.2050."+c]=0
    for i in renddf.index:
        renddf.loc[i,"Rend.2050."+c]= renddf.loc[i,"Rend.2010."+c] * evolu.loc[ent.loc[i,"Nom.de.region"],(c,"Evolu.rend")]

newcolumns=[]
for c in crop_list:
    newcolumns.append("Rend.2010."+c)
    newcolumns.append("Rend.2050."+c)
renddf=renddf.reindex(columns=newcolumns)

iterables = [crop_list,["2010","2050"]]
mI=pd.MultiIndex.from_product(iterables, names=["Crop", "Year"])
renddf.columns = mI

renddf.to_csv("./ress/rend.csv")