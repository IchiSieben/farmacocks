import streamlit as st
from core.renal import calculate_all_methods, select_fg_for_drugs


def renal_results(patient_data: dict):
    st.subheader("Resultados de función renal")

    # Validación mínima
    if patient_data.get("creatinina", 0) <= 0:
        st.info("Ingrese una creatinina válida para calcular función renal.")
        return None

    # 1️⃣ Calcular TODOS los métodos (informativo)
    methods = calculate_all_methods(patient_data)

    # 2️⃣ Seleccionar FG operativo para fármacos
    fg_data = select_fg_for_drugs(methods, patient_data)

    # 3️⃣ Mostrar resultados
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Cockcroft–Gault",
            f"{methods['cg']} ml/min" if methods["cg"] is not None else "—"
        )
        st.metric(
            "MDRD",
            f"{methods['mdrd']} ml/min" if methods["mdrd"] is not None else "—"
        )

    with col2:
        st.metric(
            "CKD-EPI",
            f"{methods['ckd_epi']} ml/min" if methods["ckd_epi"] is not None else "—"
        )

        if fg_data["valid"]:
            st.caption(f"FG usado para fármacos: {fg_data['method']}")
        else:
            st.warning("No se pudo determinar un FG confiable para ajuste farmacológico.")

    st.divider()

    # 4️⃣ Sugerencias clínicas (UI, no lógica)
    st.subheader("Sugerencias")

    if fg_data["valid"] and fg_data["fg"] < 60:
        st.info(
            "Función renal disminuida. Considere ajuste de fármacos "
            "y monitorización más estrecha."
        )
    else:
        st.info(
            "Interprete los resultados según el contexto clínico del paciente. "
            "Considere edad, estabilidad hemodinámica y escenario clínico."
        )

    st.divider()

    # 5️⃣ Fuentes
    st.subheader("Fuentes bibliográficas")
    st.markdown(
        """
        - KDIGO 2023  
        - UpToDate  
        - Cockcroft & Gault (1976)  
        - Levey et al. (CKD-EPI)
        """
    )

    # 6️⃣ DEVOLVER FG OPERATIVO (SIEMPRE AL FINAL)
    return fg_data["fg"]
