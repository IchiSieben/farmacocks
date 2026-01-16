def adjust(patient, fg):
    if fg >= 50:
        dose = "15–20 mg/kg cada 8–12 h"
    elif fg >= 30:
        dose = "15 mg/kg cada 24 h"
    else:
        dose = "15 mg/kg cada 48 h"
    return {"dose": dose, "notes": "Monitorear niveles", "warning": "Riesgo nefrotoxicidad"}