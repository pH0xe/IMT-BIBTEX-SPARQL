import os
import sys
from typing import List
import yake


def extract_keywords(text: str) -> List[str]:
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
    return [keyword[0] for keyword in keywords]

def check_environnement():
    to_test = ['POSTGRESQL_USERNAME', 'POSTGRESQL_PASSWORD', 'POSTGRESQL_HOST', 'POSTGRESQL_PORT', 'POSTGRESQL_DB', 'FLASK_HOST', 'FLASK_PORT']
    missing = []

    for v in to_test:
        if v not in os.environ:
            missing.append(v)
    if len(missing) > 0:
        msg = f"Error : Missing value in .env file : {', '.join(missing)}"
        sys.exit(msg)