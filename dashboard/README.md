# Breathe Barcelona Dashboard

Interactive Streamlit application developed as the productization layer of the **Breathe Barcelona** project.

The dashboard integrates the main temporal and geospatial results of the project into an interactive interface for exploring air quality patterns, model performance, spatial relationships, and predictive outputs.

## Dashboard views

- **Overview** — General overview of NO₂ concentrations, temporal evolution, spatial distribution, and air-quality classes.
- **Temporal** — Temporal patterns, traffic relationships, time-series modelling, and model interpretation.
- **Spatial** — Spatial distribution of NO₂, LISA clusters, spatial associations, regression results, and geospatial predictions.
- **Model Insights** — Performance and interpretability of the temporal classification model, including validation metrics, confusion matrix, SHAP analysis, and LOSO validation.
- **Predictor** — Dual prediction interface combining spatial NO₂ concentration estimation and temporal air-quality classification.

## Files

- `app.py` — Main Streamlit application.
- `requirements.txt` — Python dependencies required to run the dashboard.

The complete development and analytical workflow of the dashboard is documented in:

`../notebooks/ANEXO_7_LF_01_Breathe_Barcelona_Dashboard.ipynb`

## Run locally

Install the required dependencies:

```bash
pip install -r requirements.txt
