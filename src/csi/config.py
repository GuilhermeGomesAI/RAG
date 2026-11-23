"""Configuração central: caminhos, modelo de embeddings e carga dos ecossistemas."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ECOSYSTEMS_DIR = ROOT / "ecosystems"
DATA_DIR = ROOT / "data"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@dataclass(frozen=True)
class Ecosystem:
    key: str
    label: str
    host: str
    index_url: str
    scope: str
    min_score: float
    user_agent: str
    hybrid_weight: float = 0.3  # peso da busca lexical (0 = só semântica)
    product_families: dict = field(default_factory=dict)  # 1º segmento da URL -> nome do produto

    @property
    def src_dir(self) -> Path:
        return ECOSYSTEMS_DIR / self.key

    @property
    def data_dir(self) -> Path:
        return DATA_DIR / self.key

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def manifest(self) -> Path:
        return self.data_dir / "manifest.jsonl"

    @property
    def chunks_path(self) -> Path:
        return self.data_dir / "chunks.jsonl"

    @property
    def embeddings_path(self) -> Path:
        return self.data_dir / "embeddings.npy"

    @property
    def classifier_path(self) -> Path:
        return self.data_dir / "classifier.joblib"

    @property
    def meta_path(self) -> Path:
        return self.data_dir / "index_meta.json"


def available() -> list[str]:
    if not ECOSYSTEMS_DIR.exists():
        return []
    return sorted(p.name for p in ECOSYSTEMS_DIR.iterdir() if (p / "config.json").exists())


def load(key: str) -> Ecosystem:
    path = ECOSYSTEMS_DIR / key / "config.json"
    if not path.exists():
        raise SystemExit(f"Ecossistema desconhecido: {key!r}. Disponíveis: {', '.join(available())}")
    return Ecosystem(key=key, **json.loads(path.read_text(encoding="utf-8")))
