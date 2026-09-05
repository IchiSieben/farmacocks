# farmacocks

A Streamlit tool for the two calculations an intensive care team repeats all day:
estimate a patient's renal function, then adjust drug dosing to it.

Both halves normally live apart — renal function in one calculator, dosing in a
table or a memorised rule. Here the second reads the first. You enter the patient
once, and every drug card recalculates against the filtration rate the app just
computed.

## What it does

**Renal function.** Three estimators over the same patient, side by side, because
they disagree and the disagreement is clinically informative: Cockcroft-Gault,
CKD-EPI and MDRD. Cockcroft-Gault is computed on real, ideal and adjusted body
weight, since which weight you feed it changes the answer materially in obese
patients. Ideal body weight uses the Devine formula and adjusted body weight the
standard `IBW + 0.4 x (weight - IBW)`.

**Drug adjustment.** Seven drugs, grouped by therapeutic class, each one a small
module that receives the patient and the filtration rate and returns a dose, a
monitoring note and a warning:

| Class | Drugs |
|---|---|
| Antibiotics | vancomycin, gentamicin, ceftriaxone |
| Analgesia and sedation | morphine, midazolam |
| Anticonvulsants | levetiracetam |
| Vasoactive | norepinephrine |

Each module is a single `adjust(patient, fg)` function that maps filtration
thresholds to a dosing band. Adding a drug means adding one file, not touching the
application.

## Stack

Python 3.10 and Streamlit. Nothing else: no database, no API keys, no network
calls, no patient data stored anywhere. The whole app is standard library plus
Streamlit.

## Structure

```
app.py                  entry point, two tabs
core/renal.py           Cockcroft-Gault, CKD-EPI, MDRD, BSA, IBW, AdjBW
core/drugs/<class>/     one module per drug, each exposing adjust(patient, fg)
ui/inputs.py            patient form
ui/results.py           renal function panel
ui/drugs.py             drug cards
```

The split is deliberate: `core/` holds the formulas and knows nothing about
Streamlit, so the calculations are testable and reusable outside the app.

## How to run

```bash
pip install streamlit
streamlit run app.py
```

That is the whole setup. The app opens on the renal function tab; fill in age, sex,
weight, height and serum creatinine, then switch to the dosing tab.

## Scope and limitations

This is a **decision-support aid, not a prescribing authority**. It reproduces
published formulas and dosing bands; it does not know the patient's history, their
other drugs, or anything the chart says. Clinical judgement decides.

Three specific caveats worth stating plainly:

- **Creatinine-based estimates assume steady state.** In acute kidney injury,
  where creatinine is still moving, all three estimators lag the real filtration
  rate and will read falsely high.
- **The dosing bands are coarse by design.** They are threshold rules, not
  pharmacokinetic modelling. Vancomycin and gentamicin in particular are dosed to
  measured levels in practice, which is why their cards carry a monitoring note.
- **No test suite.** The formulas are transcribed from standard references but are
  not covered by automated tests.

The interface is in Spanish; this README is in English.
