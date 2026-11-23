"""Métricas objetivas e calibração do limite de evidência."""
from __future__ import annotations

import json

import numpy as np

from .config import Ecosystem
from .search import Knowledge
from .textutils import normalize_url


def _items(eco: Ecosystem) -> list[dict]:
    path = eco.src_dir / "eval_questions.jsonl"
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def evaluate(eco: Ecosystem, kn: Knowledge, k: int = 5) -> dict:
    items = _items(eco)
    n_in = n_out = hit_k = cat_ok = cat_n = fam_ok = fam_n = false_abstain = correct_abstain = wrong_delivered = 0
    rr, details = 0.0, []
    for it in items:
        ans = kn.ask(it["question"], k)
        expected = {normalize_url(u) for u in it["expected"]}
        rank = next((n for n, h in enumerate(ans.hits, 1) if normalize_url(h.source) in expected), None)
        top = ans.hits[0] if ans.hits else None
        if expected:
            n_in += 1
            hit_k += rank is not None
            rr += 1 / rank if rank else 0
            false_abstain += not ans.has_evidence
            wrong_delivered += ans.has_evidence and rank != 1
            if "category" in it:
                cat_n += 1
                cat_ok += ans.category == it["category"]
            if "family" in it:
                fam_n += 1
                fam_ok += ans.family == it["family"]
        else:
            n_out += 1
            correct_abstain += not ans.has_evidence
            wrong_delivered += ans.has_evidence
        details.append({"question": it["question"], "rank": rank, "has_evidence": ans.has_evidence,
                        "top_score": round(top.score, 3) if top else None,
                        "semantic": round(top.semantic, 3) if top else None,
                        "lexical": round(top.lexical, 3) if top else None,
                        "category": ans.category, "expected_category": it.get("category"),
                        "family": ans.family, "expected_family": it.get("family"),
                        "top1": top.source if top else None})
    n = max(n_in, 1)
    return {"ecosystem": eco.key, "k": k, "min_score": kn.min_score, "hybrid_weight": kn.w,
            "n_in_scope": n_in, f"recall@{k}": hit_k / n, "mrr": rr / n,
            "category_accuracy": (cat_ok / cat_n) if cat_n else None,
            "family_accuracy": (fam_ok / fam_n) if fam_n else None,
            "false_abstention_rate": false_abstain / n,
            "n_out_of_scope": n_out,
            "correct_abstention_rate": (correct_abstain / n_out) if n_out else None,
            "wrong_answers_delivered": wrong_delivered,
            "details": details}


def calibrate(eco: Ecosystem, kn: Knowledge, k: int = 5) -> dict:
    """Varre limites e mostra, para cada um, quantas respostas erradas seriam entregues e quantas certas perdidas."""
    rows = []
    for it in _items(eco):
        ans = kn.ask(it["question"], k)
        expected = {normalize_url(u) for u in it["expected"]}
        top = ans.hits[0]
        rows.append((top.score, bool(expected) and normalize_url(top.source) in expected))
    table = []
    for t in np.arange(0.20, 0.801, 0.05):
        t = round(float(t), 2)
        table.append({"threshold": t,
                      "right_delivered": sum(c and s >= t for s, c in rows),
                      "wrong_delivered": sum((not c) and s >= t for s, c in rows),
                      "right_lost": sum(c and s < t for s, c in rows),
                      "wrong_blocked": sum((not c) and s < t for s, c in rows)})
    safe = [r for r in table if r["wrong_delivered"] == 0]
    best = min(safe, key=lambda r: r["threshold"]) if safe else min(
        table, key=lambda r: (r["wrong_delivered"] + r["right_lost"], r["threshold"]))
    return {"n_questions": len(rows), "table": table, "recommended": best["threshold"],
            "note": "Amostra pequena: use como ponto de partida e recalibre com mais perguntas."}
