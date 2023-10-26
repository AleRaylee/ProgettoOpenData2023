import pandas as pd

#Definizione di una funzione che prendendo a parametro un file csv pulisce i file castelli
#e forti e fortezze dato che hanno caratterstiche simili

castelli_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_originali\\castelli_csv_rsd.csv"
fortezze_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_originali\\fortifortezze_csv_rsd.csv"
strutture_ricettive = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_originali\\mappa-delle-strutture-ricettive.csv"
#castelli = pd.read_csv(castelli_csv,sep = ";")
#print(castelli.head(10))

def elimina_righe_c_f(dataframe):
    df = pd.read_csv(dataframe,sep = ";")
    df.drop(df.columns[[0,1]],axis =1, inplace= True)
    df.drop(columns = ['data_caricamento'],inplace = True)
    return df


castelli = elimina_righe_c_f(castelli_csv)
castelli.rename(columns={'SOTTO_TIPO':'Tipologia'},inplace= True)
castelli['Tipologia'] = "castello";

fortezze = elimina_righe_c_f(fortezze_csv)
fortezze.drop(columns = ["OBJECTID_1"],inplace = True)

print(fortezze.head(10))




