from ast import Raise
import logging
import sys
from pybtex.database import parse_file, parse_bytes
from pybtex.database.input.bibtex import UndefinedMacro, DuplicateField

from RDFWriter import RDFWriter

error_string = "Unexpected error: {0}"
class BibtexParser:
    def __init__(self) -> None:
        self.bibdata = None
        self.writer = None
        

    def parse_file(self, filename: str = None, file: bytes = None) -> tuple[bool, str]:
        try:
            if filename is not None:
                self.bibdata = parse_file(filename, 'bibtex')
            elif file is not None:
                self.bibdata = parse_bytes(file, 'bibtex')
            else:
                return False, "No file provided"
            self.writer = RDFWriter()
            return True, "File parsed successfully"
        except UndefinedMacro as e:
            logging.error('Undefined Macro: {0}'.format(e))
            return False, 'Undefined Macro: {0}'.format(e)
        except DuplicateField as e:
            logging.error('Duplicate field: {0}'.format(e))
            return False, 'Duplicate field: {0}'.format(e)
        except Exception as e:
            logging.error(error_string.format(e))
            return False, error_string.format(e)

    def convert_file(self) -> tuple[bool, str]:
        try: 
            for key in self.bibdata.entries.keys():
                item = self.bibdata.entries[key]
                item_type = self.extract_type(item)
                fields = self.extract_fields(item)
                authors = self.extract_persons(item)
                self.writer.write_entry(key, item_type, authors, fields)
        except Exception as e:
            logging.error(error_string.format(e))
            return False, error_string.format(e)
        return True, "File converted successfully"

    def save_rdf(self) -> tuple[bool, str]:
        try:
            self.writer.save_graph()
        except Exception as e:
            logging.error(error_string.format(e))
            return False, error_string.format(e)
        return True, "RDF saved successfully"
        

    def extract_type(self, entry):
        return entry.type

    def extract_fields(self, entry):
        return entry.fields.items()
    
    def extract_richtext(self, entry):
        return [name.render_as('text') for name in entry]

    def extract_fullname(self, person):
        return ', '.join(filter(None, [
        ' '.join(self.extract_richtext(person.rich_first_names)),
        ' '.join(self.extract_richtext(person.rich_middle_names)),
        ' '.join(self.extract_richtext(person.rich_prelast_names)),
        ' '.join(self.extract_richtext(person.rich_last_names)),
        ' '.join(self.extract_richtext(person.rich_lineage_names)),
        ]))

    def extract_persons(self, entry):
        authors = []
        for persons in entry.persons:
            for person in entry.persons[persons]:
                author = self.extract_fullname(person)
                authors.append(author)
        return ' and '.join(authors)