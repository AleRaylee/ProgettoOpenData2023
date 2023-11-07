import pandas as pd
from frictionless import validate
from frictionless import Resource
fortezze_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\fortezze.csv"

torri_costiere_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\torri.csv"
castelli_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\castelli.csv"
comuni_csv= "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\Elenco-comuni-italiani.csv"
#castelli = pd.read_csv(castelli_csv,sep = ";")
#print(castelli.head(10))



# Path to your CSV file

'''
# Validate the data
report_fortezze= validate(fortezze_csv)
print(report_fortezze)
# Check if there are any errors

report_torri = validate(torri_costiere_csv)
print(report_torri)
'''
with Resource(torri_costiere_csv, encoding='utf-8') as resource:
  print(resource.encoding)
  print(resource.path)

with Resource(fortezze_csv, encoding='utf-8') as resource:
  print(resource.encoding)
  print(resource.path)

with Resource(castelli_csv, encoding='utf-8') as resource:
  print(resource.encoding)
  print(resource.path)

with Resource(comuni_csv, encoding='utf-8') as resource:
  print(resource.encoding)
  print(resource.path)

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


comuni = pd.read_csv(comuni_csv,sep =",")
#print(comuni.columns)
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

fortezze["Provincia"] = fortezze["Provincia"].replace("Pa","PA")
castelli["Prov"] = castelli["Prov"].replace("Pa","PA")
torri_costiere["Provincia"] = torri_costiere["Provincia"].replace("Pa","PA")
comuni["Provincia"]= comuni["Provincia"].replace("Pa","PA")

castelli.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\dataset_csv\\castelli.csv", index=False)
fortezze.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\dataset_csv\\fortezze.csv", index=False)
torri_costiere.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\dataset_csv\\torri.csv",index=False,)
comuni.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\dataset_csv\\comuni.csv", index=False)