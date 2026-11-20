"""Lab 2: retrieval benchmark on synthetic data.
Question: does TF-IDF cosine beat exact keyword count on precision at 5?
One factor changes: scoring method. Corpus, queries and k stay fixed.
"""
import math, random, re, time
from collections import Counter, defaultdict

random.seed(42)
TOPICS = {
    "agents": ["agent", "planner", "tool", "loop", "workflow"],
    "models": ["model", "token", "context", "weights", "inference"],
    "data": ["dataset", "label", "split", "leakage", "sample"],
    "infra": ["server", "queue", "cache", "latency", "deploy"],
}
FILLER = ["report", "notes", "weekly", "review", "draft", "update", "general", "misc"]

docs, truth = [], {}
for i in range(200):
    topic = list(TOPICS)[i % 4]
    words = random.choices(TOPICS[topic], k=14) + random.choices(FILLER, k=4)
    random.shuffle(words)
    docs.append(" ".join(words))
    truth[i] = topic

queries = []
for topic, words in TOPICS.items():
    for j in range(5):
        q = " ".join(random.sample(words, 3))
        queries.append((q, topic))

def toks(text): return re.findall(r"[a-z]+", text)

def score_keyword(query, doc):
    q, d = Counter(toks(query)), Counter(toks(doc))
    return sum(d[w] for w in q)

def build_idf():
    df = Counter()
    for d in docs:
        for w in set(toks(d)): df[w] += 1
    n = len(docs)
    return {w: math.log((n + 1) / (c + 1)) + 1 for w, c in df.items()}
IDF = build_idf()

def vec(text):
    c = Counter(toks(text))
    return {w: (1 + math.log(v)) * IDF.get(w, 1.0) for w, v in c.items()}

def score_tfidf(query, doc):
    a, b = vec(query), vec(doc)
    dot = sum(a[w] * b.get(w, 0.0) for w in a)
    na = math.sqrt(sum(v * v for v in a.values())); nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0

def precision_at_5(scorer):
    hits = 0
    for q, topic in queries:
        ranked = sorted(range(len(docs)), key=lambda i: scorer(q, docs[i]), reverse=True)[:5]
        hits += sum(1 for i in ranked if truth[i] == topic)
    return hits / (len(queries) * 5)

for name, scorer in [("keyword", score_keyword), ("tfidf", score_tfidf)]:
    vals, t0 = [], time.time()
    for _ in range(3):
        vals.append(round(precision_at_5(scorer), 4))
    dt = round((time.time() - t0) / 3, 4)
    print(f"{name}: precision@5 runs={vals} mean={round(sum(vals)/3,4)} seconds_per_run={dt}")
print("docs=200 queries=20 k=5 repeats=3 seed=42")
