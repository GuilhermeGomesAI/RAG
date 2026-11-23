from __future__ import annotations

import argparse
import json

from . import config


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="csi", description="Cielo Intelligence")
    sub = p.add_subparsers(dest="cmd", required=True)
    eco_choices = config.available()
    for name, help_ in [("crawl", "baixa a documentação pública"),
                        ("index", "gera embeddings e treina a MLP"),
                        ("retrain", "retreina só a MLP de tema (rápido)"),
                        ("eval", "mede recall@k, MRR, tema, produto e abstenção"),
                        ("calibrate", "sugere o min_score a partir das perguntas de avaliação"),
                        ("ask", "pergunta via terminal")]:
        s = sub.add_parser(name, help=help_)
        s.add_argument("ecosystem", choices=eco_choices)
        if name == "crawl":
            s.add_argument("--max-pages", type=int, default=2500)
            s.add_argument("--workers", type=int, default=3)
            s.add_argument("--delay", type=float, default=0.2)
        if name in {"eval", "ask", "calibrate"}:
            s.add_argument("-k", type=int, default=5)
        if name == "eval":
            s.add_argument("-v", "--verbose", action="store_true", help="mostra pergunta por pergunta")
        if name == "ask":
            s.add_argument("question")
    a = p.parse_args(argv)
    eco = config.load(a.ecosystem)

    if a.cmd == "crawl":
        from .crawler import crawl
        crawl(eco, a.max_pages, a.workers, a.delay)
    elif a.cmd in {"index", "retrain"}:
        from .encoders import SentenceTransformerEncoder
        from . import indexer
        enc = SentenceTransformerEncoder()
        out = indexer.build(eco, enc) if a.cmd == "index" else indexer.retrain_classifier(eco, enc)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        from .search import Knowledge
        kn = Knowledge(eco)
        if a.cmd == "eval":
            from .evaluate import evaluate
            rep = evaluate(eco, kn, a.k)
            details = rep.pop("details")
            print(json.dumps(rep, ensure_ascii=False, indent=2))
            if a.verbose:
                for d in details:
                    print(f'\nrank={d["rank"]} evid={d["has_evidence"]} score={d["top_score"]} '
                          f'(sem {d["semantic"]} / lex {d["lexical"]}) | {d["question"]}')
                    print(f'   tema={d["category"]} (esperado {d["expected_category"]}) '
                          f'produto={d["family"]} (esperado {d["expected_family"]})')
                    print(f'   top1: {d["top1"]}')
        elif a.cmd == "calibrate":
            from .evaluate import calibrate
            rep = calibrate(eco, kn, a.k)
            print(f'{"limite":>7} {"certas":>7} {"erradas":>8} {"certas_perdidas":>16} {"erradas_barradas":>17}')
            for r in rep["table"]:
                print(f'{r["threshold"]:>7.2f} {r["right_delivered"]:>7} {r["wrong_delivered"]:>8} '
                      f'{r["right_lost"]:>16} {r["wrong_blocked"]:>17}')
            print(f'\nSugestão: min_score = {rep["recommended"]}  ({rep["note"]})')
        else:
            ans = kn.ask(a.question, a.k)
            print(f"Tema provável (MLP): {ans.category} ({ans.category_confidence:.0%})")
            if not ans.has_evidence:
                print(f"⚠ Sem evidência suficiente na documentação indexada (melhor pontuação < {ans.min_score}).")
            elif ans.family:
                print(f"Produto (pela fonte): {ans.family}")
            for n, h in enumerate(ans.hits, 1):
                print(f"\n{n}. [{h.score:.3f} = sem {h.semantic:.2f} + lex {h.lexical:.2f}] {h.title}"
                      f"\n   {h.source or '(sem URL)'}\n   {h.text[:300]}...")
    return 0
