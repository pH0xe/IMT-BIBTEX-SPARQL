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
    def writeEntry(self, id, type, authors, fields):
        id = Literal(id)
        self.graph.add((id, RDF.type, self.namespace[type]))
        self.graph.add((id, self.namespace.hasAuthor, Literal(authors)))
        for key, value in fields:
            self.graph.add((id, self.namespace[getProperty(key)], Literal(value)))
        # self.graph.add((Literal(id), Literal('https://zeitkunst.org/bibtex/0.2/bibtex.owl/Article'), Literal(type)))
    
    def printGraph(self):
        print(self.namespace['Article'])
        print('\n')
        print(self.graph.serialize(format='pretty-xml'))
    def saveGraph(self):
        self.graph.serialize(destination='rdfOut/lib.rdf', format='pretty-xml')