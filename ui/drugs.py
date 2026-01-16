import streamlit as st
from core.drugs.antibioticos import vancomicina, gentamicina, ceftriaxona
from core.drugs.analgosedacion import morfina, midazolam
from core.drugs.vasoactivos import norepinefrina
from core.drugs.anticonvulsivantes import levetiracetam

DRUG_GROUPS = {
    "Antibióticos": {
        "Vancomicina": vancomicina,
        "Gentamicina": gentamicina,
        "Ceftriaxona": ceftriaxona,
    },
    "Analgosedación": {
        "Morfina": morfina,
        "Midazolam": midazolam,
    },
    "Vasoactivos": {
        "Norepinefrina": norepinefrina,
    },
    "Anticonvulsivantes": {
        "Levetiracetam": levetiracetam,
    }
}

def drug_adjustment(patient, fg):
    st.subheader("Ajuste de fármacos")

    group = st.selectbox(
        "Grupo farmacológico",
        list(DRUG_GROUPS.keys())
    )

    drug_name = st.selectbox(
        "Fármaco",
        list(DRUG_GROUPS[group].keys())
    )

    drug = DRUG_GROUPS[group][drug_name]

    st.divider()
    result = drug.adjust(patient, fg)

    st.markdown(f"### {drug_name}")

    if result.get("no_adjustment"):
        st.success("No requiere ajuste por función renal.")

    if "dose" in result:
        st.metric("Dosis / recomendación", result["dose"])

    if "formula" in result:
        st.markdown("**Fórmula farmacocinética:**")
        st.latex(result["formula"])

    if "notes" in result:
        st.info(result["notes"])

    if "warning" in result:
        st.warning(result["warning"])

    if "refs" in result:
        with st.expander("Fuentes"):
            for ref in result["refs"]:
                st.markdown(f"- {ref}")
