import re
import emoji

# Function to filter profanity and perform word replacement
def filter_text(text):
    # Filter profanity
    # Word replacements
    word_replacements = {
        "fuck": "eff",
        "shit": "poop",
        "sexual experience": "intercourse",
        "sexual": "you know",
        "sexy": "tempting",
        "seggs": "lovemaking",
        "sex": "lovemaking",
        "blowjob": "oral",
        "blow job": "oral",
        "pussy": "vaj",
        "cock": "willie",
        "dick": "willie",
        "cumshot": "bust-shot",
        "cumming": "busting",
        "cum": "bust",
        "squirt": "flow",
        "porn": "lewd videos",
        "masturbation": "self-stimulation",
        "anal": "back",
        "fucking": "flippin",
        "|":"I",
        "masturbating":"playing with myself",
        "masturbate":"self-stimulate",
        "@.":""
        # Add more replacements as needed
    }

    # Perform word replacement for profanity, case-insensitive
    for profane_word, replacement_word in word_replacements.items():
        # Use a case-insensitive regular expression with word boundaries to replace word occurences in isolation
        pattern = re.compile(rf'\b{re.escape(profane_word)}\b', re.IGNORECASE)
        text = pattern.sub(replacement_word, text)

    return text

# Function to clean and format text
def clean_and_format_text(text):
    # Remove leading and trailing spaces
    text = text.strip()

    # Remove newlines and extra spaces
    text = ' '.join(text.split())

    # Convert emoji symbols to names
    text = emoji.emojize(text)

    # Use regex to remove the \u201c in the beginning
    text = re.sub(r'(\u201c)', '', text)

    # Use regex to replace the final \u201d before the location with a full stop
    text = re.sub(r'(\u201d)', '.', text)

    # Use regex to replace \u2019 or \u2018 with an apostrophe
    text = re.sub(r'(\u2019|\u2018)', "'", text)

    # Use regex to replace \u00ae or \u00a9 with "crying emoji"
    text = re.sub(r'(\u00ae|\u00a9)', ', crying emoji', text)

    # Use regex to replace " with '
    text = re.sub(r'"', "'", text)

    # Replace '|' with 'I'
    text = text.replace('|', 'I')

    return text

# Function to extract series and part information
def extract_series_and_part(text):
    pattern = r'Confession #(\d+)'
    match = re.search(pattern, text)
    series = "Confessions"
    part = match.group(1) if match else None
    return series, part

# Function to split and clean text
def split_and_clean_text(text):
    # Split the text into words
    words = text.split()

    # Delete the first 2 words (if there are at least 3 words)
    if len(words) >= 3:
        del words[:2]

    # Join the remaining words back into text
    text = ' '.join(words)

    return text
