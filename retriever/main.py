from embedding.main import pickle, embedder, faiss


def load_index(index_path, meta_path):
    idx = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        meta = pickle.load(f)
    return idx, meta

def query_index(query: str, idx, meta, top_k: int = 5):
    q_emb = embedder.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = idx.search(q_emb, top_k)
    results = []
    for score, i in zip(D[0], I[0]):
        if i < 0:
            continue
        results.append({"id": meta["ids"][i], "text": meta["texts"][i], "score": float(score)})
    return results

# load both
wiki_idx, wiki_meta = load_index("../barca_wiki_index.faiss", "barca_wiki_meta.pkl")
struct_idx, struct_meta = load_index("barca_struct_index.faiss", "barca_struct_meta.pkl")


# example
# q = "Who scored for Barcelona in the last match?"
# print(query_index(q, wiki_idx, wiki_meta, top_k=3))
# print(query_index(q, struct_idx, struct_meta, top_k=3))
