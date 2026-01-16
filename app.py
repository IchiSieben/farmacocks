import streamlit as st

from ui.inputs import patient_inputs
from ui.results import renal_results
from ui.drugs import drug_adjustment


# --------------------------------------------------
# Configuración general
# --------------------------------------------------
st.set_page_config(
    page_title="Farma Intensiva",
    layout="wide"
)

st.title("🧪 Farma Intensiva")
st.caption("Soporte clínico para función renal y ajuste farmacológico")

# --------------------------------------------------
# Pestañas principales
# --------------------------------------------------
tab_renal, tab_drugs = st.tabs([
    "Función renal",
    "Ajuste de fármacos"
])

# --------------------------------------------------
# TAB 1: FUNCIÓN RENAL
# --------------------------------------------------
with tab_renal:
    st.subheader("Evaluación de función renal")

    patient_data = patient_inputs()

    st.divider()

    # renal_results debe devolver el FG calculado
    fg = renal_results(patient_data)

    # Guardamos el FG para usarlo en otras pestañas
    if fg is not None:
        st.session_state["fg"] = fg


# --------------------------------------------------
# TAB 2: AJUSTE DE FÁRMACOS
# --------------------------------------------------
with tab_drugs:
    st.subheader("Ajuste de fármacos")

    if "fg" not in st.session_state:
        st.warning(
            "⚠️ Primero calcule la función renal en la pestaña "
            "**Función renal** para poder ajustar fármacos."
        )
    else:
        drug_adjustment(patient_data, fg)

