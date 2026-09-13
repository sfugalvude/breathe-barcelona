# Notebooks

This directory contains the complete analytical workflow of **Breathe Barcelona**, from data preprocessing and integration to temporal modelling, spatial analysis, and dashboard development.

The notebooks are organized according to the logical sequence of the project.

## Analytical workflow

### 1. Data preprocessing and source integration
**`ANEXO_1_LF_01_ETL_Preprocesamiento_Fuentes.ipynb`**

Preprocessing and harmonization of the temporal data sources used in the project, including air quality, meteorology, road traffic, environmental noise, air traffic, and maritime activity.

### 2. Temporal master dataset
**`ANEXO_2_LF_02_ETL_Integracion_Dataset_Maestro.ipynb`**

Integration of the processed temporal sources into the master analytical dataset used for exploratory analysis and temporal modelling.

### 3. Temporal NO₂ classification
**`ANEXO_3_LF_03_Modelo_Temporal_Clasificacion_NO2.ipynb`**

Development and evaluation of the temporal air-quality classification model using XGBoost and SMOTE. Includes temporal validation, leave-one-station-out (LOSO) validation, class-level performance analysis, and SHAP interpretability.

### 4. Time-series modelling
**`ANEXO_4_LF_04_Modelos_Series_Temporales.ipynb`**

Time-series modelling of NO₂, PM10, and PM2.5 concentrations using SARIMAX models with exogenous urban and meteorological variables. Performance is evaluated through rolling validation and comparison against a persistence baseline.

### 5. Geospatial data preprocessing
**`ANEXO_5_LF_01_Preprocesado_Fuentes_Geoespaciales.ipynb`**

Preparation and harmonization of the geospatial data sources, including air pollution, traffic, socioeconomic variables, land use, and elevation data.

### 6. Geospatial integration and analysis
**`ANEXO_6_LF_02_Integración_y_análisis_geoespacial.ipynb`**

Spatial integration at census-section level and development of the geospatial analytical workflow, including Local Moran's I (LISA), bivariate spatial association, spatial regression (SAR), XGBoost, and SHAP interpretation.

### 7. Breathe Barcelona dashboard
**`ANEXO_7_LF_01_Breathe_Barcelona_Dashboard.ipynb`**

Development of the interactive **Breathe Barcelona** dashboard, integrating temporal and spatial results into a decision-support interface with exploratory views, model insights, and the Dual Predictor.

## Workflow overview

`Open data → ETL & preprocessing → Temporal master dataset → Temporal modelling → Geospatial modelling → Model interpretation → Interactive dashboard`

## Reproducibility

The notebooks preserve the main analytical outputs used in the final report and dashboard. The workflow relies on public open-data sources and is structured to provide traceability between data preparation, modelling, validation, interpretation, and final visualization.

> **Note:** Some notebooks require access to the original open datasets and project-specific directory paths to reproduce the complete workflow from scratch.
