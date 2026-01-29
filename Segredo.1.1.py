import streamlit as st

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Football Studio – IA Ciclo 9 (Leitura Correta)",
    layout="centered"
)

# =====================================================
# STATE
# =====================================================
if "history" not in st.session_state:
    st.session_state.history = []  # antigo -> recente

# =====================================================
# UI INPUT
# =====================================================
st.title("⚽ Football Studio – IA Profissional")

c1, c2, c3 = st.columns(3)
if c1.button("🔴 HOME"):
    st.session_state.history.append("R")
if c2.button("🔵 AWAY"):
    st.session_state.history.append("B")
if c3.button("🟡 DRAW"):
    st.session_state.history.append("D")

# =====================================================
# UTILS
# =====================================================
def icon(x):
    return "🔴" if x == "R" else "🔵" if x == "B" else "🟡"

def get_ciclo_9(hist):
    if len(hist) < 9:
        return None
    return hist[-9:]  # antigo -> recente

# =====================================================
# HISTÓRICO VISUAL
# =====================================================
st.markdown("## 📊 Histórico (Mais recente → Mais antigo)")
visual = list(reversed(st.session_state.history[-30:]))
st.write(" ".join(icon(x) for x in visual))

# =====================================================
# IA – LEITURA DIREITA → ESQUERDA
# =====================================================
def analyze_ciclo_9(c9):
    """
    c9 chega como antigo -> recente
    leitura correta = recente -> antigo
    """
    leitura = list(reversed(c9))  # 🔥 ponto-chave

    r = leitura.count("R")
    b = leitura.count("B")
    d = leitura.count("D")

    alternancias = sum(
        1 for i in range(1, 9) if leitura[i] != leitura[i - 1]
    )

    # 1️⃣ DOMÍNIO ATIVO (6+)
    if leitura[:6].count("R") >= 5:
        return "Domínio ativo 🔴", "R", 75
    if leitura[:6].count("B") >= 5:
        return "Domínio ativo 🔵", "B", 75

    # 2️⃣ ESTRUTURA 6x3 (OLHANDO DO PRESENTE)
    if r == 6 and b == 3:
        dominante = "R" if leitura[0] == "R" else "B"
        return "Estrutura 6x3", dominante, 70

    # 3️⃣ FALSA QUEBRA REAL
    if leitura[0] != leitura[1]:
        base = leitura[1]
        if leitura.count(base) >= 5:
            return "Falsa quebra (retorno)", base, 72

    # 4️⃣ SIMETRIA OCULTA (3–3–3)
    if leitura[0:3] == leitura[3:6] == leitura[6:9]:
        return "Simetria 3x3x3", leitura[0], 76

    # 5️⃣ COMPRESSÃO (ARMADILHA)
    if alternancias >= 6:
        return "Compressão ativa – aguardar", None, 0

    # 6️⃣ PRESSÃO DE DRAW
    if d >= 4:
        return "Pressão estatística de empate", "D", 73

    return "Sem padrão confiável", None, 0

# =====================================================
# DECISÃO FINAL
# =====================================================
st.markdown("## 🎯 Decisão da IA")

c9 = get_ciclo_9(st.session_state.history)

if not c9:
    st.info("⏳ Aguardando 9 resultados")
else:
    pattern, direction, conf = analyze_ciclo_9(c9)

    st.markdown("### 🔄 Ciclo analisado (Direita → Esquerda)")
    st.write(" ".join(icon(x) for x in reversed(c9)))

    st.markdown("### 🧠 Leitura Estrutural")
    st.write(pattern)

    if direction:
        st.success(f"🎯 ENTRADA: {icon(direction)} | Confiança: {conf}%")
    else:
        st.warning("⏳ AGUARDAR – cassino ainda não expôs a intenção")
