import pandas as pd

fortezze_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\forti-fortezze.csv"
strutture_ricettive_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\mappa-delle-strutture-ricettive.csv"
torri_costiere_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\torri-costiere.csv"
castelli_csv = "C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset\\castelli.csv"

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





print(castelli.head(10))
print(castelli.columns)

'''
print(castelli.head(10))
print(fortezze.head(10))
print(torri_costiere.head(10))
'''
castelli.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\castelli.csv", index=False)
fortezze.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\forti-fortezze.csv", index=False)
torri_costiere.to_csv("C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_finali\\torri-costiere.csv", index=False)

