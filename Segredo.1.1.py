import streamlit as st

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(
    page_title="Football Studio – IA Ciclo 9",
    layout="centered"
)

# =====================================================
# ESTADO GLOBAL
# =====================================================
if "history" not in st.session_state:
    st.session_state.history = []  # antigo -> recente

# =====================================================
# UI – ENTRADA DE DADOS
# =====================================================
st.title("⚽ Football Studio – IA Profissional (Ciclo 9)")

c1, c2, c3 = st.columns(3)
if c1.button("🔴 HOME"):
    st.session_state.history.append("R")
if c2.button("🔵 AWAY"):
    st.session_state.history.append("B")
if c3.button("🟡 DRAW"):
    st.session_state.history.append("D")

# =====================================================
# UTILIDADES
# =====================================================
def icon(x):
    return "🔴" if x == "R" else "🔵" if x == "B" else "🟡"

def get_last_n(hist, n):
    if len(hist) < n:
        return None
    return hist[-n:]  # antigo -> recente

# =====================================================
# HISTÓRICO VISUAL
# =====================================================
st.markdown("## 📊 Histórico (Mais recente → Mais antigo)")
visual = list(reversed(st.session_state.history[-30:]))
st.write(" ".join(icon(x) for x in visual))

# =====================================================
# IA – ANÁLISE CICLO 9 (ESTRUTURAL)
# =====================================================
def analyze_cycle_9(c9):
    # c9 está em ordem temporal correta (antigo -> recente)

    r = c9.count("R")
    b = c9.count("B")
    d = c9.count("D")

    alternancias = sum(1 for i in range(1, 9) if c9[i] != c9[i-1])

    # -------------------------------------------------
    # 1. REPETIÇÃO DOMINANTE (CONTROLE)
    # -------------------------------------------------
    if r >= 7:
        return "Domínio prolongado 🔴", "R", 75
    if b >= 7:
        return "Domínio prolongado 🔵", "B", 75

    # -------------------------------------------------
    # 2. BLOCO ESTRUTURAL 6 + 3
    # -------------------------------------------------
    if r == 6 and b == 3:
        return "Estrutura 6x3 🔴", "R", 70
    if b == 6 and r == 3:
        return "Estrutura 6x3 🔵", "B", 70

    # -------------------------------------------------
    # 3. FALSA QUEBRA REAL (RETORNO)
    # -------------------------------------------------
    if c9[-1] != c9[-2]:
        dominante = c9[-2]
        if c9.count(dominante) >= 5:
            return "Falsa quebra confirmada", dominante, 72

    # -------------------------------------------------
    # 4. SIMETRIA OCULTA (3–3–3)
    # -------------------------------------------------
    if c9[:3] == c9[3:6] == c9[6:9]:
        return "Simetria 3x3x3", c9[-1], 76

    # -------------------------------------------------
    # 5. COMPRESSÃO (ARMADILHA)
    # -------------------------------------------------
    if alternancias >= 6 and r >= 3 and b >= 3:
        return "Compressão ativa (aguardar)", None, 0

    # -------------------------------------------------
    # 6. PRESSÃO DE EMPATE
    # -------------------------------------------------
    if d >= 4:
        return "Pressão estatística de Draw", "D", 73

    # -------------------------------------------------
    return "Sem padrão confiável", None, 0

# =====================================================
# DECISÃO FINAL
# =====================================================
st.markdown("## 🎯 Decisão da IA")

c9 = get_last_n(st.session_state.history, 9)

if not c9:
    st.info("⏳ Aguardando 9 resultados para análise completa")
else:
    pattern, direction, confidence = analyze_cycle_9(c9)

    st.markdown("### 🔄 Ciclo analisado (Antigo → Recente)")
    st.write(" ".join(icon(x) for x in c9))

    st.markdown("### 🧠 Leitura Estrutural")
    st.write(pattern)

    if direction:
        st.success(f"🎯 ENTRADA: {icon(direction)} | Confiança: {confidence}%")
    else:
        st.warning("⏳ AGUARDAR – cassino ainda não revelou intenção")
