import logging
from pybtex.database import parse_file, parse_bytes
from pybtex.database.input.bibtex import UndefinedMacro, DuplicateField
from HttpMessage import DUPLICATED_FIELD, NO_FILE_SELECTED, SUCCESS_CONVERT, SUCCESS_PARSE, SUCCESS_SAVE, UNDEFINED_MACRO, UNEXPECTED_ERROR
from RDFWriter import RDFWriter



class BibtexParser:
    def __init__(self) -> None:
        self.bibdata = None
        self.writer = None
        self.logger = logging.getLogger("bibtexToRDF")


    def parse_file(self, filename: str = None, file: bytes = None) -> tuple[bool, str]:
        try:
            if filename is not None:
                self.bibdata = parse_file(filename, 'bibtex')
            elif file is not None:
                self.bibdata = parse_bytes(file, 'bibtex')
            else:
                return False, NO_FILE_SELECTED
            self.writer = RDFWriter()
            return True, SUCCESS_PARSE
        except UndefinedMacro as e:
            self.logger.error(UNDEFINED_MACRO.format(e))
            return False, UNDEFINED_MACRO.format(e)
        except DuplicateField as e:
            self.logger.error(DUPLICATED_FIELD.format(e))
            return False, DUPLICATED_FIELD.format(e)
        except Exception as e:
            self.logger.error(UNEXPECTED_ERROR.format(e))
            return False, UNEXPECTED_ERROR.format(e)

    def convert_file(self) -> tuple[bool, str, list[str]]:
        errors = []
        try:      
            for key in self.bibdata.entries.keys():
                item = self.bibdata.entries[key]
                item_type = self.extract_type(item)
                fields = self.extract_fields(item)
                authors = self.extract_persons(item)
                err = self.writer.write_entry(key.replace(':', '_').replace('-', '_'), item_type, authors, fields)
                errors.extend(err)
        except Exception as e:
            self.logger.error(UNEXPECTED_ERROR.format(e))
            return False, UNEXPECTED_ERROR.format(e), errors
        return True, SUCCESS_CONVERT, errors

    def save_rdf(self) -> tuple[bool, str, str]:
        try:
            graph_data = self.writer.save_graph()
        except Exception as e:
            self.logger.error(UNEXPECTED_ERROR.format(e))
            return False, UNEXPECTED_ERROR.format(e)
        return True, SUCCESS_SAVE, graph_data
        

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