import streamlit as st

# =====================================
# CONFIG
# =====================================
st.set_page_config(page_title="Football Studio – Ciclo 5 Padrões", layout="centered")

# =====================================
# STATE
# =====================================
if "history" not in st.session_state:
    st.session_state.history = []

# =====================================
# UI INPUT
# =====================================
st.title("⚽ Football Studio – Ciclo 5 com Padrões")

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
    return hist[-5:] if len(hist) >= 5 else None

# =====================================
# HISTÓRICO
# =====================================
st.markdown("## 📊 Histórico")
st.write(" ".join(icon(x) for x in st.session_state.history[-30:]))

# =====================================
# PADRÕES CICLO 5
# =====================================
def detect_pattern(c5):
    r, b, d = c5.count("R"), c5.count("B"), c5.count("D")
    alt = sum(1 for i in range(1, 5) if c5[i] != c5[i-1])

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
        return "Falsa quebra", c5[-2], 63

    # ⚖️ Bloco 3x2
    if r == 3 and b == 2:
        return "Bloco 3x2 🔴", "R", 60
    if b == 3 and r == 2:
        return "Bloco 3x2 🔵", "B", 60

    # 🟡 Pressão de empate
    if d >= 3:
        return "Pressão de empate", "D", 62

    # 🔄 Alternância
    if alt >= 4:
        return "Alternância excessiva", None, 0

    # 🔒 Compressão
    if alt == 3 and r == 2 and b == 3 or alt == 3 and b == 2 and r == 3:
        return "Compressão de padrão", None, 0

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

    st.markdown("### 🔄 Ciclo 5")
    st.write(" ".join(icon(x) for x in c5))

    st.markdown("### 🧠 Padrão Detectado")
    st.write(pattern)

    if direction:
        st.success(f"🎯 ENTRADA: {icon(direction)} | Confiança: {conf}%")
    else:
        st.warning("⏳ AGUARDAR – padrão instável ou armadilha")
