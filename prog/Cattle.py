import numpy as np
from numpy.core.fromnumeric import prod
from numpy.lib.shape_base import column_stack
import pandas as pd 

ent=pd.read_csv("./doc/potcantonsale.csv",header=13,index_col=2,encoding="latin_1")
ent=ent[:-4]
ent=ent.drop(columns=["Canton","Nom.de.canton","Intitule"])
ent=ent.fillna(0)
ent=ent.replace({',': '.'}, regex=True)

cattle_list=["Vaches_laitieres","Vaches.allaitantes","Brebis.meres.nourrices","Porcs","Poulets.de.chair","Poules.pondeuses"]
cattle_list_=["Vaches_laitieres","Vaches_allaitantes","Brebis_meres_nourrices","Porcs","Poulets de chair","Poules_pondeuses"]
cattle_listevolu=["Vaches_laitieres","Vaches_allaitantes","Brebis_meres_nourrices","Porcs","Poulets de chair","Poules pondeuses"]
year_list=["2010","2050"]

iterables = [cattle_list,["2010","2050"]]
mI=pd.MultiIndex.from_product(iterables, names=["Cattle", "Year"])
cattledf=pd.DataFrame(index=ent.index,columns=mI)

for i in range(len(cattle_list)):
    cattledf[(cattle_list[i],"2010")]=ent[cattle_list_[i]+"_2010"]

evoluc_list=[]
for i in range(len(cattle_list)):
    evoluc_list.append("Evolution.effectifs."+cattle_listevolu[i]+".2010-2050")

##### Vérifions que les évolutions sont définies au niveau départemental

# dep=ent["Nom.DPT"].unique()

# 1: Vérifions que les évolutions de surfaces sont déterminées au niveau départemental
# for c in cattle_list:
#     ent["Evolution.effectifs."+c+".2010-2050"]=ent["Evolution.effectifs."+c+".2010-2050"].astype("float64")
#     hyp=ent.groupby("Nom.DPT")["Evolution.effectifs."+c+".2010-2050"].std()
#     for d in dep:
#         if hyp[d] > 0.01:
#             print(f"Problème avec l'évolution du nombre de têtes de {c} dans le département, {d} avec une valeur de {hyp[d]}")

evolucdf=ent[evoluc_list].copy()
evolucdf=evolucdf.astype("float64")
evolucdf.columns=["Evolution.effectifs."+c for c in cattle_list]

for i in range (len(cattle_list)):
    cattledf[(cattle_list[i],"2050")]=cattledf[(cattle_list[i],"2010")]*evolucdf["Evolution.effectifs."+cattle_list[i]]

cattledf.to_csv("./ress/cattle.csv")
evolucdf.to_csv("./ress/evolucattle.csv")