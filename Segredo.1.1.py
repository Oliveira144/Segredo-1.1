import streamlit as st

# =====================================
# CONFIG
# =====================================
st.set_page_config(
    page_title="Football Studio – Ciclo 5 Inteligente",
    layout="centered"
)

# =====================================
# STATE
# =====================================
if "history" not in st.session_state:
    st.session_state.history = []  # ordem REAL: antigo -> recente

# =====================================
# UI INPUT
# =====================================
st.title("⚽ Football Studio – Leitura Correta")

c1, c2, c3 = st.columns(3)
if c1.button("🔴 HOME"):
    st.session_state.history.append("R")
if c2.button("🔵 AWAY"):
    st.session_state.history.append("B")
if c3.button("🟡 DRAW"):
    st.session_state.history.append("D")

# =====================================
# UTILS
# =====================================
def icon(x):
    return "🔴" if x == "R" else "🔵" if x == "B" else "🟡"

def last5(hist):
    if len(hist) < 5:
        return None
    return hist[-5:]  # ordem correta: antigo -> recente

# =====================================
# HISTÓRICO VISUAL (INVERTIDO)
# =====================================
st.markdown("## 📊 Histórico (mais recente → mais antigo)")
visual = list(reversed(st.session_state.history[-30:]))
st.write(" ".join(icon(x) for x in visual))

# =====================================
# PADRÕES – CICLO 5
# =====================================
def detect_pattern(c5):
    # c5 está na ordem correta: antigo -> recente
    r = c5.count("R")
    b = c5.count("B")
    d = c5.count("D")

    alternancias = sum(
        1 for i in range(1, 5) if c5[i] != c5[i - 1]
    )

    # 🔁 Repetição
    if r == 5:
        return "Repetição 🔴", "R", 70
    if b == 5:
        return "Repetição 🔵", "B", 70

    # 🧱 Bloco 4 + 1
    if r == 4:
        return "Bloco 4+1 🔴", "R", 65
    if b == 4:
        return "Bloco 4+1 🔵", "B", 65

    # 🎭 Falsa quebra
    if c5[-1] != c5[-2] and c5.count(c5[-2]) >= 3:
        return "Falsa quebra (retorno)", c5[-2], 63

    # ⚖️ Bloco 3x2
    if r == 3 and b == 2:
        return "Bloco 3x2 🔴", "R", 60
    if b == 3 and r == 2:
        return "Bloco 3x2 🔵", "B", 60

    # 🟡 Pressão de empate
    if d >= 3:
        return "Pressão de empate", "D", 62

    # 🔄 Alternância excessiva
    if alternancias >= 4:
        return "Alternância (armadilha)", None, 0

    # 🔒 Compressão
    if alternancias == 3 and r >= 2 and b >= 2:
        return "Compressão (aguardar explosão)", None, 0

    return "Sem padrão válido", None, 0

# =====================================
# DECISÃO
# =====================================
st.markdown("## 🎯 Leitura do Sistema")

c5 = last5(st.session_state.history)

if not c5:
    st.info("⏳ Aguardando 5 resultados")
else:
    pattern, direction, conf = detect_pattern(c5)

    st.markdown("### 🔄 Ciclo 5 (antigo → recente)")
    st.write(" ".join(icon(x) for x in c5))

    st.markdown("### 🧠 Padrão Detectado")
    st.write(pattern)

    if direction:
        st.success(f"🎯 ENTRADA: {icon(direction)} | Confiança: {conf}%")
    else:
        st.warning("⏳ AGUARDAR – padrão instável ou armadilha")
