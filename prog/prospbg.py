import numpy as np
from numpy.core.fromnumeric import prod
from numpy.lib.shape_base import column_stack
import pandas as pd 
import geopandas as gpd

##### Introduction

bg=pd.DataFrame()
ent=pd.read_csv("./biogaz/potcantonsale.csv",header=13,index_col=2,encoding="latin_1")
ent=ent[:-4]
ent=ent.drop(columns=["Canton","Nom.de.canton","Intitule"])
ent=ent.fillna(0)
ent=ent.replace({',': '.'}, regex=True)

##### 2010

## Surface 2010

surf_list=["Surf.2010.Ble.tendre","Surf.2010.Ble.dur","Surf.2010.Triticale","Surf.2010.Mais.grain","Surf.2010.Mais.ensilage","Surf.2010.Orge","Surf.2010.Avoin","Surf.2010.Sorgho","Surf.2010.Seigle","Surf.2010.Betterave","Surf.2010.Pomme.de.terre","Surf.2010.Tournesol","Surf.2010.Colza","Surf.2010.Soja"]
surf2010df = ent[surf_list].copy()

## Rendements 2010

rend_list=["Rend.2010.Ble.tendre","Rend.2010.Ble.dur","Rend.2010.Triticale","Rend.2010.Mais.grain","Rend.2010.Mais.ensilage","Rend.2010.Orge","Rend.2010.Avoin","Rend.2010.Sorgho","Rend.2010.Seigle","Rend.2010.Betterave","Rend.2010.Pomme.de.terre","Rend.2010.Tournesol","Rend.2010.Colza","Rend.2010.Soja"]
rend2010df = ent[rend_list].copy()
rend2010df=rend2010df.astype("float64")

## Production 2010 

prod_list=[]
for i in range(len(rend_list)):
    prod_list.append("Prod"+rend_list[i][4:])
prod2010df=pd.DataFrame(index=ent.index)

for i in range(len(rend_list)):
    mul=surf2010df.join(rend2010df)
    prod2010df[prod_list[i]]= mul[surf_list[i]] * mul[rend_list[i]]

##### 2050

### Evolutions 

## Surface

evolus_list=[]
for i in range(len(rend_list)):
    evolus_list.append("Evolu.rend."+rend_list[i][10:])
evolusdf = ent[evolus_list].copy()

## Rendements

evolur_list=[]
for i in range(len(rend_list)):
    evolur_list.append("Evolu.surf."+rend_list[i][10:])
evolurdf = ent[evolur_list].copy()
