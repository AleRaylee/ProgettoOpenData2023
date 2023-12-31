import pandas as pd

castelli_csv =r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\castelli.csv"
comuni_csv=r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\comuni.csv"
fortezze_csv = r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\fortezze.csv"
torri_csv = r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\torri.csv"

#Conteggio di castelli, fortezze e torri_costiere per provincia

castelli = pd.read_csv(castelli_csv,sep=",")
forti = pd.read_csv(fortezze_csv,sep=",")
torri = pd.read_csv(torri_csv,sep=",",encoding="utf-8")

colonne_interesse_castelli = ['Denominazione', 'Prov', 'Comune','PRO_COM_T']
colonne_interesse_forti = ['Denominazione', 'Provincia', 'Comune','PRO_COM_T']
colonne_interesse_torri = ['Denominazione', 'Provincia', 'Comune','PRO_COM_T']

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


print(monumenti_df)
monumenti_per_comune = monumenti_df.groupby(['Comune', 'Tipologia']).size().reset_index(name='Conteggio')
print(monumenti_per_comune)
totale_per_comune = monumenti_per_comune.groupby('Comune')['Conteggio'].sum().reset_index(name='Totale')
totale_per_comune = totale_per_comune.sort_values(by='Totale', ascending=False)




top10 = totale_per_comune.head(10)
citta = top10['Comune'].to_list()
print(type(citta))
top10_citta = monumenti_per_comune[monumenti_per_comune['Comune'].isin(citta)]

pivot_df = top10_citta.pivot(index='Comune', columns='Tipologia', values='Conteggio').fillna(0)
pivot_df.reset_index(inplace=True)
pivot_df.to_csv('C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\Grafici\\conteggio_monumenti_citta_dettaglio.csv', index=False)
top10.to_csv('C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\Grafici\\conteggio_monumenti_citta.csv', index=False)
conteggio_monumenti.to_csv('C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\Grafici\\conteggio_monumenti.csv', index=False)