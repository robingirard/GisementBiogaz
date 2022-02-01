import numpy as np
from numpy.core.fromnumeric import prod
from numpy.lib.shape_base import column_stack
import pandas as pd 
import geopandas as gpd


crop_list=["Ble.tendre","Ble.dur","Triticale","Mais.grain","Mais.ensilage","Orge","Avoin","Sorgho","Seigle","Betterave","Pomme.de.terre","Tournesol","Colza","Soja"]
special_crop_list=["Pois","Orge.d.hiver.et.escourgeon...2010","Orge.de.printemps...2010","Pois.proteagineux"]

ent=pd.read_csv("./doc/potcantonsale.csv",header=13,index_col=2,encoding="UTF-16")
ent=ent[:-4]
ent=ent.drop(columns=["Canton","Nom.de.canton","Intitule"])
ent=ent.fillna(0)
ent=ent.replace({',': '.'}, regex=True)

scl = ent[special_crop_list].copy()

surfdf=pd.read_csv("./ress/surf.csv",index_col=[0],header=[0,1],encoding="latin_1")
renddf=pd.read_csv("./ress/rend.csv",index_col=[0],header=[0,1],encoding="latin_1")

special_crop_list2=["Pois","Orge.d.hiver.et.escourgeon","Orge.de.printemps","Pois.proteagineux"]

iterables = [crop_list+special_crop_list2,["2010","2050"]]
mI=pd.MultiIndex.from_product(iterables, names=["Crop", "Year"])
proddf=pd.DataFrame(index=surfdf.index,columns=mI)

for c in crop_list:
    for y in ["2010","2050"]:
            proddf[(c,y)]= surfdf[(c,y)] * renddf[(c,y)]

for y in ["2010","2050"]:
    for i in range(len(special_crop_list)):
        proddf[(special_crop_list2[i],y)]=scl[special_crop_list[i]]

proddf.to_csv("./ress/prod.csv")

#Bien fait au niveau départemental, selon la doc 
