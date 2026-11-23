"""Encoder de embeddings. Import pesado é adiado para não exigir PyTorch em testes/CI."""
from __future__ import annotations

import numpy as np

from .config import MODEL_NAME


class SentenceTransformerEncoder:
    def __init__(self, name: str = MODEL_NAME):
        from sentence_transformers import SentenceTransformer  # import tardio
        self.name = name
        self._model = SentenceTransformer(name)

    def encode(self, texts: list[str], show_progress: bool = False) -> np.ndarray:
        vec = self._model.encode(texts, batch_size=32, show_progress_bar=show_progress,
                                 normalize_embeddings=True)
        return np.asarray(vec, dtype=np.float32)
