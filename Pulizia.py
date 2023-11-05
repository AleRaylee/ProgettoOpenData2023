import pandas as pd

fortezze_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\forti_fortezze.csv"
strutture_ricettive_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\mappa-delle-strutture-ricettive.csv"
torri_costiere_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\torri-costiere.csv"
castelli_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\castelli.csv"
comuni_csv= "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\Elenco-comuni-italiani.csv"
#castelli = pd.read_csv(castelli_csv,sep = ";")
#print(castelli.head(10))
def capitalize_column_name(column_name):
    if column_name not in ['longitude', 'latitude','PRO_COM_T']:
        return column_name.capitalize()
    return column_name

def elimina_colonne(lista,dataframe):
    df = pd.read_csv(dataframe, sep=",")
    df.drop(columns=lista,inplace=True)
    return df



castelli_eliminare = ["Id","TIPO","SOTTO_TIPO","OBJECTID_1","OBJECTID","cons","data_caricamento"]

fortezze_eliminare = ["OBJECTID","Id","OBJECTID_1","data_caricamento"]

fortezze = elimina_colonne(fortezze_eliminare,fortezze_csv)

torri_eliminare = ["ID","OBJECTID","RIFMAZ","NUM","CONS","OBJECTID_12","OBJECTID_1","data_caricamento"]

torri_costiere = elimina_colonne(torri_eliminare,torri_costiere_csv)

castelli = elimina_colonne(castelli_eliminare,castelli_csv)

castelli.rename(columns={'DENOMINAZI':'DENOMINAZIONE'},inplace= True)
fortezze.rename(columns={'Denom':'Denominazione'},inplace= True)
torri_costiere.rename(columns={'DENOM':'Denominazione'},inplace= True)

lista_colonne_c = castelli.columns.tolist()
lista_colonne_t = torri_costiere.columns.tolist()
castelli = castelli.rename(columns={col: capitalize_column_name(col) for col in lista_colonne_c})
torri_costiere = torri_costiere.rename(columns={col: capitalize_column_name(col) for col in lista_colonne_t})

strutture_ricettive = pd.read_csv(strutture_ricettive_csv,sep=';',encoding='ISO-8859-1')
strutture_ricettive = strutture_ricettive.drop(['Regione'],axis=1)


comuni = pd.read_csv(comuni_csv,sep =",")
print(comuni.columns)
#Prendo solo i comuni appartenenti alla regione Sicilia che ha codice regione 19
comuni = comuni[comuni['Codice Regione'] == 19]

# Seleziona solo le colonne desiderate
columns_to_keep = ['Denominazione in italiano', 'Sigla automobilistica', 'Codice Comune formato numerico']
comuni = comuni[columns_to_keep]
comuni.rename(columns={'Denominazione in italiano':'Comune'},inplace= True)
comuni.rename(columns={'Sigla automobilistica':'Provincia'},inplace= True)
comuni.rename(columns={'Codice Comune formato numerico':'Codice_Istat'},inplace= True)

fortezze = fortezze.merge(comuni, left_on='PRO_COM_T', right_on='Codice_Istat', how='left')
fortezze = fortezze.drop(['Codice_Istat'],axis=1)
'''
print(castelli.head(10))
print(fortezze.head(10))
print(torri_costiere.head(10))
print(strutture_ricettive.head(10))
print(castelli.head(10))
print(castelli.columns)
print(comuni)
'''
castelli.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\dataset_csv\\castelli.csv", index=False)
fortezze.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\dataset_csv\\forti_fortezze.csv", index=False)
torri_costiere.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\dataset_csv\\torri-costiere.csv", index=False)
strutture_ricettive.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\dataset_csv\\strutture_ricettive.csv", index=False)
comuni.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\dataset_csv\\comuni.csv", index=False)