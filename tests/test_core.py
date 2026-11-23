
"""Testes offline: encoder determinístico (hashing) no lugar do SentenceTransformer."""
import re
import sys
import tempfile
import unicodedata
import unittest
import zlib
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import json  # noqa: E402
from csi import config, crawler, evaluate, indexer, lexical, textutils  # noqa: E402
from csi.search import Knowledge  # noqa: E402


class HashingEncoder:
    name = "hashing-test-encoder"

    def encode(self, texts, show_progress=False):
        out = np.zeros((len(texts), 4096), dtype=np.float32)
        for i, t in enumerate(texts):
            t = unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()
            for tok in re.findall(r"\w+", t):
                out[i, zlib.crc32(tok.encode()) % 4096] += 1
        n = np.linalg.norm(out, axis=1, keepdims=True)
        return out / np.where(n == 0, 1, n)


class TextUtils(unittest.TestCase):
    def test_normalize_url(self):
        a = "https://x.com/reference/boas-pr%C3%A1ticas-e-seguran%C3%A7a"
        b = "https://x.com/reference/boas-práticas-e-segurança.md/"
        self.assertEqual(textutils.normalize_url(a), textutils.normalize_url(b))

    def test_title_from(self):
        self.assertEqual(textutils.title_from("---\ntitle: Olá\n---\ncorpo"), "Olá")
        self.assertEqual(textutils.title_from("# Meu título\ntexto"), "Meu título")
        self.assertEqual(textutils.title_from("", "https://x.com/a/minha-pagina.md"), "minha pagina")

    def test_split_respects_size(self):
        chunks = textutils.split("Frase um. " * 400)
        self.assertTrue(chunks and all(80 < len(c) <= 1100 for c in chunks))

    def test_parse_seed_uses_fonte_url(self):
        md = "# T\n\n## A\nFonte: https://h.com/a\nConteúdo A bem longo.\n\n## B\nSem fonte aqui.\n"
        docs = textutils.parse_seed(md, "fallback.md")
        self.assertEqual([d["url"] for d in docs], ["https://h.com/a", "fallback.md"])
        self.assertNotIn("Fonte:", docs[0]["text"])


class Lexical(unittest.TestCase):
    def test_bm25_prefers_exact_product_name(self):
        docs = ["Extrato Eletrônico dados de vendas e pagamentos", "API Pix cobrança imediata", "Chargeback contestação"]
        sc = lexical.BM25(docs).scores("O que é o Extrato Eletrônico?")
        self.assertEqual(int(sc.argmax()), 0)
        self.assertTrue(0 < sc[0] < 1)

    def test_bm25_zero_without_match(self):
        sc = lexical.BM25(["API Pix", "Chargeback"]).scores("bolo de cenoura")
        self.assertEqual(float(sc.max()), 0.0)

    def test_family_of(self):
        m = {"conecta": "Cielo Conecta"}
        self.assertEqual(textutils.family_of("https://d.com/conecta/docs/x.md", m), "Cielo Conecta")
        self.assertEqual(textutils.family_of("https://d.com/outro/docs/x", m), "outro")
        self.assertIsNone(textutils.family_of("https://d.com/conecta/x", {}))
        self.assertIsNone(textutils.family_of("ecosystems/cielo/seed.md", m))


class DataQuality(unittest.TestCase):
    def test_no_eval_question_leaks_into_training(self):
        for key in config.available():
            eco = config.load(key)
            train = {json.loads(l)["text"].strip().lower() for l in
                     (eco.src_dir / "training_examples.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
            ev = {json.loads(l)["question"].strip().lower() for l in
                  (eco.src_dir / "eval_questions.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
            self.assertFalse(train & ev, f"{key}: perguntas de avaliação no treino: {train & ev}")

    def test_every_class_has_enough_examples(self):
        from collections import Counter
        for key in config.available():
            eco = config.load(key)
            c = Counter(json.loads(l)["label"] for l in
                        (eco.src_dir / "training_examples.jsonl").read_text(encoding="utf-8").splitlines() if l.strip())
            self.assertGreaterEqual(min(c.values()), 4, f"{key}: {c}")


class Crawler(unittest.TestCase):
    def test_safe_url_only_official_host(self):
        eco = config.load("cielo")
        self.assertIsNotNone(crawler.safe_url(eco, "https://docs.cielo.com.br/x/y.md#frag"))
        self.assertIsNone(crawler.safe_url(eco, "https://evil.com/docs.cielo.com.br"))
        self.assertIsNone(crawler.safe_url(eco, "ftp://docs.cielo.com.br/x"))

    def test_seed_urls_fallback(self):
        urls = crawler.seed_urls(config.load("cielo"))
        self.assertTrue(urls and all(u.endswith(".md") for u in urls))


class EndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls._old = config.DATA_DIR
        config.DATA_DIR = Path(cls._tmp.name)
        cls.enc = HashingEncoder()
        cls.kn = {}
        for key in config.available():
            eco = config.load(key)
            cls.meta = indexer.build(eco, cls.enc)
            cls.kn[key] = Knowledge(eco, encoder=cls.enc, min_score=0.2)

    @classmethod
    def tearDownClass(cls):
        config.DATA_DIR = cls._old
        cls._tmp.cleanup()

    def test_meta_is_honest_about_seed_only(self):
        self.assertTrue(self.meta["seed_only"])
        self.assertEqual(self.meta["crawled_md"], 0)

    def test_retrieval_returns_official_url(self):
        ans = self.kn["cielo"].ask("Quais os requisitos do Tap on Phone para iOS?", 3)
        self.assertTrue(ans.has_evidence)
        self.assertEqual(textutils.normalize_url(ans.hits[0].source),
                         "https://docs.cielo.com.br/conecta/docs/requisitos-ios")

    def test_abstains_without_evidence(self):
        for key in self.kn:
            ans = self.kn[key].ask("xyzzy plugh qwertyuiop", 3)
            self.assertFalse(ans.has_evidence)

    def test_max_per_source(self):
        ans = self.kn["cielo"].ask("Pix cobrança API", 8, max_per_source=1)
        sources = [textutils.normalize_url(h.source) for h in ans.hits]
        self.assertEqual(len(sources), len(set(sources)))

    def test_family_from_source(self):
        ans = self.kn["cielo"].ask("Quais os requisitos do Tap on Phone para iOS?", 3)
        self.assertEqual(ans.family, "Cielo Conecta e Tap on Phone")

    def test_context_recovers_neighbor_chunks(self):
        kn = self.kn["cielo"]

        original_chunks = kn.chunks
        original_lookup = kn.chunk_lookup

        try:
            kn.chunks = [
                {
                    "document_id": "pagina-a",
                    "chunk_index": 0,
                    "text": "Trecho anterior"
                },
                {
                    "document_id": "pagina-a",
                    "chunk_index": 1,
                    "text": "Trecho principal"
                },
                {
                    "document_id": "pagina-a",
                    "chunk_index": 2,
                    "text": "Trecho posterior"
                },
                {
                    "document_id": "pagina-b",
                    "chunk_index": 2,
                    "text": "Outra página"
                }
            ]

            kn.chunk_lookup = {
                (c["document_id"], c["chunk_index"]): i
                for i, c in enumerate(kn.chunks)
            }

            context = kn.get_context(kn.chunks[1])

            self.assertIn("Trecho anterior", context)
            self.assertIn("Trecho posterior", context)
            self.assertNotIn("Outra página", context)

        finally:
            kn.chunks = original_chunks
            kn.chunk_lookup = original_lookup

    def test_calibrate_and_retrain(self):
        rep = evaluate.calibrate(config.load("cielo"), self.kn["cielo"])
        self.assertIn(rep["recommended"], [r["threshold"] for r in rep["table"]])
        m = indexer.retrain_classifier(config.load("cielo"), self.enc)
        self.assertEqual(m["n_examples"], sum(m["labels"].values()))
        self.assertEqual(m["classes_com_1_exemplo"], [])
        self.assertIsNotNone(m["cv_accuracy"])

    def test_evaluate_report_shape(self):
        for key, kn in self.kn.items():
            rep = evaluate.evaluate(config.load(key), kn, 5)
            self.assertIn("recall@5", rep)
            self.assertIn("wrong_answers_delivered", rep)
            self.assertGreater(rep["n_in_scope"], 0)
            print(f"\n[{key}] " + str({k: v for k, v in rep.items() if k != "details"}))


if __name__ == "__main__":
    unittest.main()
