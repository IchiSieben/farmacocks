# Farmacocks

A small Streamlit tool for ICU/critical-care pharmacology: it estimates renal function
(Cockcroft-Gault, MDRD, CKD-EPI 2021) from patient data, then uses the result to suggest
dose adjustments for a handful of drugs commonly used in intensive care (antibiotics,
sedation/analgesia, vasoactives, anticonvulsants).

The name is a portmanteau of "Farma" and Cockcroft-Gault, the formula the dose-adjustment
tab relies on by default.

**This is a reference/teaching aid, not a certified medical device.** It has no clinical
validation and should not be used to make real dosing decisions without a qualified
clinician reviewing the output.

## What it does

- `app.py` is the Streamlit entry point with two tabs: "Función renal" (renal function)
  and "Ajuste de fármacos" (drug adjustment).
- `core/renal.py` implements Cockcroft-Gault (real and adjusted body weight), MDRD, and
  CKD-EPI 2021, plus body-surface-area / ideal-body-weight / adjusted-body-weight helpers.
- `core/drugs/<category>/<drug>.py` each expose an `adjust(patient, fg)` function that
  returns a dose recommendation, notes, warnings and references given the calculated
  glomerular filtration rate. Categories present today: `antibioticos` (vancomicina,
  gentamicina, ceftriaxona), `analgosedacion` (morfina, midazolam), `vasoactivos`
  (norepinefrina), `anticonvulsivantes` (levetiracetam).
- `ui/` holds the Streamlit views (patient inputs, renal results, drug-adjustment panel).

**Note on `estructura_proyecto.txt`:** that file describes a larger planned layout
(`core/rules.py`, `core/units.py`, `core/enums.py`, `data/bibliography.py`, a
`dopamina.py` and `fenitoina.py` module, etc.) that doesn't match what's actually in the
repo. It's left as-is (a planning note, not touched per scope of this cleanup) — treat the
directory listing above, not that file, as the source of truth for what exists today.

## Running it

Requires Python 3.12+ (developed and verified against 3.12.10) and Streamlit. There is no
`requirements.txt` in the repo; the only third-party dependency actually imported is
`streamlit`.

```bash
pip install streamlit
streamlit run app.py
```

**Verified:** a fresh virtualenv with `streamlit` installed, `python -m py_compile` over
every `.py` file present in the repo (all pass), and `streamlit run app.py --server.headless
true` serving `HTTP 200` on `localhost:8501` with no import errors. Manually exercising
every input combination in the UI was not done.

No database, external API, or network access is required — everything runs client-side
in the Streamlit process.

## Clinical sources

Each drug module can return a `refs` list, shown in an expander in the UI, with the
sources behind that specific dosing rule. There's no single consolidated bibliography
file in the repo today (see the note above about `estructura_proyecto.txt`).

## Author

Yoichi Palacios Tanaka (IchiSieben) · [ichisieben.dev](https://ichisieben.dev)

## Licence

Apache License 2.0 — see [LICENSE](LICENSE).

---

## Español

Una pequeña herramienta en Streamlit de farmacología para cuidados intensivos: estima la
función renal (Cockcroft-Gault, MDRD, CKD-EPI 2021) a partir de datos del paciente, y usa
ese resultado para sugerir ajustes de dosis en un grupo reducido de fármacos de uso
frecuente en UCI (antibióticos, sedoanalgesia, vasoactivos, anticonvulsivantes).

El nombre es un juego de palabras entre "Farma" y Cockcroft-Gault, la fórmula que usa por
defecto la pestaña de ajuste de fármacos.

**Es una herramienta de referencia/apoyo docente, no un dispositivo médico certificado.**
No tiene validación clínica y no debe usarse para decisiones reales de dosificación sin
la revisión de un profesional calificado.

### Qué hace

- `app.py` es el punto de entrada de Streamlit, con dos pestañas: "Función renal" y
  "Ajuste de fármacos".
- `core/renal.py` implementa Cockcroft-Gault (peso real y ajustado), MDRD y CKD-EPI 2021,
  además de utilidades de superficie corporal, peso ideal y peso ajustado.
- `core/drugs/<categoría>/<fármaco>.py` exponen cada uno una función `adjust(patient, fg)`
  que devuelve dosis recomendada, notas, advertencias y referencias según el filtrado
  glomerular calculado. Categorías presentes hoy: `antibioticos` (vancomicina,
  gentamicina, ceftriaxona), `analgosedacion` (morfina, midazolam), `vasoactivos`
  (norepinefrina), `anticonvulsivantes` (levetiracetam).
- `ui/` contiene las vistas de Streamlit (datos del paciente, resultados renales, panel
  de ajuste de fármacos).

**Nota sobre `estructura_proyecto.txt`:** ese archivo describe una estructura planeada más
grande (`core/rules.py`, `core/units.py`, `core/enums.py`, `data/bibliography.py`, un
módulo `dopamina.py` y `fenitoina.py`, etc.) que no coincide con lo que realmente hay en
el repo. Se dejó tal cual (es una nota de planificación, no se tocó por estar fuera del
alcance de esta limpieza) — la lista de arriba, no ese archivo, es la fuente de verdad de
lo que existe hoy.

### Cómo correrlo

Requiere Python 3.12+ (desarrollado y verificado contra 3.12.10) y Streamlit. El repo no
tiene `requirements.txt`; la única dependencia de terceros que realmente se importa es
`streamlit`.

```bash
pip install streamlit
streamlit run app.py
```

**Verificado:** un entorno virtual nuevo con `streamlit` instalado, `python -m py_compile`
sobre todos los `.py` presentes en el repo (todos pasan), y `streamlit run app.py
--server.headless true` sirviendo `HTTP 200` en `localhost:8501` sin errores de
importación. No se probó manualmente cada combinación de entradas de la interfaz.

No requiere base de datos, API externa ni acceso a red: todo corre del lado del proceso
de Streamlit.

### Fuentes clínicas

Cada módulo de fármaco puede devolver una lista `refs`, mostrada en un expansor de la
interfaz, con las fuentes detrás de esa regla de dosificación específica. Hoy no hay un
archivo de bibliografía consolidado en el repo (ver la nota de arriba sobre
`estructura_proyecto.txt`).

### Autor

Yoichi Palacios Tanaka (IchiSieben) · [ichisieben.dev](https://ichisieben.dev)

### Licencia

Apache License 2.0 — ver [LICENSE](LICENSE).
