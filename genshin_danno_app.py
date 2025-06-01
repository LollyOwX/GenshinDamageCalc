import streamlit as st
import math

st.set_page_config(page_title="Genshin Damage Calculator", layout="centered")
st.title("🔮 Genshin Impact - Damage Calculator")

st.markdown("""
Inserisci le statistiche del personaggio per calcolare il danno di attacchi normali, critici, medi e delle reazioni elementali.
""")

# --- Input statistiche base ---
base_atk = st.number_input("**ATK Totale** (Base + Flat)", value=2253)
crit_rate = st.number_input("**Tasso di CRIT (%)**", value=61.6) / 100
crit_dmg = st.number_input("**Danno CRIT (%)**", value=141.0) / 100
em = st.number_input("**Maestria Elementale (EM)**", value=98)
res_shred = st.number_input("**Shred Resistenza Elementale (%)**", value=0.0) / 100

talent_lvl = st.selectbox("**Livello Talento Normale**", [1,2,3,4,5,6,7,8,9,10])

view_option = st.radio("**Visualizzazione Danno**", ["Senza Reazioni Elementali", "Con Reazioni Elementali"])

# --- Talents
# Esempio per Xiao (i valori sono solo a scopo illustrativo)
talent_multipliers = {
    1: [44.5, 43.5, 54.2, 65.5, 64.2, 82.0, 104.1],
    2: [47.2, 46.1, 57.4, 69.4, 68.0, 86.9, 110.4],
    3: [50.0, 48.9, 61.0, 73.7, 72.3, 92.3, 117.3],
    4: [53.4, 52.2, 65.1, 78.6, 77.1, 98.4, 125.1],
    5: [56.1, 54.9, 68.3, 82.5, 81.0, 103.3, 131.4],
    6: [58.9, 57.7, 71.6, 86.5, 84.9, 108.3, 137.8],
    7: [62.3, 61.0, 75.6, 91.3, 89.7, 114.3, 145.6],
    8: [65.7, 64.3, 79.6, 96.1, 94.5, 120.2, 153.4],
    9: [69.0, 67.6, 83.7, 100.9, 99.2, 126.2, 161.2],
    10: [72.4, 71.0, 87.7, 105.7, 104.0, 132.2, 169.0],
}

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
        "Electro-Charged",
        "Burning",
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
        # usare la media dei bonus danno se più attacchi
        avg_bonus = sum(bonus_dmg_per_hit) / num_hits
        base = base_atk * (1 + avg_bonus) * res_multiplier
        reaction_bonus = 1 + ((2.78 * em) / (1400 + em))
        total = base * amplif * reaction_bonus
        st.write(f"**Danno da {reaction_type}:** `{total:.1f}`")
    else:
        st.write("Errore: reazione non supportata.")
