import re

# Predefined patterns and keywords for labeling
price_pattern = re.compile(r"^(ዋጋ|ብር|\d+)$")  # Match "ዋጋ", "ብር", or numbers
location_keywords = {"አዳማ", "አዲስአበባ", "መገናኛ", "ሜክሲኮ"}  
product_keywords = {"glasses", "sunglass", "shield", "ማበጠሪያ", "ብሩሽ", "ምንጣፍ", "Bottle", "መተኮሻ", "toilet rack", "scale", "Scarlet"}  

# Token labeling function for a single row
def label_tokens(row_tokens):
    labeled_tokens = []
    
    for i, token in enumerate(row_tokens):
        # The first token is always labeled as B-PRODUCT
        if i == 0:
            labeled_tokens.append((token, "B-PRODUCT"))
        else:
            # Check for price-related tokens
            if price_pattern.match(token):
                label = "B-PRICE" if token == "ዋጋ" else "I-PRICE"
                labeled_tokens.append((token, label))
            # Check for location-related tokens
            elif token in location_keywords:
                labeled_tokens.append((token, "I-LOC"))
            # Check for product-related tokens
            elif token.lower() in product_keywords:
                labeled_tokens.append((token, "I-PRODUCT"))
            # Otherwise, mark as outside any entity
            else:
                labeled_tokens.append((token, "O"))
    
    return labeled_tokens
