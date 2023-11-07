import pandas as pd

castelli_csv =r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\castelli.csv"
comuni_csv=r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\comuni.csv"
fortezze_csv = r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\fortezze.csv"
torri_csv = r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\torri.csv"

#Conteggio di castelli, fortezze e torri_costiere per provincia

castelli = pd.read_csv(castelli_csv,sep=",")
forti = pd.read_csv(fortezze_csv,sep=",")
torri = pd.read_csv(torri_csv,sep=",")

colonne_interesse_castelli = ['Denominazione', 'Prov', 'Comune']
colonne_interesse_forti = ['Denominazione', 'Provincia', 'Comune']
colonne_interesse_torri = ['Denominazione', 'Provincia', 'Comune']

castelli_selezionati = castelli[colonne_interesse_castelli]
castelli_selezionati.rename(columns={'Prov': 'Provincia'}, inplace=True)
forti_selezionati = forti[colonne_interesse_forti]
torri_selezionati = torri[colonne_interesse_torri]

castelli_selezionati['Tipologia'] = 'Castelli'
forti_selezionati['Tipologia'] = 'Forti'
torri_selezionati['Tipologia'] = 'Torri_Costiere'

# Concatena i tre dataset in un unico dataset
monumenti_df = pd.concat([castelli_selezionati, forti_selezionati, torri_selezionati], ignore_index=True)


conteggio_monumenti = monumenti_df.groupby(['Provincia', 'Tipologia']).size().reset_index(name='Conteggio')

print(monumenti_df.columns)
conteggio_monumenti = conteggio_monumenti.pivot(index='Provincia', columns='Tipologia', values='Conteggio').reset_index()
conteggio_monumenti.columns.name = None  # Rimuove il nome delle colonne
print(conteggio_monumenti)

conteggio_monumenti.to_csv('C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\Grafici\\conteggio_monumenti.csv', index=False)