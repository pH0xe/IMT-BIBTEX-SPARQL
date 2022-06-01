import logging
import sys
from pybtex.database import parse_file
from pybtex.database.input.bibtex import UndefinedMacro, DuplicateField

from RDFWriter import RDFWriter


class BibtexParser:
    def __init__(self, filename) -> None:
        try:
            self.bibdata = parse_file(filename)
            self.writer = RDFWriter()
        except UndefinedMacro as e:
            logging.error('Undefined Macro: {0}'.format(e))
            exit(-1)
        except DuplicateField as e:
            logging.error('Duplicate field: {0}'.format(e))
            exit(-1)
        except:
            logging.error("Unexpected error:", sys.exc_info()[0])
            exit(-1)

    def exploreFile(self):
        for key in self.bibdata.entries.keys():
            item = self.bibdata.entries[key]
            type = self.extract_type(item)
            fields = self.extract_fields(item)
            authors = self.extract_persons(item)
            self.writer.writeEntry(key, type, authors, fields)

    def writeRDF(self):
        self.writer.writeRDF()

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