import csv
import urllib.parse
import math
import pandas as pd
import requests
from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, OWL, XSD
from SPARQLWrapper import SPARQLWrapper, JSON


g = Graph()
ts = Namespace('http://www.turismosicilia.org/ontology/')
base_uri = "http://www.turismosicilia.org/resource/"
g.bind("ts",ts)

castelli_csv =r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\castelli.csv"
comuni_csv=r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\comuni.csv"
fortezze_csv = r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\fortezze.csv"
torri_csv = r"C:\Users\harub\Documents\GitHub\ProgettoOpenData2023\dataset_finali\dataset_csv\torri.csv"

comuni_df = pd.read_csv(comuni_csv)
castelli_df = pd.read_csv(castelli_csv)
fortezze_df = pd.read_csv(fortezze_csv)
torri_df = pd.read_csv(torri_csv)

def urify(base, name):
    name = name.replace(" ", "_").replace(".", "")
    return base + urllib.parse.quote(name)
def interlinkDbpediaComune(comune_uri, nome):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setTimeout(10000)
    query = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX dbr: <http://dbpedia.org/resource/>
            SELECT ?label ?link
            WHERE {{
              ?comune a dbo:Settlement ;
                      dbo:region dbr:Sicily ;
                      rdfs:label ?label ;
                      owl:sameAs ?link .
              FILTER(LANG(?label) = "it") .
            }}
        """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    bindings = results["results"]["bindings"]
def add_comuni(row):
    comune_uri = URIRef(urify(base_uri, row['Comune']))
    g.add((comune_uri, URIRef(RDF.type), URIRef(ts.Comuni)))
    g.add((comune_uri, ts.haNome, Literal(row['Comune'], datatype=XSD.string)))
    g.add((comune_uri, ts.haSiglaProvincia, Literal(row['Provincia'], datatype=XSD.string)))
    g.add((comune_uri, ts.haCodiceIstat, Literal(row['Codice_Istat'], datatype=XSD.string)))
    interlinkDbpediaComune(comune_uri, row['Comune'])

def add_castelli(row):
    for_comune = URIRef(urify(base_uri, row['Comune']))
    castello_uri = URIRef(urify(base_uri, row['Denominazione']))
    g.add((castello_uri, URIRef(RDF.type), URIRef(ts.Castelli)))
    g.add((castello_uri, ts.haDenominazione, Literal(row['Denominazione'], datatype=XSD.string)))
    g.add((castello_uri, ts.haProvincia, Literal(row['Prov'], datatype=XSD.string)))
    g.add((castello_uri, ts.haCronologia, Literal(row['Cronologia'], datatype=XSD.string)))
    g.add((castello_uri, ts.haGestoreT, Literal(row['Prop_att'], datatype=XSD.string)))
    g.add((castello_uri, ts.haUso, Literal(row['Uso_att'], datatype=XSD.string)))
    g.add((castello_uri, ts.haSitoWeb, Literal(row['Web_link'], datatype=XSD.anyURI)))
    g.add((castello_uri, ts.haImmagine, Literal(row['Image_link'], datatype=XSD.anyURI)))
    g.add((castello_uri, ts.haNote, Literal(row['Note_1'], datatype=XSD.string)))
    g.add((castello_uri, ts.haLongitudine, Literal(row['longitude'], datatype=XSD.double)))
    g.add((castello_uri, ts.haLatitudine, Literal(row['latitude'], datatype=XSD.double)))
    g.add((castello_uri, ts.haComune, Literal(row['Comune'], datatype=XSD.string)))
    g.add((for_comune, ts.haNome, Literal(row['Comune'], datatype=XSD.string)))
    g.add((castello_uri, ts.isIn, for_comune))

def add_fortezze(row):
    for_comune = URIRef(urify(base_uri, row['Comune']))
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
    g.add((fortezza_uri, ts.haComune, Literal(row['Comune'], datatype=XSD.string)))
    g.add((for_comune, ts.haNome, Literal(row['Comune'], datatype=XSD.string)))
    g.add((fortezza_uri, ts.isIn, for_comune))

def add_torri(row):
    for_comune = URIRef(urify(base_uri, row['Comune']))
    torre_uri = URIRef(urify(base_uri, row['Denominazione']))
    g.add((torre_uri, URIRef(RDF.type), URIRef(ts.TorriCostiere)))
    g.add((torre_uri, ts.haDenominazione, Literal(row['Denominazione'], datatype=XSD.string)))
    g.add((torre_uri, ts.haTipo, Literal(row['Tipo'], datatype=XSD.string)))
    g.add((torre_uri, ts.haGestoreT, Literal(row['Amstor'], datatype=XSD.string)))
    g.add((torre_uri, ts.haNote, Literal(row['Note2'], datatype=XSD.string)))
    g.add((torre_uri, ts.haLocazioneStorica, Literal(row['Loc_stor'], datatype=XSD.string)))
    g.add((torre_uri, ts.haSitoWeb, Literal(row['Foto_web'], datatype=XSD.anyURI)))
    g.add((torre_uri, ts.haConservazione, Literal(row['Consit'], datatype=XSD.string)))
    g.add((torre_uri, ts.haStatoProprietario, Literal(row['Proat'], datatype=XSD.string)))
    g.add((torre_uri, ts.haIconaTorri, Literal(row['Ico_torri'], datatype=XSD.anyURI)))
    g.add((torre_uri, ts.haLocalita, Literal(row['Localita'], datatype=XSD.string)))
    g.add((torre_uri, ts.haLatitudine, Literal(row['latitude'], datatype=XSD.double)))
    g.add((torre_uri, ts.haLongitudine, Literal(row['longitude'], datatype=XSD.double)))
    g.add((torre_uri, ts.haLonge, Literal(row['Longe'], datatype=XSD.double)))
    g.add((torre_uri, ts.haProvincia, Literal(row['Provincia'],datatype=XSD.string)))
    g.add((torre_uri, ts.haComune, Literal(row['Comune'], datatype=XSD.string)))
    g.add((for_comune, ts.haNome, Literal(row['Comune'], datatype=XSD.string)))
    g.add((torre_uri, ts.isIn, for_comune))

# Apply the functions to the respective DataFrames

comuni_df['Comune'] = comuni_df['Comune'].astype(str)
comuni_df.apply(add_comuni, axis=1)

castelli_df['Denominazione'] = castelli_df['Denominazione'].astype(str)
castelli_df['Note_1'] = castelli_df['Note_1'].astype(str)
castelli_df.apply(add_castelli, axis=1)

#fortezze_df['Denominazione'] = fortezze_df['Denominazione'].astype(str)
fortezze_df['note_'] = fortezze_df['note_'].astype(str)
fortezze_df.apply(add_fortezze, axis=1)

torri_df['Denominazione'] = torri_df['Denominazione'].astype(str)
torri_df['Note2'] = torri_df['Note2'].astype(str)
torri_df.apply(add_torri, axis=1)

g.serialize(destination="C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_completi\\datasetFinale_ttl.ttl",format= 'turtle')
g.serialize(destination="C:\\Users\\harub\\Documents\\GitHub\\ProgettoOpenData2023\\dataset_completi\\datasetFinale_XML.xml", format="xml")
