import logging

from HttpMessage import PROPERTY_NOT_FOUND

properties = {
    'abstract': 'hasAbstract',
    'address': 'hasAddress',
    'affiliation': 'hasAffiliation',
    'annote': 'hasAnnotation',
    'author': 'hasAuthor',
    'booktitle': 'hasBooktitle',
    'book': 'hasBooktitle',
    'chapter': 'hasChapter',
    'content': 'hasContents',
    'contents': 'hasContents',
    'copyright': 'hasCopyright',
    'copyrights': 'hasCopyright',
    'crossref': 'hasCrossref',
    'edition': 'hasEdition',
    'editors': 'hasEditor',
    'institution': 'hasInstitution',
    'isbn': 'hasISBN',
    'issn': 'hasISSN',
    'journal': 'hasJournal',
    'key': 'hasKey',
    'keywords': 'hasKeywords',
    'keyword': 'hasKeywords',
    'language': 'hasLanguage',
    'lccn': 'hasLCCN',
    'location': 'hasLocation',
    'month': 'hasMonth',
    'mrnumber': 'hasMrnumber',
    'note': 'hasNote',
    'notes': 'hasNote',
    'number': 'hasNumber',
    'organization': 'hasOrganization',
    'pages': 'hasPages',
    'numpages': 'hasPages',
    'price': 'hasPrice',
    'publisher': 'hasPublisher',
    'school': 'hasSchool',
    'series': 'hasSeries',
    'size': 'hasSize',
    'title': 'hasTitle',
    'type': 'hasType',
    'url': 'hasURL',
    'volume': 'hasVolume',
    'year': 'hasYear',
    'howpublished': 'howPublished',
    'pagechapterdata': 'pageChapterData',
    # Illegal not in definition
    'folder': 'hasFolder',
    'doiurl': 'hasDoiURL',
    'doi': 'hasDoiURL',
    'localurl': 'hasLocalURL',
    'localurl2': 'hasLocalURL2',
    'filing': 'hasFiling',
    'comment': 'hasComment',
    'comments': 'hasComment',
    'eprint': 'hasEprint',
    'issue_date': 'hasIssueDate',
    'acmid': 'hasACMID',
    'opttype': 'hasOptType',
    'optkey': 'hasOptKey',
    'optnumber': 'hasOptNumber',
    'optaddress': 'hasOptAddress',
    'optmonth': 'hasOptMonth',
    'optnote': 'hasOptNote',
    'optannote': 'hasOptAnnotation',
    'articleno': 'hasArticleNo',
    'url2': 'hasURL2',
    'oldurl': 'hasOldURL',
    'day': 'hasDay',
    'source': 'hasSource',
    'bibsource': 'hasSource',
    'urlpdf': 'hasURLPDF',
    'urlinfo': 'hasURLInfo',
    'urlspringer': 'hasURLSpringer',
}

logger = logging.getLogger('bibtexToRDF')

def get_property(name) -> tuple[bool, str]:
    name = name.lower()
    try:
        return True, properties[name]
    except KeyError:
        logger.warning(PROPERTY_NOT_FOUND.format(name))
        return False, name