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

## CIMSE
type_list=["RdProduction","RdRecolte"]
season_list=["Ete","Hiver"]
year_list= ["2010","2050"]

iterables = [type_list,season_list,year_list]
mI=pd.MultiIndex.from_product(iterables, names=["Type","Season","Year"])
rendcimsedf=pd.DataFrame(index=ent.index,columns=mI)

for t in type_list:
    for s in season_list:
        for y in year_list:
            if s=="Ete" and t=="RdRecolte":
                rendcimsedf[(t,s,y)]=ent["Rendement.moyen.de."+t[2:].lower()+".tMS.ha."+s.lower()+"_"+y]
            else:
                rendcimsedf[(t,s,y)]=ent["Rendement.moyen.de."+t[2:].lower()+".tMS.ha."+s.lower()+"."+y]

print(rendcimsedf)

rendcimsedf.to_csv("./ress/rendcimse.csv")

## Résidus

