import streamlit as st

def patient_inputs():
    st.subheader("Datos del paciente")

    col1, col2, col3 = st.columns(3)

    with col1:
        sexo = st.selectbox("Sexo", ["", "Masculino", "Femenino"])
        peso = st.number_input("Peso (kg)", min_value=0.0)
        otros = st.multiselect(
            "Otros",
            ["Uso de diuréticos", "UCI", "Sepsis", "Embarazo"]
        )

    with col2:
        edad = st.number_input("Edad (años)", min_value=0)
        talla = st.number_input("Talla (cm)", min_value=0.0)
        diuresis = st.number_input("Diuresis (ml)", min_value=0.0)

    with col3:
        creatinina = st.number_input("Creatinina (mg/dL)", min_value=0.0)
        urea = st.number_input("Urea (mg/dL)", min_value=0.0)
        albumina = st.number_input("Albúmina (g/dL)", min_value=0.0)

    return {
        "sexo": sexo,
        "edad": edad,
        "peso": peso,
        "talla": talla,
        "creatinina": creatinina,
        "urea": urea,
        "albumina": albumina,
        "diuresis": diuresis,
        "otros": otros,
    }
