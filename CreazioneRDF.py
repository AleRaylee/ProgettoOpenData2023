import csv
import urllib.parse
import math
import pandas as pd
import requests
from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, OWL, XSD
from SPARQLWrapper import SPARQLWrapper, JSON
import codecs

g = Graph();
ts = Namespace('http://www.turismosicilia.org/ontology/')
base_uri = "http://www.turismosicilia.org/resource/"
g.bind("ts",ts)

castelli_csv =r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\castelli.csv"
comuni_csv=r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\comuni.csv"
fortezze_csv = r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\forti_fortezze.csv"
torri_csv = r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\torri-costiere.csv"

def urify(base, name):
    name = name.replace(" ", "_").replace(".", "")
    return base + urllib.parse.quote(name)


def add_Comuni():
    with open(comuni_csv) as comuni:
        reader = csv.DictReader(comuni)
        for row in reader:
            comune_uri = URIRef(urify(base_uri,row['Comune']))
            g.add((comune_uri, URIRef(RDF.type), URIRef(ts.Comuni)))
            g.add((comune_uri, ts.haNome, Literal(row['Comune'], datatype=XSD.string)))
            g.add((comune_uri, ts.haSiglaProvincia, Literal(row['Provincia'], datatype=XSD.string)))
            g.add((comune_uri, ts.haCodiceIstat, Literal(row['Codice_Istat'], datatype=XSD.string)))

            #Interlink con dbPedia
            dbpedia_url = "http://dbpedia.org/resource/" + str(row['Comune']).title().replace(" ","_").replace("' ","'_")
            t = requests.get(dbpedia_url)

            if (t.status_code == 200):
                g.add([URIRef(comune_uri), ts.comune, URIRef(dbpedia_url)])
            else:
                print(row['Comune'] + " --- " + dbpedia_url)
                g.add([URIRef(comune_uri), ts.comune, Literal(row['Comune'])])


def add_castelli():
    with open(castelli_csv) as castelli:
        reader = csv.DictReader(castelli)
        for row in reader:
            for_comune = URIRef(urify(base_uri, row['Comune']))
            castello_uri = URIRef(urify(base_uri, row['Denominazione']))
            g.add((castello_uri, URIRef(RDF.type), URIRef(ts.Castelli)))
            g.add((castello_uri, ts.haDenominazione, Literal(row['Denominazione'], datatype=XSD.string)))
            g.add((castello_uri, ts.haProvincia, Literal(row['Prov'], datatype=XSD.string)))
            g.add((castello_uri, ts.haCronologia, Literal(row['Cronologia'], datatype=XSD.string)))
            g.add((castello_uri, ts.haGestoreT, Literal(row['Prop_att'], datatype=XSD.string)))
            g.add((castello_uri, ts.haUso, Literal(row['Uso_att'], datatype=XSD.string)))
            g.add((castello_uri, ts.haSitoWeb, Literal(row['Web_link'], datatype=XSD.anyURI)))
            g.add((castello_uri, ts.haIconaTorri, Literal(row['Image_ico'], datatype=XSD.anyURI)))
            g.add((castello_uri, ts.haImmagine, Literal(row['Image_link'], datatype=XSD.anyURI)))
            g.add((castello_uri, ts.haNote, Literal(row['Note_1'], datatype=XSD.string)))
            g.add((castello_uri, ts.haLongitudine, Literal(row['longitude'], datatype=XSD.double)))
            g.add((castello_uri, ts.haLatitudine, Literal(row['latitude'], datatype=XSD.double)))
            g.add((for_comune, ts.haNome, Literal(row['Comune'], datatype=XSD.string)))
            g.add((castello_uri, ts.isIn, for_comune))


def add_fortezze():
    with open(fortezze_csv) as fortezze:
        reader = csv.DictReader(fortezze)
        for row in reader:
            for_comune = URIRef(urify(base_uri,row['Comune']))
            fortezza_uri = URIRef(urify(base_uri, row['Denominazione']))
            g.add((fortezza_uri, URIRef(RDF.type), URIRef(ts.Fortezze)))
            g.add((fortezza_uri, ts.haDenominazione, Literal(row['Denominazione'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.haCronologiaF, Literal(row['Cronologia'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.haS_L_M, Literal(row['s_l_m_'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.haUbicazione, Literal(row['Ubicazione'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.haStatoConservazione, Literal(row['Stato_Cons'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.haGestore, Literal(row['Gestore'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.haIconaTorri, Literal(row['ico_image'], datatype=XSD.anyURI)))
            g.add((fortezza_uri, ts.haUso, Literal(row['Uso'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.haSitoWeb, Literal(row['weblink'], datatype=XSD.anyURI)))
            g.add((fortezza_uri, ts.haTipologia, Literal(row['Tipologia'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.haNote, Literal(row['note_'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.haLongitudine, Literal(row['longitude'], datatype=XSD.double)))
            g.add((fortezza_uri, ts.haLatitudine, Literal(row['latitude'], datatype=XSD.double)))
            g.add((fortezza_uri, ts.haProvincia, Literal(row['Provincia'], datatype=XSD.string)))
            g.add((for_comune, ts.haNome, Literal(row['Comune'], datatype=XSD.string)))
            g.add((fortezza_uri, ts.isIn, for_comune))


def add_torri():
    with open(torri_csv) as torri:
        reader = csv.DictReader(torri)
        for row in reader:
            for_comune = URIRef(urify(base_uri, row['Comune']))
            torre_uri = URIRef(urify(base_uri, row['Denominazione']))
            g.add((torre_uri, URIRef(RDF.type), URIRef(ts.TorriCostiere)))
            g.add((torre_uri, ts.haDenominazione, Literal(row['Denominazione'], datatype=XSD.string)))
            g.add((torre_uri, ts.haTipo, Literal(row['Tipo'], datatype=XSD.string)))
            g.add((torre_uri,ts.haGestoreT,Literal(row['Amstor'],datatype=XSD.string)))
            g.add((torre_uri, ts.haNote2, Literal(row['Note2'], datatype=XSD.string)))
            g.add((torre_uri, ts.haLocazioneStorica, Literal(row['Loc_stor'], datatype=XSD.string)))
            g.add((torre_uri, ts.haSitoWeb, Literal(row['Foto_web'], datatype=XSD.anyURI)))
            g.add((torre_uri, ts.haConservazione, Literal(row['Consit'], datatype=XSD.string)))
            g.add((torre_uri, ts.haStatoProprietario, Literal(row['Proat'], datatype=XSD.string)))
            g.add((torre_uri, ts.haIconaTorri, Literal(row['Ico_torri'], datatype=XSD.anyURI)))
            g.add((torre_uri, ts.haLocalita, Literal(row['Localita'], datatype=XSD.string)))
            g.add((torre_uri, ts.haLatitudine, Literal(row['latitude'], datatype=XSD.double)))
            g.add((torre_uri, ts.haLongitudine, Literal(row['longitude'], datatype=XSD.double)))
            g.add((torre_uri, ts.haLonge, Literal(row['Longe'], datatype=XSD.double)))
            g.add((torre_uri,ts.haProvincia,Literal(row['Provincia'])))
            g.add((for_comune, ts.haNome, Literal(row['Comune'], datatype=XSD.string)))
            g.add((torre_uri, ts.isIn, for_comune))

add_Comuni()
add_castelli()
#add_torri()
add_fortezze()
g.serialize(destination='C:\\Users\\harub\\Desktop\\prove\\Dataset_rdf.ttl', format='turtle')
'''
#Funziona me devo cambiare il collegamento
output_file = 'C:\\Users\\harub\\Desktop\\prove\\Dataset_prova_codificato.ttl'
rdf_data = g.serialize(format='turtle', encoding='utf-8')
# Salva il file con l'encoding Latin-1
with codecs.open(output_file, 'w', 'latin-1') as file:
    file.write(rdf_data)
'''
