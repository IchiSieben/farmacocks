import math


def cockcroft_gault(patient):
    """
    Cockcroft–Gault (ml/min)
    Usado para ajuste de fármacos
    """
    edad = patient["edad"]
    peso = patient["peso"]
    creat = patient["creatinina"]
    sexo = patient["sexo"]

    if creat <= 0 or edad <= 0 or peso <= 0:
        return None

    fg = ((140 - edad) * peso) / (72 * creat)

    if sexo.lower().startswith("f"):
        fg *= 0.85

    return round(fg, 1)


def mdrd(patient):
    """
    MDRD (ml/min/1.73 m²)
    Informativo
    """
    edad = patient["edad"]
    creat = patient["creatinina"]
    sexo = patient["sexo"]

    if creat <= 0 or edad <= 0:
        return None

    fg = 175 * (creat ** -1.154) * (edad ** -0.203)

    if sexo.lower().startswith("f"):
        fg *= 0.742

    return round(fg, 1)


def ckd_epi(patient):
    """
    CKD-EPI 2009 sin raza
    """
    edad = patient["edad"]
    creat = patient["creatinina"]
    sexo = patient["sexo"].lower()

    if creat <= 0 or edad <= 0:
        return None

    if sexo.startswith("f"):
        k = 0.7
        a = -0.329
        factor_sexo = 1.018
    else:
        k = 0.9
        a = -0.411
        factor_sexo = 1.0

    fg = (
        141
        * min(creat / k, 1) ** a
        * max(creat / k, 1) ** -1.209
        * (0.993 ** edad)
        * factor_sexo
    )

    return round(fg, 1)


def calculate_all_methods(patient):
    """
    Calcula todos los métodos disponibles
    """
    return {
        "cg": cockcroft_gault(patient),
        "mdrd": mdrd(patient),
        "ckd_epi": ckd_epi(patient),
    }


def select_fg_for_drugs(methods, patient):
    """
    Selección del FG a usar para ajuste farmacológico
    Regla clínica: Cockcroft–Gault por defecto
    """
    if methods["cg"] is not None:
        return {
            "fg": methods["cg"],
            "method": "Cockcroft–Gault",
            "valid": True
        }

    return {
        "fg": None,
        "method": None,
        "valid": False
    }
