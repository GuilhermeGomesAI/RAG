
"""Funções de texto: limpeza, chunking, títulos e normalização de URL."""
from __future__ import annotations

import re
from urllib.parse import unquote, urldefrag, urlparse


def normalize_url(url: str) -> str:
    url = unquote(urldefrag(url.strip())[0]).rstrip("/")
    return url[:-3] if url.lower().endswith(".md") else url


def strip_frontmatter(s: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", s, count=1, flags=re.S)


def title_from(markdown: str, url: str = "") -> str:
    fm = re.match(r"\A---\n(.*?)\n---\n", markdown, flags=re.S)
    if fm:
        m = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", fm.group(1), flags=re.M)
        if m:
            return m.group(1)

    m = re.search(r"^#\s+(.+)$", strip_frontmatter(markdown), flags=re.M)
    if m:
        return m.group(1).strip()

    slug = unquote(url.rstrip("/").rsplit("/", 1)[-1]) if url else "documento"
    return re.sub(r"\.(md|pdf)$", "", slug).replace("-", " ")


def clean(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"`{1,3}", "", s)
    return re.sub(r"\s+", " ", s).strip()


def split(s: str, size: int = 1100, overlap: int = 180) -> list[str]:
    """Divide o conteúdo respeitando parágrafos, títulos e listas."""

    s = strip_frontmatter(s)
    s = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"`{1,3}", "", s)

    lines = [line.strip() for line in s.splitlines()]

    blocks = []
    current = []

    for line in lines:
        if not line:
            if current:
                blocks.append("\n".join(current))
                current = []
            continue

        # Títulos iniciam um novo bloco.
        if re.match(r"^#{1,6}\s+", line):
            if current:
                blocks.append("\n".join(current))
                current = []

        current.append(line)

    if current:
        blocks.append("\n".join(current))

    chunks = []
    current = ""

    for block in blocks:
        block = block.strip()

        if not block:
            continue

        candidate = f"{current}\n\n{block}".strip() if current else block

        if len(candidate) <= size:
            current = candidate
            continue

        if current and len(current) > 80:
            chunks.append(current)

        # Blocos grandes são divididos em partes menores.
        if len(block) > size:
            start = 0

            while start < len(block):
                end = min(start + size, len(block))

                if end < len(block):
                    point = block.rfind(" ", start + size // 2, end)
                    if point > start:
                        end = point

                piece = block[start:end].strip()

                if len(piece) > 80:
                    chunks.append(piece)

                if end >= len(block):
                    break

                start = max(start + 1, end - overlap)

            current = ""
        else:
            current = block

    if current and len(current) > 80:
        chunks.append(current)

    return chunks


def parse_seed(markdown: str, fallback_source: str) -> list[dict]:
    """Divide uma base-semente por seções e identifica sua fonte."""

    docs = []

    for block in re.split(r"^## ", markdown, flags=re.M)[1:]:
        head, _, body = block.partition("\n")

        m = re.search(r"^Fonte:\s*(\S+)\s*$", body, flags=re.M)
        url = m.group(1) if m else fallback_source

        body = re.sub(r"^Fonte:.*$", "", body, flags=re.M).strip()

        if body:
            docs.append({
                "title": head.strip(),
                "url": url,
                "text": body
            })

    return docs


def family_of(url: str, mapping: dict) -> str | None:
    """Identifica a família do produto pela URL."""

    if not mapping or not url.startswith("http"):
        return None

    seg = [x for x in urlparse(url).path.split("/") if x]

    return mapping.get(seg[0], seg[0]) if seg else None
