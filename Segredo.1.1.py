import streamlit as st

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(page_title="Football Studio – IA REAL", layout="centered")

# =====================================================
# STATE
# =====================================================
if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# UI INPUT
# =====================================================
st.title("⚽ Football Studio – IA REAL")

c1, c2, c3 = st.columns(3)
if c1.button("🔴 HOME"):
    st.session_state.history.insert(0, "R")
if c2.button("🔵 AWAY"):
    st.session_state.history.insert(0, "B")
if c3.button("🟡 DRAW"):
    st.session_state.history.insert(0, "D")

# =====================================================
# UTILS
# =====================================================
def icon(x):
    return "🔴" if x == "R" else "🔵" if x == "B" else "🟡"

def cycle(hist, n):
    return hist[:n] if len(hist) >= n else None

# =====================================================
# FEATURE EXTRACTION
# =====================================================
def extract_features(seq):
    feats = {
        "R": seq.count("R"),
        "B": seq.count("B"),
        "D": seq.count("D"),
        "alternancia": 0,
        "streak_max": 1
    }

    streak = 1
    for i in range(1, len(seq)):
        if seq[i] == seq[i-1]:
            streak += 1
            feats["streak_max"] = max(feats["streak_max"], streak)
        else:
            streak = 1
            if seq[i] != "D" and seq[i-1] != "D":
                feats["alternancia"] += 1
    return feats

# =====================================================
# REGIME – CICLO 7
# =====================================================
def regime_c7(c7):
    f = extract_features(c7)

    if f["D"] >= 3:
        return "DRAW DOMINANTE", 8
    if f["R"] >= 5:
        return "DIREÇÃO 🔴", 7
    if f["B"] >= 5:
        return "DIREÇÃO 🔵", 7
    if f["alternancia"] >= 4:
        return "ALTERNÂNCIA REAL", 6
    if f["D"] == 2:
        return "COMPRESSÃO", 5
    return "NEUTRO / ARMADILHA", 3

# =====================================================
# PROBABILITY ENGINE (IA)
# =====================================================
def probability_engine(hist):
    if len(hist) < 7:
        return None, None, None

    c3 = cycle(hist, 3)
    c5 = cycle(hist, 5)
    c7 = cycle(hist, 7)

    p = {"R": 33.0, "B": 33.0, "D": 34.0}

    f3 = extract_features(c3)
    f5 = extract_features(c5)
    f7 = extract_features(c7)

    # -------- CICLO 7 (REGIME)
    if f7["R"] >= 5: p["R"] += 25
    if f7["B"] >= 5: p["B"] += 25
    if f7["D"] >= 3: p["D"] += 30

    # -------- CICLO 5 (CONFIRMAÇÃO)
    if f5["R"] >= 3: p["R"] += 10
    if f5["B"] >= 3: p["B"] += 10
    if f5["D"] >= 2: p["D"] += 12

    # -------- CICLO 3 (TIMING)
    if f3["alternancia"] == 2:
        if c3[0] == "R": p["B"] += 10
        if c3[0] == "B": p["R"] += 10

    # NORMALIZA
    total = sum(p.values())
    for k in p:
        p[k] = round(p[k] / total * 100, 2)

    return p, c3, c5

# =====================================================
# DECISION ENGINE
# =====================================================
def ia_decision(hist):
    probs, c3, c5 = probability_engine(hist)
    if not probs:
        return "⏳ AGUARDAR", "Histórico insuficiente", None

    best = max(probs, key=probs.get)

    if probs[best] >= 55:
        label = "🔴 HOME" if best == "R" else "🔵 AWAY" if best == "B" else "🟡 DRAW"
        return f"🎯 APOSTAR {label}", f"Probabilidade {probs[best]}%", probs

    return "⏳ AGUARDAR", "Sem vantagem estatística", probs

# =====================================================
# DISPLAY
# =====================================================
st.markdown("## 📊 Histórico")
st.write(" ".join(icon(x) for x in st.session_state.history[:30]))

decision, reason, probs = ia_decision(st.session_state.history)

st.markdown("## 🎯 Decisão da IA")
st.success(f"{decision}\n\n{reason}")

# =====================================================
# PAINEL CICLOS
# =====================================================
if len(st.session_state.history) >= 7:
    st.markdown("## 🔄 Leitura por Ciclos")

    c3 = cycle(st.session_state.history, 3)
    c5 = cycle(st.session_state.history, 5)
    c7 = cycle(st.session_state.history, 7)

    col1, col2, col3 = st.columns(3)

    col1.markdown("### Ciclo 3 (Timing)")
    col1.write(" ".join(icon(x) for x in c3))

    col2.markdown("### Ciclo 5 (Confirmação)")
    col2.write(" ".join(icon(x) for x in c5))

    col3.markdown("### Ciclo 7 (Regime)")
    col3.write(" ".join(icon(x) for x in c7))

    regime, level = regime_c7(c7)

    st.markdown("## 🔥 Mapa de Manipulação")
    st.warning(f"Nível **{level}/9** — {regime}")

# =====================================================
# PROBABILIDADES
# =====================================================
if probs:
    st.markdown("## 📈 Probabilidades")
    st.write(f"🔴 HOME: {probs['R']}%")
    st.write(f"🔵 AWAY: {probs['B']}%")
    st.write(f"🟡 DRAW: {probs['D']}%")

# =====================================================
# PAINEL LEITURA
# =====================================================
st.markdown("## 🎭 Cassino vs Jogador")
st.info(
    "Cassino tenta induzir por ruído e alternância curta.\n\n"
    "Jogador espera regime (7), confirma (5) e entra no timing (3)."
)
