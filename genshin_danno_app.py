import streamlit as st
import math

st.set_page_config(page_title="Genshin Damage Calculator", layout="centered")
st.title("🔮 Genshin Impact - Damage Calculator")

st.markdown("""
Inserisci le statistiche del personaggio per calcolare il danno di attacchi normali, critici, medi, attacchi caricati, burst e delle reazioni elementali.
""")

# --- Input statistiche base ---
base_atk = st.number_input("**ATK Totale** (Base + Flat)", value=2253)
crit_rate = st.number_input("**Tasso di CRIT (%)**", value=61.6) / 100
crit_dmg = st.number_input("**Danno CRIT (%)**", value=141.0) / 100
em = st.number_input("**Maestria Elementale (EM)**", value=98)
res_shred = st.number_input("**Shred Resistenza Elementale (%)**", value=0.0) / 100


view_option = st.radio("**Visualizzazione Danno**", ["Senza Reazioni Elementali", "Con Reazioni Elementali"])

# --- Talents
# Esempio per Xiao (i valori sono solo a scopo illustrativo)



num_hits = st.selectbox("**Numero di Attacchi Normali da Calcolare**", [1,2,3,4,5,6,7])

# Input per ogni attacco: bonus danno individuale
bonus_dmg_per_hit = []
for i in range(num_hits):
    bonus = st.number_input(f"**Bonus Danno (%) per Attacco Normale {i+1}**", value=15.0) / 100
    bonus_dmg_per_hit.append(bonus)

# Calcolo base
mults = talent_multipliers[talent_lvl][:num_hits]
res_multiplier = 1 + res_shred

st.markdown("### 📈 Risultati Attacchi Normali")
for i, mult in enumerate(mults):
    bonus_multiplier = 1 + bonus_dmg_per_hit[i]
    base = base_atk * (mult / 100) * bonus_multiplier * res_multiplier
    crit = base * (1 + crit_dmg)
    avg = base * (1 + crit_rate * crit_dmg)
    st.write(f"**Attacco Normale {i+1}:**")
    st.write(f"- Danno NON critico: `{base:.1f}`")
    st.write(f"- Danno CRITICO: `{crit:.1f}`")
    st.write(f"- Danno MEDIO: `{avg:.1f}`")

# --- Attacco Caricato ---
st.markdown("### ⚔️ Attacco Caricato")
charged_bonus = st.number_input("**Bonus Danno Attacco Caricato (%)**", value=15.0) / 100
charged_base = base_atk * (charged_multipliers[talent_charged_lvl] / 100) * (1 + charged_bonus) * res_multiplier
charged_crit = charged_base * (1 + crit_dmg)
charged_avg = charged_base * (1 + crit_rate * crit_dmg)
st.write(f"- Danno NON critico: `{charged_base:.1f}`")
st.write(f"- Danno CRITICO: `{charged_crit:.1f}`")
st.write(f"- Danno MEDIO: `{charged_avg:.1f}`")

# --- Elemental Burst ---
st.markdown("### 💥 Elemental Burst")
burst_bonus = st.number_input("**Bonus Danno Elemental Burst (%)**", value=15.0) / 100
burst_base = base_atk * (burst_multipliers[talent_burst_lvl] / 100) * (1 + burst_bonus) * res_multiplier
burst_crit = burst_base * (1 + crit_dmg)
burst_avg = burst_base * (1 + crit_rate * crit_dmg)
st.write(f"- Danno NON critico: `{burst_base:.1f}`")
st.write(f"- Danno CRITICO: `{burst_crit:.1f}`")
st.write(f"- Danno MEDIO: `{burst_avg:.1f}`")

# --- Sezione Reazioni Elementali ---
if view_option == "Con Reazioni Elementali":
    st.markdown("---")
    st.markdown("### 🌪️ Calcolo Reazioni Elementali (Swirl, Overload, Melt, Vaporize, ecc.)")

    reaction_type = st.selectbox("Tipo di Reazione", [
        "Swirl (Dispersione)",
        "Overloaded (Sovraccarico)",
        "Superconduct (Superconduzione)",
        "Electro-Charged",  
        "Burning",
        "Bloom",
        "Hyperbloom",
        "Burgeon",
        "Vaporize (x1.5)",
        "Vaporize (x2.0)",
        "Melt (x1.5)",
        "Melt (x2.0)",
        "Aggravate",
        "Spread"
    ])

    # Reazioni trasformative (base reaction damage scalato da EM e res)
    transformative_base = {
        "Swirl (Dispersione)": 1294,
        "Overloaded (Sovraccarico)": 2041,
        "Superconduct (Superconduzione)": 408,
        "Electro-Charged": 1220,
        "Burning": 1220,
        "Bloom": 2039,
        "Hyperbloom": 3073,
        "Burgeon": 1533
    }

    # Amplificatori (moltiplicatori per reazioni)
    amp_multipliers = {
        "Vaporize (x1.5)": 1.5,
        "Vaporize (x2.0)": 2.0,
        "Melt (x1.5)": 1.5,
        "Melt (x2.0)": 2.0,
        "Aggravate": 1.15,
        "Spread": 1.25
    }

    if reaction_type in transformative_base:
        base_react = transformative_base[reaction_type]
        reaction_bonus = (16 * em) / (2000 + em)
        total = base_react * (1 + reaction_bonus) * res_multiplier
        st.write(f"**Danno da {reaction_type}:** `{total:.1f}`")
    elif reaction_type in amp_multipliers:
        amplif = amp_multipliers[reaction_type]
        avg_bonus = sum(bonus_dmg_per_hit) / num_hits
        base = base_atk * (1 + avg_bonus) * res_multiplier
        reaction_bonus = 1 + ((2.78 * em) / (1400 + em))
        total = base * amplif * reaction_bonus
        st.write(f"**Danno da {reaction_type}:** `{total:.1f}`")
    else:
        st.write("Errore: reazione non supportata.")
