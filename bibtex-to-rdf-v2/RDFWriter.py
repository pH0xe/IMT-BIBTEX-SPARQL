from argparse import Namespace
from rdflib import RDF, Graph, Literal, Namespace

from namespaceAssociation import getProperty


class RDFWriter:
    def __init__(self):
        self.graph = Graph()
        self.namespace = Namespace('https://zeitkunst.org/bibtex/0.2/bibtex.owl#')
        self.graph.bind('bibtex', self.namespace)

    # Chaque entrée correspond à une réference bibliographique. Elle contient les entrées suivantes :
    # -
    def write_entry(self, entry_id, type, authors, fields):
        entry_id = Literal(entry_id)
        self.graph.add((entry_id, RDF.type, self.namespace[type]))
        self.graph.add((entry_id, self.namespace.hasAuthor, Literal(authors)))
        for key, value in fields:
            self.graph.add((entry_id, self.namespace[getProperty(key)], Literal(value)))
        # self.graph.add((Literal(id), Literal('https://zeitkunst.org/bibtex/0.2/bibtex.owl/Article'), Literal(type)))
    
    def print_graph(self):
        print(self.namespace['Article'])
        print('\n')
        print(self.graph.serialize(format='pretty-xml'))
        
    def save_graph(self):
        self.graph.serialize(destination='rdfOut/lib.rdf', format='pretty-xml')