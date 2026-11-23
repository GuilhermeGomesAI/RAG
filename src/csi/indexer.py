"""Gera chunks + embeddings + classificador e grava index_meta.json com o que REALMENTE foi processado."""
from __future__ import annotations

import json
from datetime import datetime, timezone

import numpy as np

from . import classifier
from .config import Ecosystem
from .textutils import parse_seed, split, strip_frontmatter, title_from


def collect_docs(eco: Ecosystem) -> tuple[list[dict], dict]:
    seed_md = (eco.src_dir / "seed_knowledge.md").read_text(encoding="utf-8")
    docs = parse_seed(seed_md, fallback_source=f"ecosystems/{eco.key}/seed_knowledge.md")
    for d in docs:
        d["origin"] = "seed"
    stats = {"seed_sections": len(docs), "crawled_md": 0, "crawled_pdf": 0, "pdf_failed": 0}

    urls = {}
    if eco.manifest.exists():
        for line in eco.manifest.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if rec.get("path"):
                urls[rec["path"]] = rec["url"]
    if eco.raw_dir.exists():
        for p in sorted(eco.raw_dir.glob("*.md")):
            text = p.read_text(encoding="utf-8", errors="ignore")
            url = urls.get(str(p.relative_to(eco.data_dir)), "")
            docs.append({"title": title_from(text, url), "url": url,
                         "text": strip_frontmatter(text), "origin": "crawl"})
            stats["crawled_md"] += 1
        try:
            import fitz  # PyMuPDF
        except ImportError:
            fitz = None
            print("PyMuPDF ausente: PDFs não indexados.")
        if fitz:
            for p in sorted(eco.raw_dir.glob("*.pdf")):
                url = urls.get(str(p.relative_to(eco.data_dir)), "")
                try:
                    txt = "\n".join(page.get_text() for page in fitz.open(p))
                    docs.append({"title": title_from("", url), "url": url, "text": txt, "origin": "crawl"})
                    stats["crawled_pdf"] += 1
                except Exception:  # noqa: BLE001
                    stats["pdf_failed"] += 1
    return docs, stats


def build(eco: Ecosystem, encoder) -> dict:
    docs, stats = collect_docs(eco)
    rows = []

    
    for d in docs:
        document_id = d["url"] or d["title"]
        chunks = split(d["text"])

        for i, c in enumerate(chunks):
            rows.append({
                "id": f"{document_id}#{i}",
                "document_id": document_id,
                "chunk_index": i,
                "title": d["title"],
                "source": d["url"],
                "text": c
            })

    if not rows:
        raise SystemExit("Nenhum documento para indexar.")
    print(f"Calculando embeddings para {len(rows)} trechos...")
    # o título entra no texto embutido: melhora a recuperação por nome de produto
    vectors = encoder.encode([f'{r["title"]}. {r["text"]}' for r in rows], show_progress=True)
    eco.data_dir.mkdir(parents=True, exist_ok=True)
    np.save(eco.embeddings_path, np.asarray(vectors, dtype=np.float32))
    with eco.chunks_path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    metrics = classifier.train(eco, encoder)
    meta = {"ecosystem": eco.key, "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "model": getattr(encoder, "name", type(encoder).__name__), "n_chunks": len(rows),
            "seed_only": stats["crawled_md"] + stats["crawled_pdf"] == 0, **stats, "classifier": metrics}
    eco.meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def retrain_classifier(eco: Ecosystem, encoder) -> dict:
    """Retreina só a MLP (rápido): reaproveita o índice já gerado."""
    metrics = classifier.train(eco, encoder)
    meta = json.loads(eco.meta_path.read_text(encoding="utf-8")) if eco.meta_path.exists() else {}
    meta["classifier"] = metrics
    meta["classifier_retrained_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    eco.meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return metrics
