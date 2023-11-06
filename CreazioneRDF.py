import csv
import urllib.parse
import pandas as pd
import math

import unicodedata
from unidecode import unidecode
import requests
from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, OWL, XSD
from SPARQLWrapper import SPARQLWrapper, JSON

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
            row['Comune'] = row['Comune'].replace("a'", "à").replace("o'", "ò").replace("e'", "è").replace("i'", "ì").replace("u'", "ù").title()
            comune_uri = URIRef(urify(base_uri,row['Comune']))
            row['Comune'] = row['Comune'].replace("a'", "à").replace("o'", "ò").replace("e'", "è").replace("i'",
                                                                                                           "ì").replace(
                "u'", "ù").title()
            g.add((comune_uri, URIRef(RDF.type), URIRef(ts.Comuni)))
            g.add((comune_uri, ts.haNome, Literal(row['Comune'], datatype=XSD.string)))
            g.add((comune_uri, ts.haSiglaProvincia, Literal(row['Provincia'], datatype=XSD.string)))
            g.add((comune_uri, ts.haCodiceIstat, Literal(row['Codice_Istat'], datatype=XSD.string)))

            #Interlink con dbPedia
            dbpedia_url = "http://dbpedia.org/resource/" + str(row['Comune']).title().replace(" ", "_")
            t = requests.get(dbpedia_url)

            dbpedia_url = "http://dbpedia.org/resource/" + str(row['Comune']).title().replace(" ", "_")
            r = requests.get(dbpedia_url)

            if (r.status_code == 200):
                g.add([URIRef(comune_uri), ts.comune, URIRef(dbpedia_url)])
            else:
                print(row['Comune'] + " --- " + dbpedia_url)
                g.add([URIRef(comune_uri), ts.comune, Literal(row['Comune'])])

add_Comuni()
g.serialize(destination='C:\\Users\\harub\\Desktop\\prove\\Dataset_rdf.ttl', format='turtle')