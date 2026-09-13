
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==============================================================================
# 1. CONFIGURACIÓN
# ==============================================================================

st.set_page_config(
    page_title="Breathe Barcelona",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

RUTA_APP = Path(__file__).resolve().parent
RUTA_DASHBOARD = RUTA_APP.parent
RUTA_DATOS = RUTA_DASHBOARD / "01_Datos"

ARCHIVO_TEMPORAL = RUTA_DATOS / "dashboard_temporal.parquet"
ARCHIVO_RESUMEN = RUTA_DATOS / "dashboard_resumen_ejecutivo.parquet"
ARCHIVO_MOVILIDAD = RUTA_DATOS / "dashboard_movilidad_diaria.parquet"
ARCHIVO_COVID = RUTA_DATOS / "dashboard_comparativa_covid.parquet"


# ==============================================================================
# 2. ESTILO COMPACTO 16:9
# ==============================================================================

st.markdown(
    """
    <style>

    html, body, [class*="css"] {
        font-size: 13px;
    }

    .stApp {
        background-color: #07111b;
        color: #eef5f8;
    }

    .block-container {
        max-width: 100%;
        padding-top: 0.55rem;
        padding-bottom: 0.35rem;
        padding-left: 1.15rem;
        padding-right: 1.15rem;
    }

    header[data-testid="stHeader"] {
        height: 0px;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    [data-testid="stSidebar"] {
        background-color: #091722;
        width: 245px !important;
    }

    h1 {
        font-size: 2.0rem !important;
        margin-bottom: 0.05rem !important;
    }

    h2 {
        font-size: 1.45rem !important;
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }

    h3 {
        font-size: 1.05rem !important;
        margin-top: 0.15rem !important;
        margin-bottom: 0.15rem !important;
    }

    p {
        margin-bottom: 0.2rem !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 5px;
        margin-top: 0.15rem;
        margin-bottom: 0.25rem;
    }

    button[data-baseweb="tab"] {
        background-color: #0d1d29;
        border-radius: 7px;
        padding: 5px 10px;
        font-size: 12px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 2px solid #38b6d4;
    }

    [data-testid="stMetric"] {
        background-color: #0d1d29;
        border: 1px solid #1c3545;
        border-radius: 9px;
        padding: 9px 12px;
        min-height: 78px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.78rem;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.65rem;
    }

    .compact-card {
        background-color: #0d1d29;
        border: 1px solid #1c3545;
        border-radius: 9px;
        padding: 10px 12px;
    }

    .compact-placeholder {
        background-color: #0d1d29;
        border: 1px dashed #355264;
        border-radius: 9px;
        padding: 10px 12px;
        min-height: 170px;
        color: #9fb3bf;
    }

    .compact-note {
        background-color: #0d1d29;
        border-left: 3px solid #38b6d4;
        border-radius: 7px;
        padding: 8px 10px;
        font-size: 0.82rem;
    }

    hr {
        margin-top: 0.35rem !important;
        margin-bottom: 0.35rem !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==============================================================================
# 3. CARGA
# ==============================================================================

@st.cache_data(show_spinner=False)
def cargar_parquet(ruta):
    if not ruta.exists():
        return None

    df = pd.read_parquet(ruta)

    for c in ["fecha", "FECHA"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")

    return df


df_temporal = cargar_parquet(ARCHIVO_TEMPORAL)
df_resumen = cargar_parquet(ARCHIVO_RESUMEN)
df_movilidad = cargar_parquet(ARCHIVO_MOVILIDAD)
df_covid = cargar_parquet(ARCHIVO_COVID)


# ==============================================================================
# 4. FUNCIONES
# ==============================================================================

def filtrar_temporal(df, anio, periodo):

    if df is None or df.empty:
        return df

    out = df.copy()

    if anio != "Todos" and "AÑO" in out.columns:
        out = out[out["AÑO"] == int(anio)]

    if periodo != "Todos" and "PERIODO" in out.columns:
        out = out[out["PERIODO"] == periodo]

    return out


def media_segura(df, columna):

    if (
        df is None
        or df.empty
        or columna not in df.columns
    ):
        return None

    s = pd.to_numeric(
        df[columna],
        errors="coerce"
    )

    if s.dropna().empty:
        return None

    return s.mean()


def fmt(valor, dec=1, sufijo=""):

    if valor is None or pd.isna(valor):
        return "—"

    return f"{valor:,.{dec}f}{sufijo}"


def aplicar_layout_plotly(fig, altura=280):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#07111b",
        plot_bgcolor="#07111b",
        height=altura,
        margin=dict(
            l=35,
            r=20,
            t=28,
            b=32
        ),
        font=dict(
            size=11
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )

    return fig


# ==============================================================================
# 5. CABECERA COMPACTA
# ==============================================================================

col_titulo, col_estado = st.columns(
    [4.8, 1]
)

with col_titulo:

    st.markdown(
        "## 🌬️ Breathe Barcelona"
    )

    st.caption(
        "Calidad del aire · movilidad · meteorología · "
        "análisis temporal y espacial · 2018–2024"
    )

with col_estado:

    st.markdown(
        """
        <div class="compact-card" style="text-align:center;">
            <b>PROTOTIPO FUNCIONAL</b><br>
            <span style="color:#44d27c;font-size:12px;">
            Datos reales conectados
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
# 6. FILTROS COMPACTOS
# ==============================================================================

f1, f2, f3, f4 = st.columns(
    [1, 1, 1, 3.5]
)

with f1:
    anio = st.selectbox(
        "Año",
        [
            "Todos",
            2018,
            2019,
            2020,
            2021,
            2022,
            2023,
            2024
        ],
        label_visibility="collapsed"
    )

with f2:
    periodo = st.selectbox(
        "Periodo",
        [
            "Todos",
            "Pre-COVID",
            "COVID",
            "Post-COVID"
        ],
        label_visibility="collapsed"
    )

with f3:
    contaminante = st.selectbox(
        "Contaminante",
        [
            "NO2",
            "O3",
            "PM10",
            "PM2.5"
        ],
        label_visibility="collapsed"
    )

with f4:
    st.caption(
        "Filtros globales · EAQI y clasificación se conectarán tras cerrar el modelo temporal."
    )


df_temporal_filtrado = filtrar_temporal(
    df_temporal,
    anio,
    periodo
)


# ==============================================================================
# 7. PESTAÑAS
# ==============================================================================

tabs = st.tabs([
    "1 · Resumen",
    "2 · Temporal",
    "3 · Espacial",
    "4 · Movilidad",
    "5 · Modelos e IA",
    "6 · Simulador",
    "7 · COVID",
    "8 · Metodología"
])


# ==============================================================================
# 1. RESUMEN
# ==============================================================================

with tabs[0]:

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "NO₂ medio",
            fmt(
                media_segura(
                    df_temporal_filtrado,
                    "NO2"
                ),
                1,
                " µg/m³"
            )
        )

    with k2:
        st.metric(
            "O₃ medio",
            fmt(
                media_segura(
                    df_temporal_filtrado,
                    "O3"
                ),
                1,
                " µg/m³"
            )
        )

    with k3:
        st.metric(
            "PM10 medio",
            fmt(
                media_segura(
                    df_temporal_filtrado,
                    "PM10"
                ),
                1,
                " µg/m³"
            )
        )

    with k4:
        st.metric(
            "PM2.5 medio",
            fmt(
                media_segura(
                    df_temporal_filtrado,
                    "PM2.5"
                ),
                1,
                " µg/m³"
            )
        )


    col_izq, col_der = st.columns(
        [2.1, 1]
    )


    with col_izq:

        if (
            df_resumen is not None
            and
            "NO2_medio_ciudad" in df_resumen.columns
        ):

            fig = px.line(
                df_resumen,
                x="anio",
                y="NO2_medio_ciudad",
                markers=True,
                title="Evolución anual del NO₂"
            )

            fig = aplicar_layout_plotly(
                fig,
                altura=300
            )

            fig.update_xaxes(
                dtick=1
            )

            fig.update_yaxes(
                title="µg/m³"
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )


    with col_der:

        st.markdown(
            """
            <div class="compact-card">
                <b>Cobertura del estudio</b><br><br>
                <b>Periodo</b><br>
                2018–2024<br><br>
                <b>Localizaciones</b><br>
                8<br><br>
                <b>Contaminantes</b><br>
                4
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="compact-note">
            Contaminación + meteorología + tráfico + ruido +
            vuelos + actividad marítima integrados en un único maestro.
            </div>
            """,
            unsafe_allow_html=True
        )



# ==============================================================================
# 2. TEMPORAL
# ==============================================================================

with tabs[1]:

    if (
        df_temporal_filtrado is None
        or df_temporal_filtrado.empty
    ):

        st.warning(
            "Sin datos para los filtros seleccionados."
        )

    else:

        # ----------------------------------------------------------------------
        # Serie diaria de ciudad
        # ----------------------------------------------------------------------

        df_serie = (
            df_temporal_filtrado[
                [
                    "fecha",
                    contaminante
                ]
            ]
            .drop_duplicates()
            .groupby(
                "fecha",
                as_index=False
            )[contaminante]
            .mean()
        )


        df_serie["anio"] = (
            df_serie[
                "fecha"
            ]
            .dt.year
        )


        df_serie["mes_num"] = (
            df_serie[
                "fecha"
            ]
            .dt.month
        )


        df_serie["mes_fecha"] = (
            df_serie[
                "fecha"
            ]
            .dt.to_period("M")
            .dt.to_timestamp()
        )


        # ----------------------------------------------------------------------
        # Agregados
        # ----------------------------------------------------------------------

        df_mensual = (
            df_serie
            .groupby(
                "mes_fecha",
                as_index=False
            )[contaminante]
            .mean()
        )


        df_anual = (
            df_serie
            .groupby(
                "anio",
                as_index=False
            )[contaminante]
            .mean()
        )


        df_estacional = (
            df_serie
            .groupby(
                [
                    "anio",
                    "mes_num"
                ],
                as_index=False
            )[contaminante]
            .mean()
        )


        nombres_meses = {
            1: "Ene",
            2: "Feb",
            3: "Mar",
            4: "Abr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Ago",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dic"
        }


        df_estacional[
            "mes"
        ] = (
            df_estacional[
                "mes_num"
            ]
            .map(
                nombres_meses
            )
        )


        # ----------------------------------------------------------------------
        # KPI
        # ----------------------------------------------------------------------

        k1, k2, k3, k4 = st.columns(
            4
        )


        with k1:

            st.metric(
                f"{contaminante} medio",
                fmt(
                    df_serie[
                        contaminante
                    ].mean(),
                    1,
                    " µg/m³"
                )
            )


        with k2:

            st.metric(
                "Máximo mensual",
                fmt(
                    df_mensual[
                        contaminante
                    ].max(),
                    1,
                    " µg/m³"
                )
            )


        with k3:

            st.metric(
                "Mínimo mensual",
                fmt(
                    df_mensual[
                        contaminante
                    ].min(),
                    1,
                    " µg/m³"
                )
            )


        with k4:

            st.metric(
                "Días",
                f"{df_serie['fecha'].nunique():,}"
            )


        # ----------------------------------------------------------------------
        # FILA PRINCIPAL
        # ----------------------------------------------------------------------

        col_a, col_b = st.columns(
            [2.0, 1]
        )


        with col_a:

            fig_t = px.line(
                df_mensual,
                x="mes_fecha",
                y=contaminante,
                title=(
                    f"Evolución mensual · {contaminante}"
                )
            )

            fig_t = aplicar_layout_plotly(
                fig_t,
                altura=260
            )

            fig_t.update_yaxes(
                title="µg/m³"
            )

            st.plotly_chart(
                fig_t,
                width="stretch"
            )


        with col_b:

            fig_anual = px.bar(
                df_anual,
                x="anio",
                y=contaminante,
                text_auto=".1f",
                title="Comparativa anual"
            )

            fig_anual = aplicar_layout_plotly(
                fig_anual,
                altura=260
            )

            fig_anual.update_xaxes(
                dtick=1
            )

            fig_anual.update_yaxes(
                title="µg/m³"
            )

            st.plotly_chart(
                fig_anual,
                width="stretch"
            )


        # ----------------------------------------------------------------------
        # EVOLUCIÓN ESTACIONAL POR AÑO
        # ----------------------------------------------------------------------

        fig_estacional = px.line(
            df_estacional,
            x="mes",
            y=contaminante,
            color="anio",
            markers=True,
            category_orders={
                "mes": [
                    "Ene",
                    "Feb",
                    "Mar",
                    "Abr",
                    "May",
                    "Jun",
                    "Jul",
                    "Ago",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dic"
                ]
            },
            title=(
                f"Patrón mensual comparado por año · {contaminante}"
            )
        )

        fig_estacional = aplicar_layout_plotly(
            fig_estacional,
            altura=245
        )

        fig_estacional.update_yaxes(
            title="µg/m³"
        )

        st.plotly_chart(
            fig_estacional,
            width="stretch"
        )


# ==============================================================================
# 3. ESPACIAL
# ==============================================================================

with tabs[2]:

    c1, c2 = st.columns(
        [2.2, 1]
    )

    with c1:

        st.markdown(
            """
            <div class="compact-placeholder">
            <b>MAPA GEOESPACIAL</b><br><br>
            Se conectará aquí el mapa definitivo de contaminación,
            predicciones, residuos y variables territoriales.
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="compact-placeholder">
            <b>ANÁLISIS TERRITORIAL</b><br><br>
            Renta · densidad · elevación · Moran's I · correlaciones.
            </div>
            """,
            unsafe_allow_html=True
        )



# ==============================================================================
# 4. MOVILIDAD
# ==============================================================================

with tabs[3]:

    fuente = st.radio(
        "Fuente",
        [
            "Tráfico",
            "Ruido",
            "Vuelos",
            "Puerto"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )


    mapa_variables = {

        "Tráfico": (
            "trafico_idw_1000m",
            "Tráfico estimado"
        ),

        "Ruido": (
            "LAeq_idw_1500m",
            "LAeq"
        ),

        "Vuelos": (
            "Vuelos_total",
            "Vuelos diarios"
        ),

        "Puerto": (
            "Puerto_movimientos",
            "Movimientos portuarios"
        )
    }


    variable, etiqueta = (
        mapa_variables[
            fuente
        ]
    )


    df_mov = (
        df_movilidad[
            [
                "fecha",
                variable,
                "NO2_medio_ciudad"
            ]
        ]
        .dropna(
            subset=[
                variable
            ]
        )
        .copy()
    )


    df_mov[
        "anio"
    ] = (
        df_mov[
            "fecha"
        ]
        .dt.year
    )


    df_mov[
        "mes"
    ] = (
        df_mov[
            "fecha"
        ]
        .dt.to_period(
            "M"
        )
        .dt.to_timestamp()
    )


    df_mov_mensual = (
        df_mov
        .groupby(
            "mes",
            as_index=False
        )
        .agg(
            {
                variable:
                    "mean",

                "NO2_medio_ciudad":
                    "mean"
            }
        )
    )


    df_mov_anual = (
        df_mov
        .groupby(
            "anio",
            as_index=False
        )[variable]
        .mean()
    )


    # --------------------------------------------------------------------------
    # KPIs
    # --------------------------------------------------------------------------

    k1, k2, k3, k4 = st.columns(
        4
    )


    with k1:

        st.metric(
            f"{etiqueta} · media",
            fmt(
                df_mov[
                    variable
                ].mean(),
                1
            )
        )


    with k2:

        st.metric(
            "Máximo",
            fmt(
                df_mov[
                    variable
                ].max(),
                1
            )
        )


    with k3:

        st.metric(
            "Mínimo",
            fmt(
                df_mov[
                    variable
                ].min(),
                1
            )
        )


    with k4:

        st.metric(
            "Días disponibles",
            f"{df_mov['fecha'].nunique():,}"
        )


    # --------------------------------------------------------------------------
    # PRIMERA FILA
    # --------------------------------------------------------------------------

    col_a, col_b = st.columns(
        [2, 1]
    )


    with col_a:

        fig_mov = px.line(
            df_mov_mensual,
            x="mes",
            y=variable,
            title=(
                f"Evolución mensual · {etiqueta}"
            )
        )

        fig_mov = aplicar_layout_plotly(
            fig_mov,
            altura=255
        )

        st.plotly_chart(
            fig_mov,
            width="stretch"
        )


    with col_b:

        fig_mov_anual = px.bar(
            df_mov_anual,
            x="anio",
            y=variable,
            text_auto=".1f",
            title="Comparativa anual"
        )

        fig_mov_anual = aplicar_layout_plotly(
            fig_mov_anual,
            altura=255
        )

        fig_mov_anual.update_xaxes(
            dtick=1
        )

        st.plotly_chart(
            fig_mov_anual,
            width="stretch"
        )


    # --------------------------------------------------------------------------
    # RELACIÓN CON NO2
    # --------------------------------------------------------------------------

    if (
        "NO2_medio_ciudad"
        in df_mov_mensual.columns
    ):

        df_scatter = (
            df_mov_mensual
            .dropna(
                subset=[
                    variable,
                    "NO2_medio_ciudad"
                ]
            )
        )


        if len(
            df_scatter
        ) > 2:

            correlacion = (
                df_scatter[
                    [
                        variable,
                        "NO2_medio_ciudad"
                    ]
                ]
                .corr()
                .iloc[
                    0,
                    1
                ]
            )


            fig_rel = px.scatter(
                df_scatter,
                x=variable,
                y="NO2_medio_ciudad",
                trendline="ols",
                title=(
                    f"{etiqueta} vs NO₂ · "
                    f"r = {correlacion:.2f}"
                )
            )


            fig_rel = aplicar_layout_plotly(
                fig_rel,
                altura=245
            )


            fig_rel.update_yaxes(
                title="NO₂ medio (µg/m³)"
            )


            st.plotly_chart(
                fig_rel,
                width="stretch"
            )


# ==============================================================================
# 5. MODELOS E IA
# ==============================================================================

with tabs[4]:

    k1, k2, k3, k4 = st.columns(
        4
    )

    with k1:
        st.metric(
            "Modelo ganador",
            "Pendiente"
        )

    with k2:
        st.metric(
            "F1 macro",
            "Pendiente"
        )

    with k3:
        st.metric(
            "Accuracy",
            "Pendiente"
        )

    with k4:
        st.metric(
            "Interpretabilidad",
            "SHAP"
        )


    c1, c2 = st.columns(
        [1.4, 1]
    )

    with c1:

        st.markdown(
            """
            <div class="compact-placeholder">
            <b>MATRIZ DE CONFUSIÓN / PERFORMANCE</b><br><br>
            Comparación de modelos y métricas por clase.
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="compact-placeholder">
            <b>SHAP GLOBAL</b><br><br>
            Importancia de variables y contribución por bloques.
            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================================================================
# 6. SIMULADOR
# ==============================================================================

with tabs[5]:

    col_inputs, col_pred, col_shap = st.columns(
        [1, 1.25, 1]
    )


    with col_inputs:

        st.markdown(
            "### Escenario"
        )

        st.selectbox(
            "Estación",
            ["Pendiente"]
        )

        st.slider(
            "Tráfico (%)",
            -50,
            50,
            0
        )

        st.slider(
            "Vuelos (%)",
            -50,
            50,
            0
        )

        st.slider(
            "Puerto (%)",
            -50,
            50,
            0
        )


    with col_pred:

        st.markdown(
            """
            <div class="compact-placeholder">
            <b>PREDICCIÓN</b><br><br>
            Clase predicha<br>
            Probabilidades por clase<br>
            Comparación referencia / escenario
            </div>
            """,
            unsafe_allow_html=True
        )


    with col_shap:

        st.markdown(
            """
            <div class="compact-placeholder">
            <b>SHAP LOCAL</b><br><br>
            Factores que explican la predicción individual.
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        """
        <div class="compact-note">
        Los escenarios se interpretarán como predicciones bajo
        valores modificados de entrada y no como estimaciones causales.
        </div>
        """,
        unsafe_allow_html=True
    )



# ==============================================================================
# 7. COVID
# ==============================================================================

with tabs[6]:

    variables_covid = [
        v
        for v in [
            "NO2_medio_ciudad",
            "O3_medio_ciudad",
            "PM10_medio_ciudad",
            "PM25_medio_ciudad",
            "trafico_idw_1000m",
            "LAeq_idw_1500m",
            "Vuelos_total",
            "Puerto_movimientos"
        ]
        if f"{v}_mean" in df_covid.columns
    ]


    variable_covid = st.selectbox(
        "Variable",
        variables_covid,
        label_visibility="collapsed"
    )


    columna_media = (
        f"{variable_covid}_mean"
    )


    columna_mediana = (
        f"{variable_covid}_median"
    )


    columna_count = (
        f"{variable_covid}_count"
    )


    # --------------------------------------------------------------------------
    # TARJETAS DE LOS TRES PERIODOS
    # --------------------------------------------------------------------------

    cols_periodo = st.columns(
        3
    )


    for col, periodo_nombre in zip(
        cols_periodo,
        [
            "Pre-COVID",
            "COVID",
            "Post-COVID"
        ]
    ):

        fila = (
            df_covid[
                df_covid[
                    "periodo_dash"
                ].astype(str)
                ==
                periodo_nombre
            ]
        )


        with col:

            if not fila.empty:

                valor = (
                    fila[
                        columna_media
                    ]
                    .iloc[0]
                )


                st.metric(
                    periodo_nombre,
                    fmt(
                        valor,
                        2
                    )
                )


    # --------------------------------------------------------------------------
    # GRÁFICO COMPARATIVO
    # --------------------------------------------------------------------------

    col_a, col_b = st.columns(
        [1.7, 1]
    )


    with col_a:

        df_plot_covid = (
            df_covid[
                [
                    "periodo_dash",
                    columna_media
                ]
            ]
            .copy()
        )


        fig_covid = px.bar(
            df_plot_covid,
            x="periodo_dash",
            y=columna_media,
            text_auto=".2f",
            title=(
                "Comparativa Pre-COVID · "
                "COVID · Post-COVID"
            )
        )


        fig_covid = aplicar_layout_plotly(
            fig_covid,
            altura=285
        )


        st.plotly_chart(
            fig_covid,
            width="stretch"
        )


    with col_b:

        if columna_mediana in df_covid.columns:

            fig_mediana = px.bar(
                df_covid,
                x="periodo_dash",
                y=columna_mediana,
                text_auto=".2f",
                title="Mediana por periodo"
            )


            fig_mediana = aplicar_layout_plotly(
                fig_mediana,
                altura=285
            )


            st.plotly_chart(
                fig_mediana,
                width="stretch"
            )


    # --------------------------------------------------------------------------
    # COBERTURA
    # --------------------------------------------------------------------------

    if columna_count in df_covid.columns:

        df_cobertura = (
            df_covid[
                [
                    "periodo_dash",
                    columna_count,
                    "dias_totales"
                ]
            ]
            .copy()
        )


        df_cobertura[
            "cobertura_pct"
        ] = (
            df_cobertura[
                columna_count
            ]
            /
            df_cobertura[
                "dias_totales"
            ]
            *
            100
        )


        fig_cov = px.bar(
            df_cobertura,
            x="periodo_dash",
            y="cobertura_pct",
            text_auto=".1f",
            title="Cobertura temporal (%)"
        )


        fig_cov = aplicar_layout_plotly(
            fig_cov,
            altura=205
        )


        fig_cov.update_yaxes(
            range=[
                0,
                105
            ]
        )


        st.plotly_chart(
            fig_cov,
            width="stretch"
        )


    st.markdown(
        """
        <div class="compact-note">
        Comparación descriptiva. Las diferencias observadas
        no se interpretan automáticamente como relaciones causales.
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
# 8. METODOLOGÍA
# ==============================================================================

with tabs[7]:

    cols = st.columns(
        6
    )


    pasos = [
        (
            "1 · DATOS",
            "Fuentes abiertas"
        ),
        (
            "2 · ETL",
            "Limpieza e integración"
        ),
        (
            "3 · EDA",
            "Temporal y espacial"
        ),
        (
            "4 · ML",
            "Modelos comparados"
        ),
        (
            "5 · SHAP",
            "Interpretabilidad"
        ),
        (
            "6 · APP",
            "Productivización"
        )
    ]


    for col, paso in zip(
        cols,
        pasos
    ):

        with col:

            st.markdown(
                f"""
                <div class="compact-card" style="min-height:145px;">
                    <b>{paso[0]}</b><br><br>
                    {paso[1]}
                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown(
        """
        <div class="compact-note">
        Pipeline reproducible desde fuentes abiertas hasta
        visualización, interpretación y generación de nuevas predicciones.
        </div>
        """,
        unsafe_allow_html=True
    )
