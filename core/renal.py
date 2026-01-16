import math

# --------------------------------------------------
# UTILIDADES
# --------------------------------------------------

def body_surface_area(weight, height_cm):
    if weight <= 0 or height_cm <= 0:
        return None
    return math.sqrt((height_cm * weight) / 3600)


def ideal_body_weight(sex, height_cm):
    height_in = height_cm / 2.54
    if sex.lower().startswith("f"):
        return 45.5 + 2.3 * (height_in - 60)
    return 50 + 2.3 * (height_in - 60)


def adjusted_body_weight(weight, ibw):
    if weight <= ibw:
        return weight
    return ibw + 0.4 * (weight - ibw)


# --------------------------------------------------
# COCKCROFT–GAULT
# --------------------------------------------------

def cockcroft_gault(patient):
    edad = patient["edad"]
    peso = patient["peso"]
    creat = patient["creatinina"]
    sexo = patient["sexo"]
    talla = patient["talla"]

    if creat <= 0 or edad <= 0 or peso <= 0:
        return None

    ibw = ideal_body_weight(sexo, talla)
    adjbw = adjusted_body_weight(peso, ibw)

    factor = 0.85 if sexo.lower().startswith("f") else 1.0

    cg_real = ((140 - edad) * peso) / (72 * creat) * factor
    cg_adj = ((140 - edad) * adjbw) / (72 * creat) * factor

    return {
        "real": round(cg_real, 1),
        "ajustado": round(cg_adj, 1),
        "ibw": round(ibw, 1),
        "adjbw": round(adjbw, 1),
    }


# --------------------------------------------------
# MDRD
# --------------------------------------------------

def mdrd(patient, with_race=False):
    edad = patient["edad"]
    creat = patient["creatinina"]
    sexo = patient["sexo"]

    if creat <= 0 or edad <= 0:
        return None

    fg = 175 * (creat ** -1.154) * (edad ** -0.203)

    if sexo.lower().startswith("f"):
        fg *= 0.742

    if with_race:
        fg *= 1.212

    return fg


def mdrd_desindexado(patient, with_race=False):
    fg = mdrd(patient, with_race)
    sc = body_surface_area(patient["peso"], patient["talla"])

    if fg is None or sc is None:
        return None

    return round(fg * (sc / 1.73), 1)


# --------------------------------------------------
# CKD-EPI
# --------------------------------------------------

def ckd_epi_2021(patient, with_race=False):
    edad = patient["edad"]
    scr = patient["creatinina"]
    sexo = patient["sexo"].lower()

    if scr <= 0 or edad <= 0:
        return None

    if sexo.startswith("f"):
        k = 0.7
        a = -0.241 if scr <= 0.7 else -1.2
        factor_sexo = 1.012
    else:
        k = 0.9
        a = -0.302 if scr <= 0.9 else -1.2
        factor_sexo = 1.0

    fg = (
        142
        * (min(scr / k, 1) ** a)
        * (max(scr / k, 1) ** -1.2)
        * (0.9938 ** edad)
        * factor_sexo
    )

    if with_race:
        fg *= 1.159

    return round(fg, 1)


# --------------------------------------------------
# CONSOLIDADO
# --------------------------------------------------

def calculate_all_methods(patient):
    cg = cockcroft_gault(patient)

    return {
        "cg": cg,
        "ckd_epi_2021": ckd_epi_2021(patient, False),
        "ckd_epi_2021_race": ckd_epi_2021(patient, True),
        "mdrd": round(mdrd(patient, False), 1) if mdrd(patient) else None,
        "mdrd_race": round(mdrd(patient, True), 1) if mdrd(patient) else None,
        "mdrd_des": mdrd_desindexado(patient, False),
        "mdrd_des_race": mdrd_desindexado(patient, True),
    }


def select_fg_for_drugs(methods):
    if methods["cg"]:
        return {
            "fg": methods["cg"]["ajustado"],
            "method": "Cockcroft–Gault (peso ajustado)"
        }

    return {"fg": None, "method": None}
