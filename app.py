import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import time

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Monitoreo Remoto — UPS · Generadores · A/C",
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
    background: rgba(244,67,54,0.12); border-left: 4px solid #f44336;
    padding: 10px 14px; margin: 6px 0; border-radius: 6px;
}
.alert-warning {
    background: rgba(255,152,0,0.12); border-left: 4px solid #ff9800;
    padding: 10px 14px; margin: 6px 0; border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# ─── CATÁLOGO DE EQUIPOS ──────────────────────────────────────────────────────
EQUIPOS = {
    # UPS
    "UPS-01  (80 kVA)":  {"tipo": "UPS", "color": "#2196F3",  "grupo": "UPS"},
    "UPS-02  (40 kVA)":  {"tipo": "UPS", "color": "#03A9F4",  "grupo": "UPS"},
    # Generadores
    "GEN-01  (250 kVA)": {"tipo": "Generador", "color": "#4CAF50", "grupo": "Generador"},
    "GEN-02  (150 kVA)": {"tipo": "Generador", "color": "#8BC34A", "grupo": "Generador"},
    # Aires acondicionados
    "AC-01  Sala Serv.":  {"tipo": "Aire Acondicionado", "color": "#FF9800", "grupo": "A/C"},
    "AC-02  Sala UPS":    {"tipo": "Aire Acondicionado", "color": "#FF5722", "grupo": "A/C"},
    "AC-03  Sala Gen.":   {"tipo": "Aire Acondicionado", "color": "#F44336", "grupo": "A/C"},
}

# Variables y límites por tipo de equipo
VARS_UPS = {
    "Voltaje Entrada (V)":  {"alerta_min": 195, "critico_min": 185, "alerta_max": 235, "critico_max": 245, "range": (170, 260)},
    "Voltaje Salida (V)":   {"alerta_min": 218, "critico_min": 210, "alerta_max": 222, "critico_max": 230, "range": (200, 240)},
    "Corriente Salida (A)": {"alerta_max": 180, "critico_max": 200, "range": (0, 220)},
    "Nivel Batería (%)":    {"alerta_min": 30,  "critico_min": 15,  "range": (0, 100)},
    "T° Batería (°C)":      {"alerta_max": 35,  "critico_max": 40,  "range": (15, 50)},
    "Autonomía (min)":      {"alerta_min": 20,  "critico_min": 10,  "range": (0, 120)},
}

VARS_GEN = {
    "Voltaje (V)":          {"alerta_min": 210, "critico_min": 200, "alerta_max": 230, "critico_max": 240, "range": (180, 260)},
    "Frecuencia (Hz)":      {"alerta_min": 59.5,"critico_min": 59.0,"alerta_max": 60.5,"critico_max": 61.0,"range": (57, 63)},
    "T° Aceite (°C)":       {"alerta_max": 90,  "critico_max": 100, "range": (20, 120)},
    "Nivel Combustible (%)":{"alerta_min": 25,  "critico_min": 15,  "range": (0, 100)},
    "RPM":                  {"alerta_min": 1450,"critico_min": 1400,"alerta_max": 1550,"critico_max": 1600,"range": (1300, 1700)},
    "Potencia Activa (kW)": {"alerta_max": 210, "critico_max": 240, "range": (0, 260)},
}

VARS_AC = {
    "T° Ambiente (°C)":     {"alerta_max": 24,  "critico_max": 27,  "range": (15, 35)},
    "T° Setpoint (°C)":     {"range": (16, 28)},
    "Humedad Relativa (%)": {"alerta_max": 60,  "critico_max": 70,  "alerta_min": 30, "critico_min": 20, "range": (10, 90)},
    "Corriente Comp. (A)":  {"alerta_max": 18,  "critico_max": 22,  "range": (0, 25)},
    "T° Evaporador (°C)":   {"alerta_min": 5,   "critico_min": 2,   "range": (-5, 20)},
    "Presión Refrig. (bar)":{"alerta_min": 3.0, "critico_min": 2.5, "alerta_max": 8.0,"critico_max": 9.0, "range": (1, 12)},
}

VARS_POR_TIPO = {"UPS": VARS_UPS, "Generador": VARS_GEN, "Aire Acondicionado": VARS_AC}

# Valores base para simulación
BASE = {
    "UPS-01  (80 kVA)":  [220, 220, 140, 85, 28, 65],
    "UPS-02  (40 kVA)":  [218, 220, 80,  92, 26, 80],
    "GEN-01  (250 kVA)": [220, 60.0, 82, 60, 1500, 185],
    "GEN-02  (150 kVA)": [219, 60.0, 75, 70, 1498, 110],
    "AC-01  Sala Serv.":  [21.5, 20.0, 48, 12.0, 8.5, 5.8],
    "AC-02  Sala UPS":    [22.0, 20.0, 50, 13.0, 9.0, 6.0],
    "AC-03  Sala Gen.":   [23.0, 22.0, 55, 14.0, 9.5, 6.5],
}
RUIDO = {
    "UPS":      [4, 1.5, 8, 0.5, 0.5, 1.5],
    "Generador":[4, 0.2, 3, 0.8, 15,  10],
    "Aire Acondicionado": [0.8, 0.2, 2, 0.8, 0.5, 0.3],
}


def vars_equipo(equipo):
    return VARS_POR_TIPO[EQUIPOS[equipo]["tipo"]]


def _estado(var, val, limites):
    L = limites.get(var, {})
    if L.get("critico_max") and val >= L["critico_max"]: return "🔴"
    if L.get("alerta_max")  and val >= L["alerta_max"]:  return "⚠️"
    if L.get("critico_min") and val <= L["critico_min"]: return "🔴"
    if L.get("alerta_min")  and val <= L["alerta_min"]:  return "⚠️"
    return "🟢"


# ─── DATOS SIMULADOS ──────────────────────────────────────────────────────────
@st.cache_data(ttl=5)
def live_values(equipo: str, tick: int) -> dict:
    tipo = EQUIPOS[equipo]["tipo"]
    b = BASE[equipo]
    r = RUIDO[tipo]
    rng = np.random.default_rng(seed=tick + abs(hash(equipo)) % 9999)
    vals = [b[i] + rng.uniform(-r[i], r[i]) for i in range(len(b))]
    return dict(zip(vars_equipo(equipo).keys(), vals))


@st.cache_data(ttl=3600)
def historico(equipo: str, dias: int) -> pd.DataFrame:
    tipo = EQUIPOS[equipo]["tipo"]
    periods = dias * 24 * 12
    idx = pd.date_range(end=datetime.now(), periods=periods, freq="5min")
    b = BASE[equipo]
    r = RUIDO[tipo]
    rng = np.random.default_rng(seed=42 + abs(hash(equipo)) % 999)

    cols = {}
    for i, var in enumerate(vars_equipo(equipo).keys()):
        serie = b[i] + np.cumsum(rng.normal(0, r[i] * 0.15, periods))
        mn, mx = vars_equipo(equipo)[var]["range"]
        serie = np.clip(serie, mn, mx)
        # Evento 1: degradación
        e1 = int(periods * 0.30)
        if "critico_max" in vars_equipo(equipo)[var]:
            serie[e1:e1+36] += r[i] * 3
        elif "critico_min" in vars_equipo(equipo)[var]:
            serie[e1:e1+36] -= r[i] * 3
        serie = np.clip(serie, mn, mx)
        cols[var] = np.round(serie, 2)

    df = pd.DataFrame(cols, index=idx)
    df.index.name = "timestamp"
    return df.reset_index()


def alertas_fijas():
    return pd.DataFrame([
        {"Timestamp": "2026-05-23 09:15", "Equipo": "UPS-01  (80 kVA)",   "Variable": "Nivel Batería (%)",   "Valor": 28.0,  "Límite": 30.0,  "Severidad": "⚠️ Advertencia", "Estado": "🔴 Activa"},
        {"Timestamp": "2026-05-23 07:42", "Equipo": "AC-01  Sala Serv.",  "Variable": "T° Ambiente (°C)",    "Valor": 25.2,  "Límite": 24.0,  "Severidad": "⚠️ Advertencia", "Estado": "🔴 Activa"},
        {"Timestamp": "2026-05-22 22:10", "Equipo": "GEN-01  (250 kVA)", "Variable": "Nivel Combustible (%)", "Valor": 22.0,  "Límite": 25.0,  "Severidad": "⚠️ Advertencia", "Estado": "✅ Resuelta"},
        {"Timestamp": "2026-05-22 14:05", "Equipo": "UPS-02  (40 kVA)",  "Variable": "T° Batería (°C)",      "Valor": 37.5,  "Límite": 35.0,  "Severidad": "⚠️ Advertencia", "Estado": "✅ Resuelta"},
        {"Timestamp": "2026-05-21 11:30", "Equipo": "AC-02  Sala UPS",   "Variable": "Humedad Relativa (%)", "Valor": 68.0,  "Límite": 60.0,  "Severidad": "⚠️ Advertencia", "Estado": "✅ Resuelta"},
        {"Timestamp": "2026-05-21 03:22", "Equipo": "GEN-01  (250 kVA)", "Variable": "T° Aceite (°C)",       "Valor": 98.0,  "Límite": 90.0,  "Severidad": "🔴 Crítico",     "Estado": "✅ Resuelta"},
        {"Timestamp": "2026-05-20 18:50", "Equipo": "UPS-01  (80 kVA)",  "Variable": "Nivel Batería (%)",    "Valor": 12.0,  "Límite": 15.0,  "Severidad": "🔴 Crítico",     "Estado": "✅ Resuelta"},
        {"Timestamp": "2026-05-19 09:00", "Equipo": "AC-03  Sala Gen.",  "Variable": "T° Ambiente (°C)",     "Valor": 28.5,  "Límite": 27.0,  "Severidad": "🔴 Crítico",     "Estado": "✅ Resuelta"},
    ])


INCIDENTES = [
    {
        "id": "INC-2026-041", "fecha": "2026-05-21", "equipo": "GEN-01  (250 kVA)",
        "descripcion": "Temperatura de aceite sobre límite crítico durante prueba de carga",
        "causa": "Obstrucción parcial en sistema de enfriamiento. Filtro de aire colmatado.",
        "duracion": "1h 45min", "severidad": "Alta", "estado": "Cerrado",
        "acciones": [
            "03:22 — Alarma crítica: T° aceite 98°C (límite 90°C)",
            "03:25 — Reducción automática de carga al 60%",
            "03:30 — Notificación a técnico de guardia",
            "04:00 — Limpieza de filtros de aire y radiador",
            "05:07 — Temperatura normalizada (78°C). Operación normal",
        ],
    },
    {
        "id": "INC-2026-038", "fecha": "2026-05-20", "equipo": "UPS-01  (80 kVA)",
        "descripcion": "Nivel de batería crítico — Falla de red eléctrica prolongada",
        "causa": "Corte de energía de red por 4.5 horas. Autonomía real insuficiente para la carga conectada.",
        "duracion": "4h 30min", "severidad": "Alta", "estado": "Cerrado",
        "acciones": [
            "18:20 — Falla red eléctrica — UPS-01 pasa a modo batería",
            "18:50 — Alerta: nivel batería 30% (30 min autonomía restante)",
            "19:10 — Alarma crítica: nivel batería 12% (10 min)",
            "19:15 — Arranque automático GEN-01 como respaldo",
            "19:20 — Transferencia a generador exitosa — carga protegida",
            "22:50 — Restauración red eléctrica — carga transferida de vuelta",
        ],
    },
    {
        "id": "INC-2026-035", "fecha": "2026-05-19", "equipo": "AC-03  Sala Gen.",
        "descripcion": "Temperatura sala de generadores sobre límite — riesgo para equipos",
        "causa": "Falla de compresor en AC-03. Temperatura ambiente alcanzó 28.5°C.",
        "duracion": "3h 10min", "severidad": "Alta", "estado": "Cerrado",
        "acciones": [
            "09:00 — Alarma crítica: T° ambiente 28.5°C (límite 27°C)",
            "09:05 — Notificación técnico de HVAC",
            "09:30 — Diagnóstico: falla en compresor AC-03",
            "10:00 — Activación AC de respaldo AC-01 (modo emergencia)",
            "11:15 — Temperatura normalizada (22°C)",
            "12:10 — Reemplazo de compresor completado. AC-03 operativo",
        ],
    },
    {
        "id": "INC-2026-031", "fecha": "2026-05-17", "equipo": "AC-02  Sala UPS",
        "descripcion": "Humedad relativa fuera de rango — riesgo de condensación",
        "causa": "Falla en sistema de deshumidificación. Humedad alcanzó 68%.",
        "duracion": "2h 20min", "severidad": "Media", "estado": "Cerrado",
        "acciones": [
            "21:10 — Alerta: humedad 68% (límite 60%)",
            "21:15 — Ajuste automático setpoint deshumidificador",
            "22:00 — Humedad sin mejora — técnico convocado",
            "22:30 — Reparación sensor humedad y módulo deshumidificador",
            "23:30 — Humedad normalizada (48%). Cierre de incidente",
        ],
    },
]

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ Monitor Remoto")
    st.markdown("*UPS · Generadores · A/C*")
    st.markdown("---")

    grupo_sel = st.radio("**Grupo de equipo**",
                         ["UPS", "Generador", "A/C (Aire Acondicionado)"])
    grupo_key = "Aire Acondicionado" if "A/C" in grupo_sel else grupo_sel

    equipos_grupo = [e for e, v in EQUIPOS.items() if v["grupo"] == grupo_key or
                     (grupo_key == "Aire Acondicionado" and v["tipo"] == "Aire Acondicionado")]
    equipo_sel = st.selectbox("**Equipo activo**", equipos_grupo)

    st.markdown("---")
    dias_hist = st.select_slider("Período histórico (días)", [7, 14, 30, 60, 90], value=30)

    st.markdown("---")
    auto_refresh = st.toggle("🔴 Monitoreo en tiempo real", value=True)
    intervalo = st.slider("Intervalo refresco (seg)", 3, 30, 5) if auto_refresh else 9999

    st.markdown("---")
    st.caption(f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    st.caption("Demo v2.0")

# ─── HEADER ───────────────────────────────────────────────────────────────────
tipo_color = {"UPS": "#1565c0", "Generador": "#2e7d32", "Aire Acondicionado": "#e65100"}
hcolor = tipo_color.get(EQUIPOS[equipo_sel]["tipo"], "#1565c0")

st.markdown(f"""
<div style="background:linear-gradient(90deg,#0d2137,{hcolor});
     padding:1.1rem 1.4rem;border-radius:10px;margin-bottom:0.8rem;">
  <h2 style="color:white;margin:0;font-size:1.4rem;">
    ⚡ Sistema de Monitoreo Remoto — UPS · Generadores · Aires Acondicionados
  </h2>
  <p style="color:#b3e5fc;margin:4px 0 0;font-size:0.85rem;">
    Tiempo real · Históricos · Alertas tempranas · Trazabilidad de incidentes
  </p>
</div>
""", unsafe_allow_html=True)

VARS = vars_equipo(equipo_sel)
COLOR = EQUIPOS[equipo_sel]["color"]

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Tiempo Real",
    "📈  Histórico & Análisis",
    "🔔  Alertas Tempranas",
    "📋  Trazabilidad de Incidentes",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TIEMPO REAL
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(f"### {equipo_sel} &nbsp;·&nbsp; {EQUIPOS[equipo_sel]['tipo']}")

    @st.fragment(run_every=intervalo if auto_refresh else None)
    def panel_live():
        tick = int(time.time() // intervalo)
        vals = live_values(equipo_sel, tick)

        # Métricas en fila
        cols = st.columns(len(vals))
        for col, (var, val) in zip(cols, vals.items()):
            est = _estado(var, val, VARS)
            if var in ("Nivel Batería (%)", "Nivel Combustible (%)"):
                fmt = f"{val:.0f} %"
            elif "V)" in var:
                fmt = f"{val:.1f} V"
            elif "Hz" in var:
                fmt = f"{val:.2f} Hz"
            elif "°C" in var:
                fmt = f"{val:.1f} °C"
            elif "kW" in var:
                fmt = f"{val:.1f} kW"
            elif "RPM" in var:
                fmt = f"{val:.0f} rpm"
            elif "bar" in var:
                fmt = f"{val:.2f} bar"
            elif "min" in var:
                fmt = f"{val:.0f} min"
            else:
                fmt = f"{val:.1f}"
            col.metric(f"{est} {var}", fmt)

        st.markdown("---")

        # Gauges — primeras 3 variables clave
        var_list = list(vals.items())
        gcols = st.columns(3)
        for idx_g, gcol in enumerate(gcols):
            if idx_g >= len(var_list):
                break
            var, val = var_list[idx_g]
            L = VARS[var]
            mn, mx = L["range"]
            # Determinar zona de color
            warn = L.get("alerta_max", L.get("alerta_min", mn + (mx - mn) * 0.7))
            crit = L.get("critico_max", L.get("critico_min", mx))
            high_bad = "alerta_max" in L

            if high_bad:
                steps = [
                    {"range": [mn, warn], "color": "#1e2535"},
                    {"range": [warn, crit], "color": "#2d2010"},
                    {"range": [crit, mx],  "color": "#2d1010"},
                ]
            else:
                steps = [
                    {"range": [mn, crit],  "color": "#2d1010"},
                    {"range": [crit, warn],"color": "#2d2010"},
                    {"range": [warn, mx],  "color": "#1e2535"},
                ]

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=val,
                title={"text": var, "font": {"size": 11, "color": "white"}},
                gauge={
                    "axis": {"range": [mn, mx], "tickcolor": "white",
                             "tickfont": {"color": "white", "size": 9}},
                    "bar": {"color": COLOR},
                    "steps": steps,
                    "threshold": {"line": {"color": "red", "width": 2},
                                  "thickness": 0.75, "value": crit},
                },
                number={"font": {"color": "white", "size": 26}},
            ))
            fig.update_layout(
                height=220, paper_bgcolor="#1e2535",
                margin=dict(l=15, r=15, t=40, b=10),
            )
            gcol.plotly_chart(fig, use_container_width=True)

        # Gráfica sparkline — últimas 2 horas simuladas
        st.markdown("#### Tendencia últimas 2 horas")
        n = 24  # 24 puntos × 5 min = 2h
        t2h = pd.date_range(end=datetime.now(), periods=n, freq="5min")
        tick_seed = int(time.time() // 300)
        rng2 = np.random.default_rng(seed=tick_seed + abs(hash(equipo_sel)) % 999)

        fig_spark = make_subplots(
            rows=2, cols=3,
            subplot_titles=list(vals.keys()),
            vertical_spacing=0.18, horizontal_spacing=0.08,
        )
        for i, (var, val_now) in enumerate(vals.items()):
            row, col_idx = divmod(i, 3)
            b_v = BASE[equipo_sel][i]
            r_v = RUIDO[EQUIPOS[equipo_sel]["tipo"]][i]
            serie = b_v + np.cumsum(rng2.normal(0, r_v * 0.1, n))
            mn2, mx2 = VARS[var]["range"]
            serie = np.clip(serie, mn2, mx2)
            serie[-1] = val_now

            est = _estado(var, val_now, VARS)
            line_color = "#f44336" if est == "🔴" else "#FF9800" if est == "⚠️" else COLOR

            fig_spark.add_trace(
                go.Scatter(x=t2h, y=serie, mode="lines",
                           line=dict(color=line_color, width=2),
                           showlegend=False, name=var),
                row=row + 1, col=col_idx + 1,
            )
            # Línea de alerta
            lim_val = VARS[var].get("alerta_max", VARS[var].get("alerta_min"))
            if lim_val:
                fig_spark.add_hline(y=lim_val, line_dash="dot",
                                    line_color="#FF9800", line_width=1,
                                    row=row + 1, col=col_idx + 1)

        fig_spark.update_layout(
            paper_bgcolor="#1e2535", plot_bgcolor="#1e2535",
            font_color="white", height=340,
            margin=dict(l=30, r=10, t=35, b=20),
        )
        fig_spark.update_xaxes(showticklabels=False, gridcolor="#252e42")
        fig_spark.update_yaxes(gridcolor="#252e42", tickfont=dict(size=9))
        st.plotly_chart(fig_spark, use_container_width=True)
        st.caption(f"Última actualización: {datetime.now().strftime('%H:%M:%S')}")

    panel_live()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — HISTÓRICO & ANÁLISIS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(f"### {equipo_sel} &nbsp;·&nbsp; últimos {dias_hist} días")
    df = historico(equipo_sel, dias_hist)

    sub1, sub2 = st.tabs(["Serie temporal", "Análisis estadístico"])

    # ── Serie temporal ────────────────────────────────────────────────────────
    with sub1:
        var_sel = st.selectbox("Variable", list(VARS.keys()), key="var_hist")
        L = VARS[var_sel]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["timestamp"], y=df[var_sel],
            mode="lines", name=var_sel,
            line=dict(color=COLOR, width=1),
            fill="tozeroy", fillcolor=f"rgba(33,150,243,0.06)",
        ))
        for lk, lc, lpos in [
            ("alerta_max",  "#FF9800", "top right"),
            ("critico_max", "#f44336", "top right"),
            ("alerta_min",  "#FF9800", "bottom right"),
            ("critico_min", "#f44336", "bottom right"),
        ]:
            if lk in L:
                fig.add_hline(y=L[lk], line_dash="dash", line_color=lc,
                              annotation_text=lk.replace("_", " ").title(),
                              annotation_font_color=lc, annotation_position=lpos)

        fig.update_layout(
            paper_bgcolor="#1e2535", plot_bgcolor="#1e2535", font_color="white",
            height=360, xaxis=dict(gridcolor="#252e42"),
            yaxis=dict(title=var_sel, gridcolor="#252e42"),
            margin=dict(l=60, r=20, t=15, b=50),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Estadísticas rápidas
        s = df[var_sel]
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Mínimo",     f"{s.min():.2f}")
        c2.metric("Máximo",     f"{s.max():.2f}")
        c3.metric("Promedio",   f"{s.mean():.2f}")
        c4.metric("Desv. Est.", f"{s.std():.2f}")
        exc = 0
        if "alerta_max" in L:  exc = int((s > L["alerta_max"]).sum())
        elif "alerta_min" in L: exc = int((s < L["alerta_min"]).sum())
        c5.metric("Excedencias", exc)

        # Mapa de calor hora del día
        st.markdown("#### Mapa de calor — promedio por hora del día")
        df2 = df.copy()
        df2["hora"] = pd.to_datetime(df2["timestamp"]).dt.hour
        df2["dia"]  = pd.to_datetime(df2["timestamp"]).dt.date.astype(str)
        pivot = df2.pivot_table(values=var_sel, index="dia", columns="hora", aggfunc="mean")
        invert = "alerta_min" in L
        fig_h = px.imshow(pivot,
                          color_continuous_scale="RdYlGn" if invert else "RdYlGn_r",
                          labels=dict(x="Hora", y="Fecha", color=var_sel),
                          aspect="auto")
        fig_h.update_layout(paper_bgcolor="#1e2535", font_color="white",
                            height=350, margin=dict(l=70, r=20, t=15, b=40))
        st.plotly_chart(fig_h, use_container_width=True)

    # ── Análisis estadístico ──────────────────────────────────────────────────
    with sub2:
        st.markdown("#### Comparación de todas las variables — distribución (box plot)")
        vars_num = list(VARS.keys())
        fig_box = go.Figure()
        for var in vars_num:
            s = df[var]
            mn2, mx2 = VARS[var]["range"]
            s_norm = (s - mn2) / (mx2 - mn2) * 100
            fig_box.add_trace(go.Box(
                y=s_norm, name=var[:22],
                marker_color=COLOR, boxmean=True,
                line_color=COLOR,
            ))
        fig_box.update_layout(
            paper_bgcolor="#1e2535", plot_bgcolor="#1e2535", font_color="white",
            height=380, yaxis_title="% del rango operativo",
            xaxis=dict(tickfont=dict(size=10)),
            margin=dict(l=50, r=10, t=20, b=80),
        )
        st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("#### Correlación entre variables")
        corr = df[vars_num].corr()
        fig_corr = px.imshow(corr, text_auto=".2f",
                             color_continuous_scale="RdBu_r",
                             zmin=-1, zmax=1,
                             labels=dict(color="Correlación"))
        fig_corr.update_layout(paper_bgcolor="#1e2535", font_color="white",
                               height=380, margin=dict(l=10, r=10, t=20, b=10))
        fig_corr.update_xaxes(tickfont=dict(size=9))
        fig_corr.update_yaxes(tickfont=dict(size=9))
        st.plotly_chart(fig_corr, use_container_width=True)

        st.markdown("#### Tendencia semanal — promedio diario")
        df3 = df.copy()
        df3["fecha"] = pd.to_datetime(df3["timestamp"]).dt.date
        daily = df3.groupby("fecha")[vars_num].mean().reset_index()
        var_trend = st.selectbox("Variable para tendencia", vars_num, key="var_trend")
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=daily["fecha"], y=daily[var_trend],
            mode="lines+markers", line=dict(color=COLOR, width=2),
            marker=dict(size=5), name="Promedio diario",
        ))
        mn3, mx3 = VARS[var_trend]["range"]
        fig_trend.update_layout(
            paper_bgcolor="#1e2535", plot_bgcolor="#1e2535", font_color="white",
            height=300, yaxis=dict(range=[mn3, mx3], gridcolor="#252e42"),
            xaxis=dict(gridcolor="#252e42"),
            margin=dict(l=50, r=10, t=15, b=50),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ALERTAS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Alertas tempranas del sistema")
    df_a = alertas_fijas()
    activas   = df_a[df_a["Estado"].str.contains("Activa")]
    resueltas = df_a[df_a["Estado"].str.contains("Resuelta")]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Críticas activas",
              int(len(activas[activas["Severidad"].str.contains("Crítico")])))
    c2.metric("⚠️ Advertencias activas",
              int(len(activas[activas["Severidad"].str.contains("Advertencia")])))
    c3.metric("✅ Resueltas (7 días)", int(len(resueltas)))
    c4.metric("Total alertas (7 días)", int(len(df_a)))

    st.markdown("---")
    st.markdown("#### Alertas activas")
    for _, row in activas.iterrows():
        cls = "alert-critical" if "Crítico" in row["Severidad"] else "alert-warning"
        st.markdown(f"""
        <div class="{cls}">
          <strong>{row['Severidad']} &nbsp;·&nbsp; {row['Equipo']}</strong><br>
          Variable: <strong>{row['Variable']}</strong> = <strong>{row['Valor']}</strong>
          &nbsp;(límite: {row['Límite']}) &nbsp;·&nbsp; {row['Timestamp']}
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Historial completo — últimos 7 días")
    st.dataframe(df_a, hide_index=True, use_container_width=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Alertas por equipo")
        cnt_eq = df_a.groupby("Equipo").size().reset_index(name="n").sort_values("n", ascending=True)
        fig_eq = px.bar(cnt_eq, x="n", y="Equipo", orientation="h",
                        color_discrete_sequence=[COLOR],
                        labels={"n": "Alertas", "Equipo": ""})
        fig_eq.update_layout(paper_bgcolor="#1e2535", plot_bgcolor="#1e2535",
                             font_color="white", height=280,
                             margin=dict(l=10, r=10, t=15, b=30))
        st.plotly_chart(fig_eq, use_container_width=True)

    with col_b:
        st.markdown("#### Alertas por severidad")
        cnt_sev = df_a["Severidad"].value_counts().reset_index()
        cnt_sev.columns = ["Severidad", "n"]
        fig_pie = px.pie(cnt_sev, values="n", names="Severidad",
                         color_discrete_map={"🔴 Crítico": "#f44336",
                                             "⚠️ Advertencia": "#FF9800"})
        fig_pie.update_layout(paper_bgcolor="#1e2535", font_color="white",
                              height=280, margin=dict(l=10, r=10, t=15, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — INCIDENTES
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Trazabilidad de incidentes")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Incidentes (30 días)", len(INCIDENTES))
    c2.metric("Alta severidad",  sum(1 for i in INCIDENTES if i["severidad"] == "Alta"))
    c3.metric("Media severidad", sum(1 for i in INCIDENTES if i["severidad"] == "Media"))
    c4.metric("Tiempo prom. resolución", "2h 56min")

    st.markdown("---")

    filtro_tipo = st.multiselect(
        "Filtrar por tipo de equipo",
        ["UPS", "Generador", "Aire Acondicionado"],
        default=["UPS", "Generador", "Aire Acondicionado"],
    )

    for inc in INCIDENTES:
        tipo_inc = EQUIPOS.get(inc["equipo"], {}).get("tipo", "")
        if tipo_inc not in filtro_tipo:
            continue
        sev_col = "#f44336" if inc["severidad"] == "Alta" else "#FF9800"
        est_col = "#4CAF50" if inc["estado"] == "Cerrado" else "#2196F3"
        equipo_color = EQUIPOS.get(inc["equipo"], {}).get("color", "#888")

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
                bullet = "🔴" if j == 0 else "🟡" if j <= 2 else "🟢"
                st.markdown(f"&nbsp;&nbsp;{bullet}&nbsp; `{accion}`")

    st.markdown("---")
    col_i1, col_i2 = st.columns(2)

    with col_i1:
        st.markdown("#### Incidentes por tipo de equipo")
        tipo_cnt = {}
        for inc in INCIDENTES:
            t = EQUIPOS.get(inc["equipo"], {}).get("tipo", "Otro")
            tipo_cnt[t] = tipo_cnt.get(t, 0) + 1
        df_tipo = pd.DataFrame(list(tipo_cnt.items()), columns=["Tipo", "n"])
        fig_t = px.bar(df_tipo, x="Tipo", y="n",
                       color="Tipo",
                       color_discrete_map={"UPS": "#2196F3",
                                           "Generador": "#4CAF50",
                                           "Aire Acondicionado": "#FF9800"},
                       labels={"n": "Incidentes"})
        fig_t.update_layout(paper_bgcolor="#1e2535", plot_bgcolor="#1e2535",
                            font_color="white", height=280, showlegend=False,
                            yaxis=dict(gridcolor="#252e42"),
                            margin=dict(l=40, r=10, t=15, b=50))
        st.plotly_chart(fig_t, use_container_width=True)

    with col_i2:
        st.markdown("#### Tiempo de resolución por incidente")
        dur_map = {"INC-2026-041": 1.75, "INC-2026-038": 4.5,
                   "INC-2026-035": 3.17, "INC-2026-031": 2.33}
        df_dur = pd.DataFrame([
            {"Incidente": inc["id"], "Horas": dur_map.get(inc["id"], 2),
             "Tipo": EQUIPOS.get(inc["equipo"], {}).get("tipo", "Otro")}
            for inc in INCIDENTES
        ])
        fig_dur = px.bar(df_dur, x="Incidente", y="Horas", color="Tipo",
                         color_discrete_map={"UPS": "#2196F3",
                                             "Generador": "#4CAF50",
                                             "Aire Acondicionado": "#FF9800"},
                         labels={"Horas": "Horas hasta resolución"})
        fig_dur.update_layout(paper_bgcolor="#1e2535", plot_bgcolor="#1e2535",
                              font_color="white", height=280,
                              yaxis=dict(gridcolor="#252e42"),
                              margin=dict(l=40, r=10, t=15, b=50))
        st.plotly_chart(fig_dur, use_container_width=True)
