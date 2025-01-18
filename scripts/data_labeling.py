import re
import pandas as pd


tokenized_data = pd.read_csv('../data/tokenized_telegram_data.csv')

# Predefined patterns for automated labeling

price_pattern = re.compile(r"^(ዋጋ|ብር|\d+)$")  # Match "ዋጋ", "ብር", or numbers
location_keywords = {"አዳማ", "አዲስአበባ", "መገናኛ", "ሜክሲኮ"}  # Example location keywords
product_keywords = {"glasses", "sunglass", "shield"}  # Example product keywords

def label_tokens(tokens):
    labeled_tokens = []
    for token in tokens:
        # Label the first token as B-PRODUCT and the rest as I-PRODUCT
        first_line_tokens = re.findall(r'\S+', token[0])
        if first_line_tokens:
            labeled_tokens.append(f"{first_line_tokens[0]} B-PRODUCT")  # First token as B-PRODUCT
            for token in first_line_tokens[1:]:
                labeled_tokens.append(f"{token} I-PRODUCT")  # Remaining tokens as I-PRODUCT
        
        # Check for price-related tokens
        elif price_pattern.match(token):
            if token == "ዋጋ":
                labeled_tokens.append((token, "B-PRICE"))
            else:
                labeled_tokens.append((token, "I-PRICE"))
        # Check for location-related tokens
        elif token in location_keywords:
            if labeled_tokens and labeled_tokens[-1][1] == "B-LOC":
                labeled_tokens.append((token, "I-LOC"))
            else:
                labeled_tokens.append((token, "B-LOC"))
        # Check for product-related tokens
        elif token.lower() in product_keywords:
            if labeled_tokens and labeled_tokens[-1][1] == "B-Product":
                labeled_tokens.append((token, "I-Product"))
            else:
                labeled_tokens.append((token, "B-Product"))
        # Otherwise, mark as outside any entity
        else:
            labeled_tokens.append((token, "O"))
    return labeled_tokens

# Apply labeling function to tokenized data
labeled_data = [label_tokens(sentence) for sentence in tokenized_data]

# Write to CoNLL format
def write_conll_format(labeled_data, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for sentence in labeled_data:
            for token, label in sentence:
                f.write(f"{token}\t{label}\n")
            f.write("\n")  # Separate sentences with a blank line

output_file = "labeled_data.conll"
write_conll_format(labeled_data, output_file)
print(f"Labeled data saved to {output_file}.")
