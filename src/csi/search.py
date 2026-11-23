
"""Recuperação híbrida (embeddings + BM25), tema por MLP, produto pela fonte e abstenção."""
from __future__ import annotations

import json
from dataclasses import dataclass, field

import joblib
import numpy as np

from .config import Ecosystem
from .lexical import BM25
from .textutils import family_of, normalize_url


@dataclass
class Hit:
    id: str
    title: str
    source: str
    text: str
    score: float
    semantic: float = 0.0
    lexical: float = 0.0
    context: str = ""


@dataclass
class Answer:
    question: str
    category: str
    category_confidence: float
    hits: list[Hit] = field(default_factory=list)
    has_evidence: bool = False
    min_score: float = 0.0
    family: str | None = None


class Knowledge:
    def __init__(
        self,
        eco: Ecosystem,
        encoder=None,
        min_score: float | None = None,
        hybrid_weight: float | None = None,
    ):
        if not eco.embeddings_path.exists():
            raise FileNotFoundError(
                f"Índice de '{eco.key}' não encontrado. "
                f"Rode: python -m csi index {eco.key}"
            )

        if encoder is None:
            from .encoders import SentenceTransformerEncoder
            encoder = SentenceTransformerEncoder()

        self.eco = eco
        self.encoder = encoder
        self.min_score = eco.min_score if min_score is None else min_score
        self.w = eco.hybrid_weight if hybrid_weight is None else hybrid_weight

        self.vectors = np.load(eco.embeddings_path)

        self.chunks = [
            json.loads(line)
            for line in eco.chunks_path.read_text(encoding="utf-8").splitlines()
        ]

        # Mapa para localizar chunks vizinhos do mesmo documento.
        # Compatível com índices antigos sem esses metadados.
        self.chunk_lookup = {}

        for idx, chunk in enumerate(self.chunks):
            document_id = chunk.get("document_id")
            chunk_index = chunk.get("chunk_index")

            if document_id is not None and chunk_index is not None:
                self.chunk_lookup[
                    (document_id, int(chunk_index))
                ] = idx

        self.classifier = joblib.load(eco.classifier_path)

        # O título conta em dobro: nomes de produto costumam estar nele.
        self.lex = BM25([
            f'{c["title"]} {c["title"]} {c["text"]}'
            for c in self.chunks
        ])

    def get_context(self, chunk: dict) -> str:
        """Recupera os chunks anterior e posterior do mesmo documento."""

        document_id = chunk.get("document_id")
        chunk_index = chunk.get("chunk_index")

        if document_id is None or chunk_index is None:
            return ""

        neighbors = []

        for offset in (-1, 1):
            neighbor_idx = self.chunk_lookup.get(
                (document_id, int(chunk_index) + offset)
            )

            if neighbor_idx is not None:
                neighbors.append(
                    self.chunks[neighbor_idx]["text"]
                )

        return "\n\n".join(neighbors)

    def ask(
        self,
        question: str,
        k: int = 5,
        max_per_source: int = 2,
    ) -> Answer:

        q = np.asarray(self.encoder.encode([question]))[0]

        sem = self.vectors @ q
        lex = self.lex.scores(question)

        scores = (1 - self.w) * sem + self.w * lex

        proba = self.classifier.predict_proba(q[None, :])[0]
        top = int(np.argmax(proba))

        hits = []
        per_source = {}

        for i in np.argsort(scores)[::-1]:
            c = self.chunks[int(i)]

            key = normalize_url(c["source"]) or c["id"]

            if per_source.get(key, 0) >= max_per_source:
                continue

            per_source[key] = per_source.get(key, 0) + 1

            hits.append(
                Hit(
                    id=c["id"],
                    title=c["title"],
                    source=c["source"],
                    text=c["text"],
                    score=float(scores[int(i)]),
                    semantic=float(sem[int(i)]),
                    lexical=float(lex[int(i)]),
                    context=self.get_context(c),
                )
            )

            if len(hits) == k:
                break

        # A evidência continua sendo avaliada pelo score original.
        # O contexto dos vizinhos não altera a pontuação.
        has_ev = bool(hits) and hits[0].score >= self.min_score

        # Produto identificado pela fonte do primeiro resultado.
        family = (
            family_of(hits[0].source, self.eco.product_families)
            if has_ev
            else None
        )

        return Answer(
            question,
            str(self.classifier.classes_[top]),
            float(proba[top]),
            hits,
            has_ev,
            self.min_score,
            family,
        )
