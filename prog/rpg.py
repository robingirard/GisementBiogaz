import folium
import branca
import geopandas as gpd
import pandas  as pd
import matplotlib
import matplotlib.pyplot as plt

fp = "./doc/GISData/RPG_2-0_SHP_LAMB93_R28_2020/PARCELLES_GRAPHIQUES.shp"
data = gpd.read_file(fp)
fp = "./doc/GISData/contour-des-departements.geojson"
dep = gpd.read_file(fp)

grilleRPGdf=pd.DataFrame(index=data["CODE_CULTU"].unique(),columns=["SBSTCROP"])
grilleRPGdf["SBSTCROP"]="0"
BD=["BDH","BDP","BDT"]
for l in BD:
    grilleRPGdf.at[l,"SBSTCROP"]="Ble.dur"
BT=["BTH","BTP"]
for l in BT:
    grilleRPGdf.at[l,"SBSTCROP"]="Ble.tendre"
M=["MIS","MID"]
for l in M:
    grilleRPGdf.at[l,"SBSTCROP"]="Mais.grain"
ME=["MIE"]
for l in ME:
    grilleRPGdf.at[l,"SBSTCROP"]="Mais.ensilage"
A=["AVH","AVP","CHA","CPA"]
for l in A:
    grilleRPGdf.at[l,"SBSTCROP"]="Avoin"
S=["CHS","CPS","SGH","SGP"]
for l in S:
    grilleRPGdf.at[l,"SBSTCROP"]="Seigle"
SO=["CGO","SOG"]
for l in SO:
    grilleRPGdf.at[l,"SBSTCROP"]="Sorgho"
T=["CHT","CPT","TTH","TTP"]
for l in T:
    grilleRPGdf.at[l,"SBSTCROP"]="Triticale"
C=["CZH","CZP"]
for l in C:
    grilleRPGdf.at[l,"SBSTCROP"]="Colza"
TOUR=["TRN"]
for l in TOUR:
    grilleRPGdf.at[l,"SBSTCROP"]="Tournesol"
SOJ=["SOJ"]
for l in SOJ:
    grilleRPGdf.at[l,"SBSTCROP"]="Soja"
POI=["PPO","PHI","PPR","PPT"]
for l in POI:
    grilleRPGdf.at[l,"SBSTCROP"]="Pois"
PPR=["FEV","FVL","FVT","MPC","MPP","PAG"]
for l in PPR:
    grilleRPGdf.at[l,"SBSTCROP"]="Pois.proteagineux"
PDT=["PTC","PTF","TOP"]
for l in PDT:
    grilleRPGdf.at[l,"SBSTCROP"]="Pomme.de.terre"
BET=["BTN","BVF"]
for l in BET:
    grilleRPGdf.at[l,"SBSTCROP"]="Betterave"
grilleRPGdf.at["ORH","SBSTCROP"]="Orge.hiver"
grilleRPGdf.at["ORP","SBSTCROP"]="Orge.de.printemps"
grilleRPGdf.at[l,"SBSTCROP"]="Betterave"
grilleRPGdf.to_csv("./ress/grilleRPGdf.csv")

for i in data.index:
    data.at[i,"CULT"]=grilleRPGdf.at[data.at[i,"CODE_CULTU"],"SBSTCROP"]

renddf=pd.read_csv("./ress/rend.csv",index_col=[0],header=[0,1],encoding="latin_1")
special_crop_list=["Pois","Pois.proteagineux"]
for i in data.index:
    c=data.at[i,"CULT"]
    if c=="Orge.de.printemps" or c=="Orge.hiver":
        data.at[i,"PROD"]=data.at[i,"SURF_PARC"]*(renddf.at["01",("Orge","2010")]/10)
    elif c in special_crop_list:
        data.at[i,"PROD"]=data.at[i,"SURF_PARC"]*(45/100)
    elif c!="0" and c not in special_crop_list:
        data.at[i,"PROD"]=data.at[i,"SURF_PARC"]*(renddf.at["01",(c,"2010")]/10)
    else :
        data.at[i,"PROD"]=0

cropCIMSEhiver=["Orge.de.printemps","Ble.tendre","Sorgho","Pois","Betterave","Mais.grain","Mais.ensilage","Soja","Pomme.de.terre"]
cropCIMSEete=["Orge.hiver"]
rendCIMSEdf=pd.read_csv("./ress/rendcimse.csv",index_col=[0],header=[0,1,2],encoding="latin_1")
for i in data.index:
    if data.at[i,"CULT"]in cropCIMSEete:
        data.at[i,"ProdCIMSE"]=data.at[i,"SURF_PARC"]*rendCIMSEdf.at["72",("RdRecolte","Ete","2010")]
    elif data.at[i,"CULT"]in cropCIMSEhiver:
        data.at[i,"ProdCIMSE"]=data.at[i,"SURF_PARC"]*rendCIMSEdf.at["72",("RdRecolte","Hiver","2010")]
    else :
        data.at[i,"ProdCIMSE"]=0

tauxresdf=pd.read_csv("./ress/tauxres.csv",index_col=[0],header=[0],encoding="latin_1")
for i in data.index:
    c=data.at[i,"CULT"]
    if c!="0":
        if c == "Orge.hiver":
            data.at[i,"RESIDUS"]=data.at[i,"PROD"]*tauxresdf.at["TOT","Orge.d.hiver.et.escourgeon"]
        else :
            data.at[i,"RESIDUS"]=data.at[i,"PROD"]*tauxresdf.at["TOT",c]
    else:
        data.at[i,"RESIDUS"]=0

methdf=pd.read_csv("./ress/methanogene.csv",index_col=[0],header=[0],encoding="latin_1")
cbg=11.04

for i in data.index:
    c=data.at[i,"CULT"]
    if c!="0":
        if c== "Orge.hiver":
            data.at[i,"PRODBG"]=(data.at[i,"RESIDUS"]*methdf.at["PM","Orge.d.hiver.et.escourgeon"]+data.at[i,"ProdCIMSE"]*methdf.at["PM","CIMSE"])*cbg
        else:
            data.at[i,"PRODBG"]=(data.at[i,"RESIDUS"]*methdf.at["PM",c]+data.at[i,"ProdCIMSE"]*methdf.at["PM","CIMSE"])*cbg
    else:
        data.at[i,"PRODBG"]=0

data.plot('PRODBG', legend=True,figsize=(12,8))
plt.title('Production de biogaz')


data.explore()




