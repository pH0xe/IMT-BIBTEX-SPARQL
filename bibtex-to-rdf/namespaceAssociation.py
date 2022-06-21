import logging

from HttpMessage import PROPERTY_NOT_FOUND

properties = {
    'abstract': ('hasAbstract', True),
    'address': ('hasAddress', False),
    'affiliation': ('hasAffiliation', False),
    'annote': ('hasAnnotation', True),
    'author': ('hasAuthor', False),
    'booktitle': ('hasBooktitle', False),
    'book': ('hasBooktitle', False),
    'chapter': ('hasChapter', False),
    'content': ('hasContents', False),
    'contents': ('hasContents', False),
    'copyright': ('hasCopyright', False),
    'copyrights': ('hasCopyright', False),
    'crossref': ('hasCrossref', False),
    'edition': ('hasEdition', False),
    'editors': ('hasEditor', False),
    'institution': ('hasInstitution', False),
    'isbn': ('hasISBN', False),
    'issn': ('hasISSN', False),
    'journal': ('hasJournal', False),
    'key': ('hasKey', False),
    'keywords': ('hasKeywords', False),
    'keyword': ('hasKeywords', False),
    'language': ('hasLanguage', False),
    'lccn': ('hasLCCN', False),
    'location': ('hasLocation', False),
    'month': ('hasMonth', False),
    'mrnumber': ('hasMrnumber', False),
    'note': ('hasNote', True),
    'notes': ('hasNote', True),
    'number': ('hasNumber', False),
    'organization': ('hasOrganization', False),
    'pages': ('hasPages', False),
    'numpages': ('hasPages', False),
    'price': ('hasPrice', False),
    'publisher': ('hasPublisher', False),
    'school': ('hasSchool', False),
    'series': ('hasSeries', False),
    'size': ('hasSize', False),
    'title': ('hasTitle', True),
    'type': ('hasType', False),
    'url': ('hasURL', False),
    'volume': ('hasVolume', False),
    'year': ('hasYear', False),
    'howpublished': ('howPublished', False),
    'pagechapterdata': ('pageChapterData', False),
    # Illegal not in definition
    'folder': ('hasFolder', False),
    'doiurl': ('hasDoiURL', False),
    'doi': ('hasDoiURL', False),
    'localurl': ('hasLocalURL', False),
    'localurl2': ('hasLocalURL2', False),
    'filing': ('hasFiling', False),
    'comment': ('hasComment', True),
    'comments': ('hasComment', True),
    'eprint': ('hasEprint', False),
    'issue_date': ('hasIssueDate', False),
    'acmid': ('hasACMID', False),
    'opttype': ('hasOptType', False),
    'optkey': ('hasOptKey', False),
    'optnumber': ('hasOptNumber', False),
    'optaddress': ('hasOptAddress', False),
    'optmonth': ('hasOptMonth', False),
    'optnote': ('hasOptNote', False),
    'optannote': ('hasOptAnnotation', False),
    'articleno': ('hasArticleNo', False),
    'url2': ('hasURL2', False),
    'oldurl': ('hasOldURL', False),
    'day': ('hasDay', False),
    'source': ('hasSource', False),
    'bibsource': ('hasSource', False),
    'urlpdf': ('hasURLPDF', False),
    'urlinfo': ('hasURLInfo', False),
    'urlspringer': ('hasURLSpringer', False),
}

logger = logging.getLogger('bibtexToRDF')

def get_property(name) -> tuple[bool, str, bool]:
    name = name.lower()
    try:
        proper, hasToBeYaked = properties[name]
        return True, proper, hasToBeYaked
    except KeyError:
        logger.warning(PROPERTY_NOT_FOUND.format(name))
        return False, f"has{name[0].upper()}{name[1:]}", False