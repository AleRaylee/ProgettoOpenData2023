import pandas as pd
import pyproj
#Definizione di una funzione che prendendo a parametro un file csv pulisce i file castelli
#e forti e fortezze dato che hanno caratterstiche simili


fortezze_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_originali\\fortifortezze_csv_rsd.csv"
strutture_ricettive_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_originali\\mappa-delle-strutture-ricettive.csv"
torri_costiere_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_originali\\torri-costiere_csv_rsd.csv"
musei_parchi_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_originali\\musei-gallerie-siti-archeologici_csv_rsd.csv"
castelli_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_originali\\castelli.csv"

#castelli = pd.read_csv(castelli_csv,sep = ";")
#print(castelli.head(10))

def elimina_colonne(lista,dataframe):
    df = pd.read_csv(dataframe, sep=",")
    df.drop(columns=lista,inplace=True)
    return df

castelli_eliminare = ["Id","TIPO","OBJECTID_1","OBJECTID","cons","data_caricamento"]

'''
fortezze_eliminare = ["OBJECTID","Id","OBJECTID_1","data_caricamento"]
fortezze = elimina_colonne(fortezze_eliminare,fortezze_csv)

torri_eliminare = ["ID","OBJECTID","RIFMAZ","NUM","OBJECTID_12","OBJECTID_1","data_caricamento"]
torri_costiere = elimina_colonne(torri_eliminare,torri_costiere_csv)
'''
castelli = elimina_colonne(castelli_eliminare,castelli_csv)
castelli.rename(columns={'SOTTO_TIPO':'Tipologia'},inplace= True)
castelli.rename(columns={'DENOMINAZI':'Denominazione'},inplace= True)
castelli['Tipologia'] = "castello";
print(castelli.head(10))
print(castelli.columns)

'''
print(castelli.head(10))
print(fortezze.head(10))
print(torri_costiere.head(10))
'''


