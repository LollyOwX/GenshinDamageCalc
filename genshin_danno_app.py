import streamlit as st
import math

st.set_page_config(page_title="Genshin DMG Calculator", layout="wide")
st.title("⚔️ Genshin Impact - Calcolatore Danno")

st.sidebar.header("📊 Statistiche Personaggio")
base_atk = st.sidebar.number_input("ATK Totale", value=2253)
crit_rate = st.sidebar.number_input("Tasso di CRIT (%)", value=71.6) / 100
crit_dmg = st.sidebar.number_input("Danno CRIT (%)", value=141.0) / 100
anemo_bonus = st.sidebar.number_input("Bonus DAN Elementale (%)", value=46.6) / 100
em = st.sidebar.number_input("Maestria Elementale", value=98)
res_reduction = st.sidebar.number_input("Shred Elementale Nemico (%)", value=0.0) / 100

# Calcolo riduzione resistenza
res_multiplier = 1.0
if res_reduction:
    effective_res = -res_reduction * 100
    if effective_res < 0:
        res_multiplier = 1 - (effective_res / 2 / 100)
    else:
        res_multiplier = 1 - (effective_res / 100)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Attacchi Normali")
num_hits = st.sidebar.selectbox("Numero di Attacchi Normali", range(1, 8), index=2)
normal_attack_multipliers = []
bonus_dmg_per_hit = []
for i in range(num_hits):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        mult = st.number_input(f"Moltiplicatore {i+1} (%)", value=100.0, key=f"mult_{i}")
    with col2:
        bonus = st.number_input(f"Bonus DAN {i+1} (%)", value=0.0, key=f"bonus_{i}") / 100
    normal_attack_multipliers.append(mult)
    bonus_dmg_per_hit.append(bonus)

st.sidebar.subheader("⚡ Attacco Caricato & Burst")
charged_attack_multiplier = st.sidebar.number_input("Moltiplicatore Caricato (%)", value=120.0)
charged_bonus = st.sidebar.number_input("Bonus DAN Caricato (%)", value=15.0) / 100
burst_attack_multiplier = st.sidebar.number_input("Moltiplicatore Burst (%)", value=245.0)
burst_bonus = st.sidebar.number_input("Bonus DAN Burst (%)", value=15.0) / 100

st.header("🧮 Calcolo Danni (senza Reazioni Elementali)")
st.subheader("Attacchi Normali")
for i, mult in enumerate(normal_attack_multipliers):
    bonus_multiplier = 1 + bonus_dmg_per_hit[i] + anemo_bonus
    base = base_atk * (mult / 100) * bonus_multiplier * res_multiplier
    crit = base * (1 + crit_dmg)
    avg = base * (1 + crit_rate * crit_dmg)
    st.write(f"**Attacco Normale {i+1}:**")
    st.write(f"- Danno NON critico: `{base:.1f}`")
    st.write(f"- Danno CRITICO: `{crit:.1f}`")
    st.write(f"- Danno MEDIO: `{avg:.1f}`")

st.subheader("⚔️ Attacco Caricato")
charged_base = base_atk * (charged_attack_multiplier / 100) * (1 + charged_bonus + anemo_bonus) * res_multiplier
charged_crit = charged_base * (1 + crit_dmg)
charged_avg = charged_base * (1 + crit_rate * crit_dmg)
st.write(f"- Danno NON critico: `{charged_base:.1f}`")
st.write(f"- Danno CRITICO: `{charged_crit:.1f}`")
st.write(f"- Danno MEDIO: `{charged_avg:.1f}`")

st.subheader("💥 Elemental Burst")
burst_base = base_atk * (burst_attack_multiplier / 100) * (1 + burst_bonus + anemo_bonus) * res_multiplier
burst_crit = burst_base * (1 + crit_dmg)
burst_avg = burst_base * (1 + crit_rate * crit_dmg)
st.write(f"- Danno NON critico: `{burst_base:.1f}`")
st.write(f"- Danno CRITICO: `{burst_crit:.1f}`")
st.write(f"- Danno MEDIO: `{burst_avg:.1f}`")
