import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EERSSA · Monitoreo Remoto",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0f1117; }
[data-testid="stSidebar"] { background: #161b27; }
.block-container { padding-top: 0.8rem; }
.stMetric { background: #1e2535; border-radius: 8px; padding: 10px 14px; }
.alert-critical {
    background: rgba(244,67,54,0.12);
    border-left: 4px solid #f44336;
    padding: 10px 14px; margin: 6px 0; border-radius: 6px;
}
.alert-warning {
    background: rgba(255,152,0,0.12);
    border-left: 4px solid #ff9800;
    padding: 10px 14px; margin: 6px 0; border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTES ───────────────────────────────────────────────────────────────
EQUIPOS = {
    "TR-01  (25 MVA)":       {"tipo": "Transformador de Potencia", "color": "#2196F3"},
    "TR-02  (15 MVA)":       {"tipo": "Transformador de Potencia", "color": "#4CAF50"},
    "CH-01  Celda MT":       {"tipo": "Celda de Media Tensión",    "color": "#FF9800"},
    "CH-02  Celda MT":       {"tipo": "Celda de Media Tensión",    "color": "#9C27B0"},
    "BC-01  Condensadores":  {"tipo": "Banco de Condensadores",    "color": "#00BCD4"},
}

LIMITES = {
    "Voltaje (kV)":        {"alerta_min": 13.2, "critico_min": 12.8, "range": (12.0, 14.5)},
    "Corriente (A)":       {"alerta_max": 720,  "critico_max": 780,  "range": (0, 850)},
    "T° Aceite (°C)":      {"alerta_max": 75,   "critico_max": 82,   "range": (20, 95)},
    "THD Voltaje (%)":     {"alerta_max": 5.0,  "critico_max": 7.0,  "range": (0, 10)},
    "Factor de Potencia":  {"alerta_min": 0.88, "critico_min": 0.86, "range": (0.80, 1.0)},
    "Frecuencia (Hz)":     {"alerta_min": 59.7, "critico_min": 59.5, "range": (59.0, 61.0)},
}

VALORES_BASE = {
    "TR-01  (25 MVA)":      [13.65, 425, 64.0, 2.8, 0.940, 60.01],
    "TR-02  (15 MVA)":      [13.72, 310, 58.0, 3.1, 0.920, 59.98],
    "CH-01  Celda MT":      [13.60, 680, 55.0, 4.5, 0.910, 60.00],
    "CH-02  Celda MT":      [13.58, 720, 57.0, 5.2, 0.900, 60.02],
    "BC-01  Condensadores": [13.70, 120, 42.0, 1.2, 0.990, 60.00],
}
RUIDO = [0.06, 12, 1.8, 0.35, 0.010, 0.06]


def _estado(var, val):
    L = LIMITES[var]
    if "critico_max" in L:
        if val >= L["critico_max"]:  return "🔴"
        if val >= L["alerta_max"]:   return "⚠️"
    if "critico_min" in L:
        if val <= L["critico_min"]:  return "🔴"
        if val <= L["alerta_min"]:   return "⚠️"
    return "🟢"


# ─── DATOS ────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=5)
def live_values(equipo: str, tick: int) -> dict:
    b = VALORES_BASE[equipo]
    rng = np.random.default_rng(seed=tick + hash(equipo) % 9999)
    vals = [b[i] + rng.uniform(-RUIDO[i], RUIDO[i]) for i in range(6)]
    keys = list(LIMITES.keys())
    return dict(zip(keys, vals))


@st.cache_data(ttl=3600)
def historico(equipo: str, dias: int) -> pd.DataFrame:
    periods = dias * 24 * 12          # cada 5 min
    idx = pd.date_range(end=datetime.now(), periods=periods, freq="5min")
    rng = np.random.default_rng(seed=42 + hash(equipo) % 999)
    b = VALORES_BASE[equipo]

    volt = b[0] + np.cumsum(rng.normal(0, 0.003, periods))
    volt = np.clip(volt, 12.8, 14.3)

    corr = b[1] + np.cumsum(rng.normal(0, 0.5, periods))
    corr = np.clip(corr, 80, 820)

    temp = b[2] + np.cumsum(rng.normal(0, 0.04, periods))
    temp = np.clip(temp, 35, 90)

    thd = np.abs(b[3] + rng.normal(0, 0.4, periods))
    thd = np.clip(thd, 0.5, 9.5)

    fp = np.clip(b[4] + rng.normal(0, 0.008, periods), 0.82, 1.0)
    freq = np.clip(b[5] + rng.normal(0, 0.05, periods), 59.2, 60.8)

    # eventos simulados
    e1 = int(periods * 0.28)
    e2 = int(periods * 0.61)
    volt[e1:e1+30] -= 0.42
    temp[e2:e2+60] += 13
    thd[e1:e1+30]  += 2.1

    return pd.DataFrame({
        "timestamp":           idx,
        "Voltaje (kV)":        np.round(volt, 3),
        "Corriente (A)":       np.round(corr, 1),
        "T° Aceite (°C)":      np.round(temp, 1),
        "THD Voltaje (%)":     np.round(thd,  2),
        "Factor de Potencia":  np.round(fp,   3),
        "Frecuencia (Hz)":     np.round(freq, 2),
    })


def alertas_df() -> pd.DataFrame:
    return pd.DataFrame([
        {"Timestamp": "2026-05-23 08:42", "Equipo": "CH-02  Celda MT",      "Variable": "THD Voltaje (%)",    "Valor": 5.80,  "Límite": 5.0,  "Severidad": "⚠️ Advertencia", "Estado": "🔴 Activa"},
        {"Timestamp": "2026-05-23 06:17", "Equipo": "TR-01  (25 MVA)",      "Variable": "T° Aceite (°C)",     "Valor": 76.2,  "Límite": 75.0, "Severidad": "⚠️ Advertencia", "Estado": "🔴 Activa"},
        {"Timestamp": "2026-05-22 23:05", "Equipo": "CH-01  Celda MT",      "Variable": "Factor de Potencia", "Valor": 0.872, "Límite": 0.88, "Severidad": "⚠️ Advertencia", "Estado": "✅ Resuelta"},
        {"Timestamp": "2026-05-22 14:30", "Equipo": "TR-02  (15 MVA)",      "Variable": "Voltaje (kV)",       "Valor": 12.95, "Límite": 13.2, "Severidad": "🔴 Crítico",     "Estado": "✅ Resuelta"},
        {"Timestamp": "2026-05-21 09:15", "Equipo": "TR-01  (25 MVA)",      "Variable": "T° Aceite (°C)",     "Valor": 83.1,  "Límite": 82.0, "Severidad": "🔴 Crítico",     "Estado": "✅ Resuelta"},
        {"Timestamp": "2026-05-20 18:44", "Equipo": "CH-02  Celda MT",      "Variable": "Corriente (A)",      "Valor": 725.0, "Límite": 720,  "Severidad": "⚠️ Advertencia", "Estado": "✅ Resuelta"},
        {"Timestamp": "2026-05-19 11:22", "Equipo": "BC-01  Condensadores", "Variable": "Frecuencia (Hz)",    "Valor": 59.48, "Límite": 59.5, "Severidad": "⚠️ Advertencia", "Estado": "✅ Resuelta"},
    ])


INCIDENTES = [
    {
        "id": "INC-2026-031", "fecha": "2026-05-22", "equipo": "TR-02  (15 MVA)",
        "descripcion": "Caída de tensión detectada — alimentador secundario",
        "causa": "Cortocircuito aguas abajo provocó sobrecarga y actuación de protecciones.",
        "duracion": "47 min", "severidad": "Alta", "estado": "Cerrado",
        "acciones": [
            "14:30 — Alarma crítica: Voltaje 12.95 kV (<13.2 kV)",
            "14:31 — Notificación automática a operadores de guardia",
            "14:35 — Desconexión selectiva por protección diferencial",
            "15:10 — Inspección en campo confirma cortocircuito",
            "15:17 — Normalización del servicio. Voltaje: 13.72 kV",
        ],
    },
    {
        "id": "INC-2026-028", "fecha": "2026-05-21", "equipo": "TR-01  (25 MVA)",
        "descripcion": "Temperatura de aceite sobre límite crítico",
        "causa": "Bloqueo parcial del sistema de ventilación forzada (ventiladores 2 y 3 inoperativos).",
        "duracion": "2h 15min", "severidad": "Alta", "estado": "Cerrado",
        "acciones": [
            "09:15 — Alarma crítica: T° aceite 83.1 °C (>82 °C)",
            "09:20 — Reducción automática de carga al 70%",
            "09:25 — Equipo de mantenimiento convocado",
            "10:30 — Reemplazo de ventiladores defectuosos",
            "11:30 — Temperatura normalizada (64°C). Carga al 100%",
        ],
    },
    {
        "id": "INC-2026-025", "fecha": "2026-05-19", "equipo": "CH-01  Celda MT",
        "descripcion": "Factor de potencia bajo límite mínimo",
        "causa": "Incremento sostenido de cargas inductivas en red de distribución zona norte.",
        "duracion": "3h 40min", "severidad": "Media", "estado": "Cerrado",
        "acciones": [
            "08:30 — Alerta temprana: FP 0.872 (<0.88)",
            "09:15 — Activación manual banco condensadores BC-01",
            "09:22 — Factor de potencia normalizado: 0.94",
            "10:30 — Revisión y ajuste planificación de carga",
            "12:10 — Cierre de incidente. FP estable.",
        ],
    },
]

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ EERSSA Monitor")
    st.markdown("*Sistema de Monitoreo Remoto*")
    st.markdown("---")

    equipo_sel = st.selectbox("**Equipo activo**", list(EQUIPOS.keys()))
    st.caption(f"Tipo: {EQUIPOS[equipo_sel]['tipo']}")

    st.markdown("---")
    dias_hist = st.select_slider("Período histórico (días)", [7, 14, 30, 60, 90], value=30)

    st.markdown("---")
    auto_refresh = st.toggle("🔴 Actualización en tiempo real", value=True)
    intervalo = 5
    if auto_refresh:
        intervalo = st.slider("Intervalo (seg)", 3, 30, 5)

    st.markdown("---")
    st.caption(f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    st.caption("Demo v1.0 · EERSSA")

# ─── ENCABEZADO ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(90deg,#0d2137,#1565c0,#0288d1);
     padding:1.1rem 1.4rem;border-radius:10px;margin-bottom:0.8rem;">
  <h2 style="color:white;margin:0;font-size:1.4rem;">
    ⚡ Sistema de Monitoreo Remoto — EERSSA
  </h2>
  <p style="color:#b3e5fc;margin:4px 0 0;font-size:0.85rem;">
    Tiempo real · Análisis histórico · Alertas tempranas · Trazabilidad de incidentes
  </p>
</div>
""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Tiempo Real",
    "📈  Histórico",
    "🔔  Alertas Tempranas",
    "📋  Trazabilidad de Incidentes",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TIEMPO REAL
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"### {equipo_sel} &nbsp;·&nbsp; {EQUIPOS[equipo_sel]['tipo']}")

    @st.fragment(run_every=intervalo if auto_refresh else None)
    def panel_tiempo_real():
        tick = int(time.time() // intervalo)
        vals = live_values(equipo_sel, tick)
        color = EQUIPOS[equipo_sel]["color"]

        # Métricas
        cols = st.columns(6)
        for col, (var, val) in zip(cols, vals.items()):
            est = _estado(var, val)
            fmt = f"{val:.3f}" if var == "Factor de Potencia" else f"{val:.2f}" if "Hz" in var else f"{val:.1f}"
            col.metric(f"{est} {var}", fmt)

        st.markdown("---")

        # Gauges — 3 variables clave
        gauge_cfg = [
            ("Voltaje (kV)",    vals["Voltaje (kV)"],    12.5, 14.5,  13.2,  12.8,  False),
            ("T° Aceite (°C)",  vals["T° Aceite (°C)"],  20,   95,    75,    82,    True),
            ("THD Voltaje (%)",  vals["THD Voltaje (%)"],  0,    10,    5.0,   7.0,   True),
        ]
        gcols = st.columns(3)
        for gcol, (name, val, mn, mx, warn, crit, high_bad) in zip(gcols, gauge_cfg):
            steps = (
                [{"range": [mn, warn], "color": "#1e2535"},
                 {"range": [warn, crit], "color": "#2d2010"},
                 {"range": [crit, mx],   "color": "#2d1010"}]
                if high_bad else
                [{"range": [mn, crit],  "color": "#2d1010"},
                 {"range": [crit, warn], "color": "#2d2010"},
                 {"range": [warn, mx],   "color": "#1e2535"}]
            )
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=val,
                title={"text": name, "font": {"size": 12, "color": "white"}},
                gauge={
                    "axis": {"range": [mn, mx], "tickcolor": "white",
                             "tickfont": {"color": "white"}},
                    "bar": {"color": color},
                    "steps": steps,
                    "threshold": {"line": {"color": "red", "width": 2},
                                  "thickness": 0.75, "value": crit},
                },
                number={"font": {"color": "white", "size": 28}},
            ))
            fig.update_layout(
                height=220, paper_bgcolor="#1e2535",
                margin=dict(l=15, r=15, t=40, b=10),
            )
            gcol.plotly_chart(fig, use_container_width=True)

        st.caption(f"Última actualización: {datetime.now().strftime('%H:%M:%S')}")

    panel_tiempo_real()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — HISTÓRICO
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"### {equipo_sel} &nbsp;·&nbsp; últimos {dias_hist} días")
    df = historico(equipo_sel, dias_hist)
    color = EQUIPOS[equipo_sel]["color"]

    var_sel = st.selectbox("Variable", list(LIMITES.keys()), key="var_hist")
    L = LIMITES[var_sel]

    # Serie temporal
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df[var_sel], mode="lines", name=var_sel,
        line=dict(color=color, width=1),
        fill="tozeroy", fillcolor=f"rgba(33,150,243,0.07)",
    ))
    for lim_key, lim_color, lim_label in [
        ("alerta_max",   "#FF9800", "Límite advertencia"),
        ("critico_max",  "#f44336", "Límite crítico"),
        ("alerta_min",   "#FF9800", "Límite advertencia"),
        ("critico_min",  "#f44336", "Límite crítico"),
    ]:
        if lim_key in L:
            fig.add_hline(y=L[lim_key], line_dash="dash", line_color=lim_color,
                          annotation_text=lim_label,
                          annotation_font_color=lim_color,
                          annotation_position="top right" if "max" in lim_key else "bottom right")

    fig.update_layout(
        paper_bgcolor="#1e2535", plot_bgcolor="#1e2535", font_color="white",
        height=380,
        xaxis=dict(title="Fecha/Hora", gridcolor="#252e42"),
        yaxis=dict(title=var_sel, gridcolor="#252e42"),
        margin=dict(l=60, r=20, t=15, b=50),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Estadísticas
    s = df[var_sel]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Mínimo",   f"{s.min():.2f}")
    c2.metric("Máximo",   f"{s.max():.2f}")
    c3.metric("Promedio", f"{s.mean():.2f}")
    c4.metric("Desv. Est.", f"{s.std():.2f}")
    if "alerta_max" in L:
        exc = int((s > L["alerta_max"]).sum())
    elif "alerta_min" in L:
        exc = int((s < L["alerta_min"]).sum())
    else:
        exc = 0
    c5.metric("Excedencias alerta", exc)

    st.markdown("---")
    st.markdown("#### Mapa de calor — promedio por hora del día")
    df["hora"] = df["timestamp"].dt.hour
    df["dia"]  = df["timestamp"].dt.date.astype(str)
    pivot = df.pivot_table(values=var_sel, index="dia", columns="hora", aggfunc="mean")

    invert = "alerta_min" in L   # green = high is good (FP, Voltaje, Frecuencia)
    fig_h = px.imshow(
        pivot,
        color_continuous_scale="RdYlGn" if invert else "RdYlGn_r",
        labels=dict(x="Hora del día", y="Fecha", color=var_sel),
        aspect="auto",
    )
    fig_h.update_layout(
        paper_bgcolor="#1e2535", font_color="white", height=360,
        margin=dict(l=70, r=20, t=15, b=40),
    )
    st.plotly_chart(fig_h, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ALERTAS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Alertas tempranas del sistema")
    df_a = alertas_df()
    activas   = df_a[df_a["Estado"].str.contains("Activa")]
    resueltas = df_a[df_a["Estado"].str.contains("Resuelta")]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Críticas activas",
              len(activas[activas["Severidad"].str.contains("Crítico")]))
    c2.metric("⚠️ Advertencias activas",
              len(activas[activas["Severidad"].str.contains("Advertencia")]))
    c3.metric("✅ Resueltas (7 días)", len(resueltas))
    c4.metric("Total alertas (7 días)", len(df_a))

    st.markdown("---")
    st.markdown("#### Alertas activas")
    for _, row in activas.iterrows():
        cls = "alert-critical" if "Crítico" in row["Severidad"] else "alert-warning"
        st.markdown(f"""
        <div class="{cls}">
          <strong>{row['Severidad']} &nbsp;·&nbsp; {row['Equipo']}</strong><br>
          Variable: <strong>{row['Variable']}</strong> &nbsp;=&nbsp;
          <strong>{row['Valor']}</strong> &nbsp;(límite: {row['Límite']})
          &nbsp;&nbsp;·&nbsp;&nbsp; {row['Timestamp']}
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Historial completo — últimos 7 días")
    st.dataframe(df_a, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Distribución de alertas por equipo")
    cnt = df_a.groupby(["Equipo", "Severidad"]).size().reset_index(name="n")
    fig_b = px.bar(cnt, x="Equipo", y="n", color="Severidad",
                   color_discrete_map={"🔴 Crítico": "#f44336", "⚠️ Advertencia": "#FF9800"},
                   labels={"n": "Alertas"})
    fig_b.update_layout(
        paper_bgcolor="#1e2535", plot_bgcolor="#1e2535", font_color="white",
        height=280, legend=dict(bgcolor="#1e2535"),
        xaxis=dict(gridcolor="#252e42"), yaxis=dict(gridcolor="#252e42"),
        margin=dict(l=40, r=10, t=15, b=80),
    )
    st.plotly_chart(fig_b, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — INCIDENTES
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Trazabilidad de incidentes")

    c1, c2, c3 = st.columns(3)
    c1.metric("Incidentes (30 días)", len(INCIDENTES))
    c2.metric("Alta severidad",   sum(1 for i in INCIDENTES if i["severidad"] == "Alta"))
    c3.metric("Tiempo prom. resolución", "2h 14min")

    st.markdown("---")

    for inc in INCIDENTES:
        sev_col   = "#f44336" if inc["severidad"] == "Alta"  else "#FF9800"
        est_col   = "#4CAF50" if inc["estado"]    == "Cerrado" else "#2196F3"
        with st.expander(
            f"📋 {inc['id']}  ·  {inc['fecha']}  ·  {inc['equipo']}  —  {inc['descripcion']}"
        ):
            r1, r2, r3 = st.columns([3, 1, 1])
            with r1:
                st.markdown(f"**Causa raíz:** {inc['causa']}")
                st.markdown(f"**Duración total:** `{inc['duracion']}`")
            r2.markdown(
                f"**Severidad:**<br><span style='color:{sev_col};font-weight:bold'>"
                f"{inc['severidad']}</span>", unsafe_allow_html=True)
            r3.markdown(
                f"**Estado:**<br><span style='color:{est_col};font-weight:bold'>"
                f"{inc['estado']}</span>", unsafe_allow_html=True)

            st.markdown("**Línea de tiempo:**")
            for j, accion in enumerate(inc["acciones"]):
                bullet = "🔴" if j == 0 else "🟡" if j == 1 else "🔵"
                st.markdown(f"&nbsp;&nbsp;{bullet}&nbsp; {accion}")

    st.markdown("---")
    st.markdown("#### Incidentes por equipo y tipo de variable")
    df_inc = pd.DataFrame([
        {"Equipo": "TR-01  (25 MVA)",      "Tipo": "Temperatura",        "n": 3},
        {"Equipo": "TR-02  (15 MVA)",      "Tipo": "Voltaje",            "n": 2},
        {"Equipo": "CH-01  Celda MT",      "Tipo": "Factor de Potencia", "n": 1},
        {"Equipo": "CH-02  Celda MT",      "Tipo": "Calidad (THD)",      "n": 2},
        {"Equipo": "BC-01  Condensadores", "Tipo": "Frecuencia",         "n": 1},
    ])
    fig_i = px.bar(df_inc, x="Equipo", y="n", color="Tipo",
                   color_discrete_sequence=px.colors.qualitative.Set2,
                   labels={"n": "Incidentes"})
    fig_i.update_layout(
        paper_bgcolor="#1e2535", plot_bgcolor="#1e2535", font_color="white",
        height=280, legend=dict(bgcolor="#1e2535"),
        xaxis=dict(gridcolor="#252e42"), yaxis=dict(gridcolor="#252e42"),
        margin=dict(l=40, r=10, t=15, b=80),
    )
    st.plotly_chart(fig_i, use_container_width=True)
