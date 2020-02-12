from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, XSD
import pandas as pd
import string
import random

nuig = Namespace("https://krr.triply.cc/nuig/")

def readCSV(inFile):
    """
    returns csv without headers
    """
    df  = pd.read_csv(inFile,  na_filter = False, header=0, encoding="latin-1" )
    return df

def clean_string(s):
    clean = ""
    for char in s:
        if char in string.punctuation or char == " " :
            clean = clean+'-'
        else : 
            clean = clean+char 
    return clean

tables = list(URIRef(nuig+"tables/T0%d" % i) for i in range(0,10))
rooms = list(URIRef(nuig+"rooms/R0%d" % i) for i in range(0,5))
positions = [URIRef(nuig+"locations/onTable"), URIRef(nuig+"locations/underTable")]

###
### need a graph of computers, located on/under a table, in a room 
### randomly assigns computers to tables (on/under), tables to rooms 
###
if __name__ == "__main__":
	
    computers = readCSV("random_devices.csv")
    g = Graph()
    
    # randomise tables 
    for t in tables : 
        g.add((t , URIRef(nuig+"locations/room") , random.choice(rooms)))
    
    for ix,pc in computers.iterrows(): 
        pc = URIRef(nuig+"device/"+clean_string(pc))
        g.add((pc , random.choice(positions), random.choice(tables)))
    
    g.serialize(destination="museum.nt" , format='nt')