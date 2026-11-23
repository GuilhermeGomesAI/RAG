"""BM25 simples (sem dependências) para dar peso a termos exatos, como nomes de produto."""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter, defaultdict

import numpy as np

STOP = set("""a o as os de da do das dos em no na nos nas um uma uns umas e ou que para pra por com como se ao aos
ser sua seu suas seus minha meu qual quais quando onde ha ja mais muito pelo pela pelos pelas isso isto esse essa
este esta sao foi tem ter""".split())


def tokens(text: str) -> list[str]:
    t = unicodedata.normalize("NFKD", text.lower()).encode("ascii", "ignore").decode()
    return [w for w in re.findall(r"[a-z0-9]+", t) if len(w) > 1 and w not in STOP]


class BM25:
    """Score normalizado em [0, 1): fração do peso dos termos da pergunta que o trecho cobre."""

    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        toks = [tokens(d) for d in docs]
        self.n, self.k1, self.b = len(docs), k1, b
        self.len = np.array([len(t) for t in toks], dtype=np.float32)
        self.avg = max(float(self.len.mean()) if self.n else 1.0, 1.0)
        df: Counter = Counter()
        self.post: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for i, t in enumerate(toks):
            for term, tf in Counter(t).items():
                df[term] += 1
                self.post[term].append((i, tf))
        self.idf = {term: math.log(1 + (self.n - d + 0.5) / (d + 0.5)) for term, d in df.items()}
        self.idf_unknown = math.log(1 + (self.n + 0.5) / 0.5)

    def scores(self, query: str) -> np.ndarray:
        out = np.zeros(self.n, dtype=np.float32)
        q = set(tokens(query))
        if not q or not self.n:
            return out
        denom = 0.0
        for term in q:
            idf = self.idf.get(term)
            denom += (self.idf_unknown if idf is None else idf) * (self.k1 + 1)
            if idf is None:
                continue
            for i, tf in self.post[term]:
                out[i] += idf * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
        return np.clip(out / denom, 0.0, 1.0)
