from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import json, pandas as pd

EMBED_MODEL = "all-MiniLM-L6-v2"  # small, fast; change for quality
embedder = SentenceTransformer(EMBED_MODEL)

def build_faiss_index(docs, index_path="barca_wiki_index.faiss", meta_path="barca_wiki_meta.pkl"):
    """
        USAGE: 
            docs = load_corpus("barca_corpus.txt")
            build_faiss_index(docs)
    """
    texts = [d["text"] for d in docs]
    ids = [d["id"] for d in docs]
    embs = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    dim = embs.shape[1]
    index = faiss.IndexFlatIP(dim)   # inner product; use IndexFlatL2 with normalized vectors if desired
    faiss.normalize_L2(embs)
    index.add(embs)                  # simple flat index: fine for small corpora
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump({"ids": ids, "texts": texts}, f)
    print("Saved FAISS index and metadata.")



def load_structured_entries(team_json="barca_team.json", matches_json="barca_matches.json"):

    entries = []
    # team/players
    try:
        with open(team_json, "r", encoding="utf-8") as f:
            team = json.load(f)
            for p in team.get("squad", []):
                text = f"{p.get('name')} — position: {p.get('position')}, nationality: {p.get('nationality')}, number: {p.get('shirtNumber')}"
                entries.append({"id": f"player_{p.get('name')}", "text": text})
    except FileNotFoundError:
        pass

    # matches
    try:
        with open(matches_json, "r", encoding="utf-8") as f:
            matches = json.load(f).get("matches", [])
            for m in matches:
                date = m.get("utcDate")
                home = m["homeTeam"]["name"]
                away = m["awayTeam"]["name"]
                score = m["score"]["fullTime"]
                text = f"{date}: {home} {score['home']} - {score['away']} {away}"
                entries.append({"id": f"match_{m.get('id')}", "text": text})
    except FileNotFoundError:
        pass

    return entries

def build_structured_index(entries, index_path="barca_struct_index.faiss", meta_path="barca_struct_meta.pkl"):
    texts = [e["text"] for e in entries]
    ids = [e["id"] for e in entries]
    embs = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    faiss.normalize_L2(embs)
    dim = embs.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embs)
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump({"ids": ids, "texts": texts}, f)
    print("Saved structured FAISS index.")



# entries = load_structured_entries()
# build_structured_index(entries)