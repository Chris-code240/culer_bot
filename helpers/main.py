import re
from typing import List

def chunk_text(text: str, max_tokens: int = 512, overlap: int = 64) -> List[str]:
    # rough tokenizer by whitespace — replace with tokenizer.encode for precise token counts
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + max_tokens]
        chunks.append(" ".join(chunk))
        i += max_tokens - overlap
    return chunks

def load_corpus(filepath: str) -> List[dict]:
    """
    Returns list of {"id": ..., "title": ..., "text": ...}
    Expects file with sections like "### Title ###\nCONTENT..."
    """
    items = []
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    parts = re.split(r"###\s*(.*?)\s*###\n", raw)
    # parts looks like ["", "Title1", "content1", "Title2", "content2", ...]
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i+1].strip()
        for j, chunk in enumerate(chunk_text(content, max_tokens=400, overlap=80)):
            items.append({"id": f"{title[:40]}_{j}", "title": title, "text": chunk})
    return items
