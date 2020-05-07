import re

def preprocess_text(document):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(document))

        # Give Space between adjecent chars and nums 
        # document = re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", document)

        # Replace _ with space
        document = re.sub(r'[_]', ' ', document)

        # Remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)

        # Replacing numbers 
        # document = clean_numbers(document)

        # Converting to Lowercase
        document = document.lower()

        # if len(word) > 3 and len(word) < 15

        tokens = [word for word in document.split() if len(word) >= 3]

        preprocessed_text = ' '.join(tokens)

        return preprocessed_text

def clean_numbers(x):

    x = re.sub('[0-9]', '', x)

    return x
        