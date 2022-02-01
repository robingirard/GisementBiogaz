from email import header
from operator import index
import numpy as np
from numpy.core.fromnumeric import prod
from numpy.lib.shape_base import column_stack
import pandas as pd 

##Production de CIMSE 

crop_list=["Ble.tendre","Ble.dur","Triticale","Mais.grain","Mais.ensilage","Orge","Avoin","Seigle","Betterave","Pomme.de.terre","Sorgho","Colza","Soja"]
special_crop_list=["Pois","Orge.d.hiver.et.escourgeon","Orge.de.printemps","Pois.proteagineux"]

cropCIMSEete2010=["Orge.d.hiver.et.escourgeon"]
cropCIMSEete2050=["Orge.d.hiver.et.escourgeon","Colza","Ble.tendre","Triticale","Orge","Avoin","Seigle"]

cropCIMSEhiver=["Orge.de.printemps","Ble.tendre","Sorgho","Pois","Betterave","Mais.grain","Mais.ensilage","Soja","Pomme.de.terre"]

surfdf=pd.read_csv("./ress/prod.csv",index_col=[0],header=[0,1],encoding="latin_1")
surfdf.index=surfdf.index.astype("string")
iterables = [["CIMSE.ete","CIMSE.hiver"],["2010","2050"]]
mI=pd.MultiIndex.from_product(iterables, names=["Season", "Year"])

surfCIMSEdf=pd.DataFrame(index=surfdf.index,columns=mI)

for s in iterables[0]:
    for y in iterables[1]:
        if s=="CIMSE.ete" :
            if y=="2010":
                i=[(c,y) for c in cropCIMSEete2010]
                surfCIMSEdf[(s,y)]=surfdf[i].sum(axis=1)
            else:
                i=[(c,y) for c in cropCIMSEete2050]
                surfCIMSEdf[(s,y)]=surfdf[i].sum(axis=1)
        else:
            i=[(c,y) for c in cropCIMSEhiver]
            surfCIMSEdf[(s,y)]=surfdf[i].sum(axis=1)

prodCIMSEdf=pd.DataFrame(index=surfdf.index,columns=mI)
rendcimse=pd.read_csv("./ress/rendcimse.csv",index_col=[0],header=[0,1,2],encoding="latin_1")

for s in ["Ete","Hiver"]:
    for y in iterables[1]:
        s_="CIMSE."+s.lower()
        prodCIMSEdf[(s_,y)]=surfCIMSEdf[(s_,y)]*rendcimse[("RdRecolte",s,y)]

## Résidus de culture

proddf=pd.read_csv("./ress/prod.csv",index_col=0,header=[0,1],encoding="latin_1")
tauxres=pd.read_csv("./ress/tauxres.csv",index_col=0,encoding="latin_1")
iterables = [crop_list+special_crop_list,["2010","2050"]]
mI=pd.MultiIndex.from_product(iterables, names=["Residue from", "Year"])
prodresdf=pd.DataFrame(index=proddf.index,columns=mI)
for c in crop_list+special_crop_list:
    for y in ["2010","2050"]:
        prodresdf[(c,y)]=proddf[(c,y)]*tauxres.at["TOT",c]

##Biogaz 

cbg=11.04 ##Capacité calorifique en kWh/m^3

prodbgdf=pd.DataFrame(index=proddf.index,columns=["2010","2050"])
methdf=pd.read_csv("./ress/methanogene.csv",index_col=0,encoding="latin_1")

for c in crop_list+special_crop_list:
    for y in ["2010","2050"]:
        prodresdf[(c,y)]=(prodresdf[(c,y)]*methdf.at["PM",c])
for c in ["CIMSE.ete","CIMSE.hiver"]:
    for y in ["2010","2050"]:
        prodCIMSEdf[(c,y)]=(prodCIMSEdf[(c,y)]*methdf.at["PM","CIMSE"])
for y in ["2010","2050"]:
    i=[(c,y) for c in crop_list+special_crop_list]
    i_=[(c,y) for c in ["CIMSE.ete","CIMSE.hiver"]]
    prodbgdf[y]=cbg*((prodresdf[i]).sum(axis=1)+prodCIMSEdf[i_].sum(axis=1))

prodbgdf.to_csv("./ress/prodbg.csv")