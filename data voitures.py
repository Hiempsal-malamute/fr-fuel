import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

data_init = pd.read_csv('Donnees-sur-le-parc-de-vehicule-au-niveau-communal.2023-05.csv',sep=";",skiprows=1)

data_init.head()
data_init.columns

data_init["CATEGORIE_VEHICULE"].unique()
data_init["CARBURANT"].unique()

voitures = data_init.loc[data_init["CATEGORIE_VEHICULE"]=='Véhicule particulier']

voitures.columns
voitures.head(1)

# part des véhicules roulant à l'assence, au diesel, à l'électrique par commune
nb_par_carburant = voitures.pivot_table(index="COMMUNE_CODE",columns=["CARBURANT"],values="PARC_2022", aggfunc='sum').fillna(0)
nb_par_carburant.columns

nb_par_carburant["part_essence"] = nb_par_carburant["Essence"] / nb_par_carburant.iloc[:, 0:7].sum(axis=1) * 100
nb_par_carburant["part_diesel"] = nb_par_carburant["Diesel"] / nb_par_carburant.iloc[:, 0:7].sum(axis=1) * 100
nb_par_carburant["part_electrique"] = (nb_par_carburant["Electrique et hydrogène"]) / nb_par_carburant.iloc[:, 0:7].sum(axis=1) * 100
nb_par_carburant.head(2)

nb_par_carburant["carburant_dominant"] = np.where(nb_par_carburant["part_essence"] == nb_par_carburant["part_diesel"], "same",
                                                 np.where(nb_par_carburant["part_essence"] > nb_par_carburant["part_diesel"], "essence", "diesel"))

nb_par_carburant["carburant_dominant"].unique()

nb_par_carburant.to_csv("voitures_carburant_communes.csv")

# évolution parc auto essence
def calcul_tx_croissance_carburant(carburant):
    print(carburant)
    df = voitures.loc[voitures["CARBURANT"] == carburant][["COMMUNE_CODE","PARC_2011","PARC_2022"]].sort_values(by="COMMUNE_CODE").fillna(0)
    df = df.groupby("COMMUNE_CODE").sum().fillna(0)
    df["evo_11_22"] = ((df["PARC_2022"] - df["PARC_2011"]) /  df["PARC_2011"]) *100
    return df   

evo_parc_essence = calcul_tx_croissance_carburant("Essence")
evo_parc_diesel = calcul_tx_croissance_carburant("Diesel")
evo_parc_hybride = calcul_tx_croissance_carburant("Hybride rechargeable")
evo_parc_electrique = calcul_tx_croissance_carburant("Electrique et hydrogène")
evo_parc_essence.head()
evo_parc_diesel.head()

evo_parc_essence.to_csv("evo_essence.csv")
evo_parc_diesel.to_csv("evo_diesel.csv")
evo_parc_hybride.to_csv("evo_hybride.csv")
evo_parc_electrique.to_csv("evo_electrique.csv")