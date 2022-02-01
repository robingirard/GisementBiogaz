import numpy as np
from numpy.core.fromnumeric import prod
from numpy.lib.shape_base import column_stack
import pandas as pd 

crop_list=["Ble.tendre","Ble.dur","Triticale","Mais.grain","Mais.ensilage","Orge","Avoin","Sorgho","Seigle","Betterave","Pomme.de.terre","Tournesol","Colza","Soja"]
special_crop_list=["Pois","Orge.d.hiver.et.escourgeon","Orge.de.printemps","Pois.proteagineux"]

# tauxres=pd.DataFrame(index=["IR","AB","TOT"],columns=crop_list+special_crop_list)
tauxres=pd.read_csv("./ress/tauxres.csv",index_col=0)
print(tauxres)
for c in tauxres.columns:
    ir=tauxres.at["IR",c]
    tauxres.at["TOT",c]= ((1-ir) * tauxres.at["AB",c])/ir
tauxres.to_csv("./ress/tauxres.csv")