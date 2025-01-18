import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import re
from amseg.amharicSegmenter import AmharicSegmenter
from transformers import AutoTokenizer

# Rule-based Tokenization using amseg.amharicSegmenter
def amseg_tokenizer(text):
    """
    Tokenize Amharic text using the AmharicSegmenter library.
    """
    sent_punct = []
    word_punct = []
    segmenter = AmharicSegmenter(sent_punct, word_punct)
    tokens = segmenter.amharic_tokenizer(text)
    return tokens


# Tokenization using NLTK
def nltk_tokenizer(text):
    """
    Tokenize Amharic text using the NLTK library.
    """
    tokens = word_tokenize(text)
    return tokens

# Tokenization using Regular Expressions
def regex_tokenizer(text):
    """
    Tokenize Amharic text using Regular Expressions.
    """
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

# Tokenization using Pre-trained XLM-Roberta-Base Tokenizer
def xlm_roberta_tokenizer(text, model_name='xlm-roberta-base'):
    """
    Tokenize text using the XLM-Roberta tokenizer.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    return tokens