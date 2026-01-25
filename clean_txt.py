import re
import unicodedata

def clean_and_save_text(raw_text, output_file="cleaned_output.txt"):
    text = unicodedata.normalize("NFKC", raw_text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = text.strip()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    return text
