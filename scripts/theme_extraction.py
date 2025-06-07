import pandas as pd
from typing import List, Dict
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter


nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str) -> str:
    """
    Preprocess text by removing stop words and punctuation.
    
    Args:
        text: Input text to preprocess
    
    Returns:
        str: Preprocessed text
    """
    doc = nlp(text.lower().strip())
    
    tokens = [
            token.lemma_ for token in doc 
            if not token.is_stop and 
            not token.is_punct
            and token.text.isalpha()
        ]
    
    return ' '.join(tokens)