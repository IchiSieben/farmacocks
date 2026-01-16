def adjust(patient, fg):
    if fg >= 80:
        dose = "500–1500 mg c/12h"
    elif fg >= 30:
        dose = "500–1000 mg c/12h"
    else:
        dose = "250–500 mg c/12h"
    return {"dose": dose, "notes": "Ajustar en IR"}