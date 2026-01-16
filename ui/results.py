import streamlit as st
from core.renal import calculate_all_methods, select_fg_for_drugs


def renal_results(patient_data: dict):
    st.subheader("Resultados de función renal")

    if patient_data.get("creatinina", 0) <= 0:
        st.info("Ingrese una creatinina válida para calcular función renal.")
        return None

    methods = calculate_all_methods(patient_data)
    fg_data = select_fg_for_drugs(methods)

    # ===============================
    # Selector de visualización
    # ===============================
    modo = st.radio(
        "Mostrar resultados como:",
        ["Rango (recomendado)", "Sin raza", "Con factor racial"],
        horizontal=True
    )

    st.divider()

    # ===============================
    # Cockcroft–Gault
    # ===============================
    if methods["cg"]:
        st.metric(
            "Cockcroft–Gault (peso ajustado)",
            f'{methods["cg"]["ajustado"]} ml/min'
        )
        st.caption(
            f'IBW: {methods["cg"]["ibw"]} kg | '
            f'Peso ajustado: {methods["cg"]["adjbw"]} kg'
        )
    else:
        st.metric("Cockcroft–Gault", "—")

    st.divider()

    # ===============================
    # CKD-EPI
    # ===============================
    if modo == "Sin raza":
        st.metric(
            "CKD-EPI 2021",
            f'{methods["ckd_epi_2021"]} ml/min'
        )

    elif modo == "Con factor racial":
        st.metric(
            "CKD-EPI 2021 (factor racial)",
            f'{methods["ckd_epi_2021_race"]} ml/min'
        )

    else:
        st.metric(
            "CKD-EPI 2021 (sin raza)",
            f'{methods["ckd_epi_2021"]} ml/min'
        )
        st.caption(
            f'Rango estimado: '
            f'{methods["ckd_epi_2021"]} – {methods["ckd_epi_2021_race"]} ml/min'
        )

    st.divider()

    # ===============================
    # MDRD INDEXADO
    # ===============================
    if modo == "Sin raza":
        st.metric(
            "MDRD indexado",
            f'{methods["mdrd"]} ml/min/1.73 m²'
        )

    elif modo == "Con factor racial":
        st.metric(
            "MDRD indexado (factor racial)",
            f'{methods["mdrd_race"]} ml/min/1.73 m²'
        )

    else:
        st.metric(
            "MDRD indexado",
            f'{methods["mdrd"]} ml/min/1.73 m²'
        )
        st.caption(
            f'Rango MDRD indexado: '
            f'{methods["mdrd"]} – {methods["mdrd_race"]} ml/min/1.73 m²'
        )

    st.divider()

    # ===============================
    # MDRD DESINDEXADO
    # ===============================
    if modo == "Sin raza":
        st.metric(
            "MDRD desindexado",
            f'{methods["mdrd_des"]} ml/min'
        )

    elif modo == "Con factor racial":
        st.metric(
            "MDRD desindexado (factor racial)",
            f'{methods["mdrd_des_race"]} ml/min'
        )

    else:
        st.metric(
            "MDRD desindexado",
            f'{methods["mdrd_des"]} ml/min'
        )
        st.caption(
            f'Rango MDRD desindexado: '
            f'{methods["mdrd_des"]} – {methods["mdrd_des_race"]} ml/min'
        )

    st.info(
        "Los rangos reflejan el uso opcional del factor racial. "
        "Se muestran para transparencia clínica y no reemplazan "
        "el juicio clínico."
    )

    st.divider()

    # ===============================
    # FG OPERATIVO PARA FÁRMACOS
    # ===============================
    if fg_data["fg"]:
        st.success(
            f"FG usado para ajuste farmacológico: "
            f"{fg_data['fg']} ml/min "
            f"({fg_data['method']})"
        )
    else:
        st.warning(
            "No se pudo determinar un FG confiable para ajuste farmacológico."
        )

    return fg_data["fg"]
