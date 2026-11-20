"""Rank short document cards with inspectable lexical scores."""
import re


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def rank(corpus, query, k, title_weight=0, aliases=None):
    original = tokens(query)
    expanded = original | {
        term for word in original for term in (aliases or {}).get(word, [])
    }
    results = []
    for document in corpus:
        body_hits = sorted(expanded & tokens(document["body"]))
        title_hits = sorted(expanded & tokens(document["title"]))
        score = len(body_hits) + title_weight * len(title_hits)
        if score:
            results.append({
                "id": document["id"],
                "score": score,
                "body_hits": body_hits,
                "title_hits": title_hits,
            })
    return sorted(results, key=lambda result: (-result["score"], result["id"]))[:k]


def candidate_aliases(plan, mode):
    if mode == "none":
        return {}
    if mode == "tight":
        return plan["aliases"]
    if mode == "wide":
        tight = plan["aliases"]
        extra = plan["wide_aliases"]
        return {
            word: sorted(set(tight.get(word, [])) | set(extra.get(word, [])))
            for word in tight.keys() | extra.keys()
        }
    raise ValueError(f"Unknown alias mode: {mode}")
