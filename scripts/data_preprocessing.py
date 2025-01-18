import pandas as pd
import re


# Remove emojis from the 'Message Text'
def remove_emojis(text):
    """
    Removes emojis and other non-text characters from the input text.
    """
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        u"\u231A"                 #  watch
        u"\u23F1"                 #  stopwatch
        u"\u23F0"                 #  alarm clock
        u"\u23F3"                 #  hourglass flowing sand
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

#  Remove URLs
def remove_urls(text):
    """
    Removes URLs from the input text.
    """
    return re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)



# Normalize text 
def normalize_text(text):
    """
    Normalize text by handling Amharic-specific variants
    """
    char_map = {
        'ሀ': 'ኀ',
        'ሰ': 'ሠ',
        'ጸ': 'ፀ'
    }
    for key, value in char_map.items():
        text = text.replace(key, value)
    return text


