import re

def segment_and_save_sentences(text, output_file="sentences.txt"):
    # Basic multilingual-safe sentence splitter
    sentences = re.split(r'(?<=[.!?।])\s+', text)

    cleaned = []
    for s in sentences:
        s = s.strip()
        if len(s) > 2:
            cleaned.append(s)

    with open(output_file, "w", encoding="utf-8") as f:
        for i, s in enumerate(cleaned, 1):
            f.write(f"{i}. {s}\n")

    print(f"✂ Sentences saved to {output_file}")
    return cleaned
