from argparse import Namespace
import keyword
from rdflib import RDF, Graph, Literal, Namespace
from HttpMessage import PROPERTY_NOT_FOUND

from namespaceAssociation import get_property
from utils import extract_keywords


class RDFWriter:
    def __init__(self):
        self.graph = Graph()
        self.namespace = Namespace('https://zeitkunst.org/bibtex/0.2/bibtex.owl#')
        self.graph.bind('bibtex', self.namespace)

    def write_entry(self, entry_id, type, authors, fields):
        errors = []
        keywords = []
        entry_id = Literal(entry_id)
        self.graph.add((entry_id, RDF.type, self.namespace[type]))
        self.graph.add((entry_id, self.namespace.hasAuthor, Literal(authors)))
        for key, value in fields:
            success, prt, has_to_be_yaked = get_property(key)
            if has_to_be_yaked:
                keywords.extend(extract_keywords(value))
            if prt == 'hasKeywords':
                keywords.append(value)
                continue
            if not success:
                errors.append(PROPERTY_NOT_FOUND.format(prt))
            self.graph.add((entry_id, self.namespace[prt], Literal(value)))
        if keywords:
            self.graph.add((entry_id, self.namespace.hasKeywords, Literal(', '.join(keywords))))
        return errors

    def print_graph(self):
        print(self.namespace['Article'])
        print('\n')
        print(self.graph.serialize(format='pretty-xml'))
        
    def save_graph(self):
        self.graph.serialize(destination='rdfOut/lib.rdf', format='pretty-xml')