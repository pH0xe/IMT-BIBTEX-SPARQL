from typing import List
import yake


def extract_keywords(text: str) -> List[str]:
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)
    return [keyword[0] for keyword in keywords]