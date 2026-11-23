"""Coleta somente conteúdo público do host oficial do ecossistema (respeitando robots.txt)."""
from __future__ import annotations

import hashlib
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib import robotparser
from urllib.parse import urldefrag, urlparse

import requests

from .config import Ecosystem


def safe_url(eco: Ecosystem, url: str) -> str | None:
    url = urldefrag(url.strip())[0]
    p = urlparse(url)
    if p.scheme not in {"https", "http"} or p.hostname != eco.host:
        return None
    return url


def extract_links(text: str) -> list[str]:
    return re.findall(r"https?://[^\s\]\)>\"']+", text)


def seed_urls(eco: Ecosystem) -> list[str]:
    """Fallback quando o llms.txt está indisponível: páginas-semente + '.md' (convenção descrita pelos portais)."""
    seeds = json.loads((eco.src_dir / "seed_sources.json").read_text(encoding="utf-8"))
    return [s["url"] if s["url"].endswith(".md") else s["url"] + ".md" for s in seeds]


def _robots(eco: Ecosystem) -> robotparser.RobotFileParser | None:
    try:
        r = requests.get(f"https://{eco.host}/robots.txt", headers={"User-Agent": eco.user_agent}, timeout=15)
        if r.status_code != 200:
            return None
        rp = robotparser.RobotFileParser()
        rp.parse(r.text.splitlines())
        return rp
    except Exception:
        return None


def crawl(eco: Ecosystem, max_pages: int = 2500, workers: int = 3, delay: float = 0.2) -> dict:
    headers = {"User-Agent": eco.user_agent}
    eco.raw_dir.mkdir(parents=True, exist_ok=True)
    robots = _robots(eco)

    def allowed(url: str) -> bool:
        return robots is None or robots.can_fetch(eco.user_agent, url)

    def fetch(url: str):
        try:
            r = requests.get(url, headers=headers, timeout=35)
            r.raise_for_status()
            return r
        except Exception as e:  # noqa: BLE001 — registramos a falha no manifesto
            return e

    index = fetch(eco.index_url)
    if isinstance(index, Exception):
        print(f"llms.txt indisponível ({index}). Usando as páginas-semente + '.md'.")
        urls = seed_urls(eco)
    else:
        (eco.data_dir / "llms.txt").write_text(index.text, encoding="utf-8")
        urls = []
        for u in extract_links(index.text):
            u = safe_url(eco, u.rstrip(".,;"))
            if u and (u.endswith(".md") or u.lower().endswith(".pdf")):
                urls.append(u)
    urls = list(dict.fromkeys(urls))[:max_pages]
    print(f"{len(urls)} URLs oficiais para coleta.")

    def download(url: str) -> dict:
        if not allowed(url):
            return {"url": url, "status": "blocked_by_robots"}
        time.sleep(delay)
        r = fetch(url)
        if isinstance(r, Exception):
            return {"url": url, "status": "error", "error": str(r)}
        ext = ".pdf" if url.lower().endswith(".pdf") else ".md"
        path = eco.raw_dir / (hashlib.sha256(url.encode()).hexdigest()[:24] + ext)
        path.write_bytes(r.content)
        return {"url": url, "status": "downloaded", "path": str(path.relative_to(eco.data_dir)),
                "bytes": len(r.content), "sha256": hashlib.sha256(r.content).hexdigest(),
                "content_type": r.headers.get("content-type", ""),
                "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}

    records = []
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futs = [pool.submit(download, u) for u in urls]
        for i, f in enumerate(as_completed(futs), 1):
            records.append(f.result())
            if i % 30 == 0 or i == len(futs):
                print(f"{i}/{len(futs)}")

    pdfs = set()
    for rec in records:
        if rec["status"] == "downloaded" and rec["path"].endswith(".md"):
            body = (eco.data_dir / rec["path"]).read_text(encoding="utf-8", errors="ignore")
            for u in extract_links(body):
                u = safe_url(eco, u.rstrip(".,;"))
                if u and u.lower().endswith(".pdf"):
                    pdfs.add(u)
    known = {r["url"] for r in records}
    for u in sorted(pdfs - known):
        records.append(download(u))

    with eco.manifest.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    ok = sum(r["status"] == "downloaded" for r in records)
    print(f"Coleta finalizada: {ok} downloads; {len(records) - ok} falhas/bloqueios (veja {eco.manifest}).")
    return {"downloaded": ok, "failed": len(records) - ok}
