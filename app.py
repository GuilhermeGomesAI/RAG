
"""Interface Streamlit: streamlit run app.py"""
import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))
from csi import config  # noqa: E402
from csi.search import Knowledge  # noqa: E402

st.set_page_config(
    page_title="Cielo Intelligence",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Cielo Intelligence")

st.caption(
    "Busca semântica (embeddings) + MLP de tema sobre documentação pública. "
    "Não é produto oficial e não gera respostas sem evidência."
)

key = st.sidebar.selectbox(
    "Ecossistema",
    config.available(),
    format_func=lambda k: config.load(k).label,
)

eco = config.load(key)
st.sidebar.info(eco.scope)

if not eco.embeddings_path.exists():
    st.warning("A base deste ecossistema ainda não foi construída.")
    st.code(
        f"python -m csi crawl {key}\npython -m csi index {key}",
        language="bash",
    )
    st.stop()

meta = (
    json.loads(eco.meta_path.read_text(encoding="utf-8"))
    if eco.meta_path.exists()
    else {}
)

if meta.get("seed_only"):
    st.sidebar.warning(
        "Índice construído SÓ com a base-semente curada "
        "(crawler não executado)."
    )
else:
    st.sidebar.success(
        f"{meta.get('crawled_md', '?')} páginas e "
        f"{meta.get('crawled_pdf', 0)} PDFs indexados."
    )

st.sidebar.caption(
    f"{meta.get('n_chunks', '?')} trechos · "
    f"gerado em {meta.get('built_at', '?')}"
)


@st.cache_resource
def load(k: str) -> Knowledge:
    return Knowledge(config.load(k))


kn = load(key)

q = st.text_input(
    "Pergunte sobre produtos, APIs e processos",
    placeholder="Ex.: Quando devo executar o ReversalProvider?",
)

k = st.slider("Trechos recuperados", 3, 10, 5)

if q:
    ans = kn.ask(q, k)

    st.markdown(
        f"**Tema provável (MLP):** `{ans.category}` "
        f"— confiança {ans.category_confidence:.0%}"
    )

    if ans.has_evidence and ans.family:
        st.markdown(f"**Produto (pela fonte):** {ans.family}")

    if not ans.has_evidence:
        st.error(
            "A documentação indexada não traz evidência suficiente "
            "para responder. Isso não prova que a funcionalidade não "
            "exista — consulte a fonte oficial."
        )

    st.subheader("Evidências recuperadas")

    for n, h in enumerate(ans.hits, 1):
        with st.expander(
            f"{n}. {h.title} — pontuação {h.score:.3f}",
            expanded=(n == 1 and ans.has_evidence),
        ):
            st.caption(
                f"Semântica {h.semantic:.2f} · "
                f"Palavras exatas {h.lexical:.2f}"
            )

            st.markdown("**Trecho principal**")
            st.write(h.text)

            if h.context:
                st.divider()
                st.markdown("**Contexto complementar da mesma página**")
                st.write(h.context)
            else:
                st.caption(
                    "Nenhum trecho vizinho disponível para este resultado."
                )

            if h.source.startswith("http"):
                st.markdown(f"[Abrir fonte oficial]({h.source})")
            else:
                st.caption(f"Base-semente curada: {h.source}")

    st.info(
        "Similaridade semântica sugere relevância, não correção técnica. "
        "Confira a fonte e a versão."
    )
