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

evolus_list=[]
for i in range(len(crop_list)):
    evolus_list.append("Evolu.surf."+crop_list[i])

## Rendements

evolur_list=[]
for i in range(len(crop_list)):
    evolur_list.append("Evolu.rend."+crop_list[i])

##### Vérifions que les évolutions sont définies au niveau régional

reg=ent["Nom.de.region"].unique()

# 1: Vérifions que les évolutions de surfaces sont déterminées au niveau régonal
for c in crop_list:
    ent["Evolu.surf."+c]=ent["Evolu.surf."+c].astype("float64")
    hyp=ent.groupby("Nom.de.region")["Evolu.surf."+c].std()
    for r in reg:
        if hyp[r] > 0.01:
            print(f"Problème avec l'évolution de surface de récolte de {c} dans la région {r}, avec une valeur de {hyp[r]}")
#Ici problème au PACA, allons plus loin dans l'étude pour corriger plus tard
paca=ent[ent['Nom.de.region'] == "PROVENCE-ALPES-COTE-D'AZUR"]
print(paca["Evolu.surf.Soja"])
#On voit que le problème est dans le 13, sûrement à cause de l'étendue de Marseille, la différence n'est pas majeure, on la négligera

for c in crop_list:
    ent["Evolu.rend."+c]=ent["Evolu.rend."+c].astype("float64")
    hyp=ent.groupby("Nom.de.region")["Evolu.rend."+c].std()
    for r in reg:
        if hyp[r] > 0.01:
            print(f"Problème avec l'évolution du rendement de {c} dans la région {r}, avec une valeur de {hyp[r]}")
#Pb en IdF, on va regarder dans cet endroit
idf=ent[ent['Nom.de.region'] == "ILE-DE-FRANCE"]
print(idf[evolur_list])
#On voit que le problème se trouve en IdF, et plus précisément à Paris, qui n'a aucune culture
#Il n'y aura surement pas de problème car pas de parcelles à Paris mais au besoin on pourra régler le pb facilement

#2 Créer un tableau multi index pour pouvoir changer les valeurs dans le futur

evolu = ent[["Nom.de.region"]+evolus_list+evolur_list].copy()
evolu=evolu.groupby("Nom.de.region").max()
newcolumns=[]
for c in crop_list:
    newcolumns.append("Evolu.surf."+c)
    newcolumns.append("Evolu.rend."+c)
evolu=evolu.reindex(columns=newcolumns)
iterables = [crop_list,["Evolu.surf","Evolu.rend"]]
mI=pd.MultiIndex.from_product(iterables, names=["Crop", "Type"])
evolu.columns = mI
evolu.to_csv("./ress/evolucrop.csv")