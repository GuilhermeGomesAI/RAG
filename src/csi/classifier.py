"""MLP (rede neural feed-forward) sobre embeddings para classificar o tema da pergunta."""
from __future__ import annotations

import json
from collections import Counter

import joblib
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neural_network import MLPClassifier

from .config import Ecosystem


def load_examples(eco: Ecosystem) -> tuple[list[str], list[str]]:
    texts, labels = [], []
    for line in (eco.src_dir / "training_examples.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            texts.append(item["text"])
            labels.append(item["label"])
    return texts, labels


def _mlp() -> MLPClassifier:
    return MLPClassifier(hidden_layer_sizes=(48, 24), activation="relu", solver="adam",
                         max_iter=800, random_state=42)


def train(eco: Ecosystem, encoder) -> dict:
    texts, labels = load_examples(eco)
    X = np.asarray(encoder.encode(texts))
    counts = Counter(labels)
    cv_acc, folds = None, 0
    if min(counts.values()) >= 2:
        folds = min(3, min(counts.values()))
        cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)
        cv_acc = float(cross_val_score(_mlp(), X, labels, cv=cv).mean())
    model = _mlp().fit(X, labels)
    eco.data_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, eco.classifier_path)
    singletons = sorted(k for k, v in counts.items() if v < 2)
    return {"n_examples": len(texts), "labels": dict(counts), "cv_accuracy": cv_acc, "cv_folds": folds,
            "classes_com_1_exemplo": singletons}
