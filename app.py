import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import time
import io

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LUXPOWER METRICS Platform",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── THEME COLORS ─────────────────────────────────────────────────────────────
TEAL   = "#009688"
TEAL_L = "#26C6DA"
TEAL_D = "#00695C"
NAVY   = "#0a0e1a"
CARD   = "#111827"
CARD2  = "#1a2535"

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{ background: {NAVY}; }}
[data-testid="stSidebar"]          {{ background: #060c18; border-right: 1px solid #1e2d3e; }}
.block-container {{ padding-top: 0.5rem; }}
.stMetric        {{ background: {CARD2}; border-radius: 8px; padding: 10px 14px; }}
.stTabs [data-baseweb="tab-list"] {{ background: {CARD}; border-radius: 8px; }}
.stTabs [data-baseweb="tab"]      {{ color: #90a4ae; }}
.stTabs [aria-selected="true"]    {{ color: {TEAL_L} !important; border-bottom: 2px solid {TEAL_L}; }}
.lux-card {{
    background: {CARD2}; border-radius: 10px; padding: 1rem 1.2rem;
    border-left: 3px solid {TEAL};
}}
.alert-critical {{
    background: rgba(244,67,54,.12); border-left: 4px solid #f44336;
    padding: 10px 14px; margin: 5px 0; border-radius: 6px;
}}
.alert-warning {{
    background: rgba(255,152,0,.12); border-left: 4px solid #ff9800;
    padding: 10px 14px; margin: 5px 0; border-radius: 6px;
}}
div[data-testid="stDownloadButton"] button {{
    background: {TEAL_D}; color: white; border: none; border-radius: 6px;
}}
</style>
""", unsafe_allow_html=True)

# ─── CREDENCIALES ─────────────────────────────────────────────────────────────
USUARIOS = {
    "DEMO":    {"clave": "1234",        "rol": "Operador"},
    "EERSSA":  {"clave": "monitor2026", "rol": "Administrador"},
    "COMITE":  {"clave": "eval2026",    "rol": "Auditor"},
}

# ─── LOGIN ────────────────────────────────────────────────────────────────────
def login_page():
    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{ background: linear-gradient(135deg,#050d18 0%,#0a1628 60%,#061a1a 100%); }}
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown(f"""
        <div style="padding:3rem 1rem 1rem 2rem;">
          <p style="color:{TEAL_L};font-size:0.8rem;letter-spacing:4px;margin:0;">
            PLATAFORMA IoT · NOC 24/7 · GSM REDUNDANTE
          </p>
          <h1 style="color:white;font-size:2.8rem;margin:0.3rem 0 0.5rem;font-weight:800;">
            Monitoreo Remoto<br>de Equipos Críticos
          </h1>
          <p style="color:#607d8b;font-size:1rem;max-width:480px;line-height:1.7;">
            Supervisión en tiempo real de UPS, generadores y aires acondicionados.
            Alertas automáticas, diagnóstico remoto y registro de eventos 24/7.
          </p>
          <div style="display:flex;gap:2rem;margin-top:2rem;">
            <div style="text-align:center;">
              <div style="color:{TEAL_L};font-size:1.8rem;font-weight:bold;">99.9%</div>
              <div style="color:#546e7a;font-size:0.75rem;">Disponibilidad</div>
            </div>
            <div style="text-align:center;">
              <div style="color:{TEAL_L};font-size:1.8rem;font-weight:bold;">24/7</div>
              <div style="color:#546e7a;font-size:0.75rem;">Monitoreo NOC</div>
            </div>
            <div style="text-align:center;">
              <div style="color:{TEAL_L};font-size:1.8rem;font-weight:bold;">5 años</div>
              <div style="color:#546e7a;font-size:0.75rem;">Historial datos</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div style="background:#0f1e2e;border:1px solid #1e3a4a;border-radius:16px;
             padding:2.5rem 2rem;max-width:380px;margin:3rem auto 0;">
          <div style="text-align:center;margin-bottom:2rem;">
            <div style="background:{TEAL_D};display:inline-block;padding:12px 18px;
                 border-radius:12px;margin-bottom:0.8rem;">
              <span style="color:white;font-size:1.4rem;font-weight:900;
                   letter-spacing:2px;">LR</span>
            </div>
            <div style="color:white;font-size:1.1rem;font-weight:700;letter-spacing:1px;">
              LUXPOWER METRICS
            </div>
            <div style="color:{TEAL_L};font-size:0.72rem;letter-spacing:3px;">PLATFORM</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("<div style='max-width:380px;margin:0 auto;padding:0 1rem;'>",
                        unsafe_allow_html=True)
            usuario = st.text_input("Email o usuario", placeholder="Ingrese su usuario",
                                    label_visibility="collapsed")
            clave   = st.text_input("Contraseña", type="password",
                                    placeholder="Contraseña",
                                    label_visibility="collapsed")
            if st.button("▶  Log In", use_container_width=True, type="primary"):
                if usuario in USUARIOS and USUARIOS[usuario]["clave"] == clave:
                    st.session_state["auth"] = True
                    st.session_state["user"] = usuario
                    st.session_state["rol"]  = USUARIOS[usuario]["rol"]
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")
            st.markdown(
                f"<p style='color:#37474f;font-size:0.72rem;text-align:center;"
                f"margin-top:0.8rem;'>Acceso restringido · Solo personal autorizado</p>",
                unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.get("auth"):
    login_page()
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# APP PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

# ─── CATÁLOGO ─────────────────────────────────────────────────────────────────
EQUIPOS = {
    "UPS-01  (80 kVA)":       {"tipo": "UPS",        "color": TEAL_L, "online": True},
    "UPS-02  (40 kVA)":       {"tipo": "UPS",        "color": TEAL,   "online": True},
    "GEN-01  (250 kVA)":      {"tipo": "Generador",  "color": "#66BB6A", "online": True},
    "GEN-02  (150 kVA)":      {"tipo": "Generador",  "color": "#A5D6A7", "online": False},
    "AC-01  Sala Servidores":  {"tipo": "A/C",        "color": "#FFA726", "online": True},
    "AC-02  Sala UPS":         {"tipo": "A/C",        "color": "#FF7043", "online": True},
    "AC-03  Sala Generadores": {"tipo": "A/C",        "color": "#EF5350", "online": True},
}

VARS_UPS = {
    "Voltaje Entrada (V)":  {"aw": 195, "cw": 185, "ah": 235, "ch": 245, "r": (170,260)},
    "Voltaje Salida (V)":   {"aw": 218, "cw": 210, "ah": 222, "ch": 230, "r": (200,240)},
    "Corriente Salida (A)": {"ah": 180, "ch": 200, "r": (0,220)},
    "Nivel Batería (%)":    {"aw": 30,  "cw": 15,  "r": (0,100)},
    "T° Batería (°C)":      {"ah": 35,  "ch": 40,  "r": (15,50)},
    "Autonomía (min)":      {"aw": 20,  "cw": 10,  "r": (0,120)},
}
VARS_GEN = {
    "Voltaje (V)":           {"aw": 210, "cw": 200, "ah": 230, "ch": 240, "r": (180,260)},
    "Frecuencia (Hz)":       {"aw": 59.5,"cw": 59.0,"ah": 60.5,"ch": 61.0,"r": (57,63)},
    "T° Aceite (°C)":        {"ah": 90,  "ch": 100, "r": (20,120)},
    "Nivel Combustible (%)": {"aw": 25,  "cw": 15,  "r": (0,100)},
    "RPM":                   {"aw": 1450,"cw": 1400,"ah": 1550,"ch": 1600,"r": (1300,1700)},
    "Potencia Activa (kW)":  {"ah": 210, "ch": 240, "r": (0,260)},
    "Horas Operación":       {"r": (0, 50000)},
    "Presión Aceite (bar)":  {"aw": 2.5, "cw": 2.0, "ah": 6.5, "ch": 7.0, "r": (1,8)},
}
VARS_AC = {
    "T° Ambiente (°C)":      {"ah": 24, "ch": 27, "r": (15,35)},
    "T° Setpoint (°C)":      {"r": (16,28)},
    "Humedad Relativa (%)":  {"ah": 60, "ch": 70, "aw": 30, "cw": 20, "r": (10,90)},
    "Corriente Comp. (A)":   {"ah": 18, "ch": 22, "r": (0,25)},
    "T° Evaporador (°C)":    {"aw": 5,  "cw": 2,  "r": (-5,20)},
    "Presión Refrig. (bar)": {"aw": 3.0,"cw": 2.5,"ah": 8.0,"ch": 9.0,"r": (1,12)},
    "Voltaje Condensadora (V)":{"ah": 235,"ch": 245,"aw": 195,"cw": 185,"r": (170,260)},
    "Voltaje Evaporadora (V)": {"ah": 125,"ch": 130,"aw": 105,"cw": 100,"r": (90,140)},
}
VARS_TIPO = {"UPS": VARS_UPS, "Generador": VARS_GEN, "A/C": VARS_AC}

BASE = {
    "UPS-01  (80 kVA)":       [220,220,140,85,28,65],
    "UPS-02  (40 kVA)":       [218,220,80,92,26,80],
    "GEN-01  (250 kVA)":      [220,60.0,82,60,1500,185,12450,4.5],
    "GEN-02  (150 kVA)":      [219,60.0,75,70,1498,110,8200,4.2],
    "AC-01  Sala Servidores":  [21.5,20.0,48,12.0,8.5,5.8,220,110],
    "AC-02  Sala UPS":         [22.0,20.0,50,13.0,9.0,6.0,219,109],
    "AC-03  Sala Generadores": [23.0,22.0,55,14.0,9.5,6.5,221,111],
}
RUIDO_TIPO = {
    "UPS":      [4,1.5,8,0.5,0.5,1.5],
    "Generador":[4,0.2,3,0.8,15,10,0,0.1],
    "A/C":      [0.8,0.2,2,0.8,0.5,0.3,3,1.5],
}

def vtipo(equipo): return EQUIPOS[equipo]["tipo"]
def vdict(equipo): return VARS_TIPO[vtipo(equipo)]

def estado_val(var, val, L):
    if L.get("ch") and val >= L["ch"]: return "🔴"
    if L.get("ah") and val >= L["ah"]: return "⚠️"
    if L.get("cw") and val <= L["cw"]: return "🔴"
    if L.get("aw") and val <= L["aw"]: return "⚠️"
    return "🟢"

def fmt_val(var, val):
    if "%" in var:   return f"{val:.0f}%"
    if "V)" in var:  return f"{val:.1f} V"
    if "Hz" in var:  return f"{val:.2f} Hz"
    if "°C" in var:  return f"{val:.1f} °C"
    if "kW" in var:  return f"{val:.1f} kW"
    if "RPM" in var: return f"{val:.0f} rpm"
    if "bar" in var: return f"{val:.2f} bar"
    if "min" in var: return f"{val:.0f} min"
    if "Horas" in var: return f"{val:.0f} h"
    return f"{val:.1f}"

# ─── DATA SIM ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=5)
def live_values(equipo, tick):
    tipo = vtipo(equipo)
    b = BASE[equipo]
    r = RUIDO_TIPO[tipo]
    rng = np.random.default_rng(seed=tick + abs(hash(equipo)) % 9999)
    vals = [b[i] + rng.uniform(-r[i], r[i]) for i in range(min(len(b), len(r)))]
    return dict(zip(list(vdict(equipo).keys())[:len(vals)], vals))

@st.cache_data(ttl=3600)
def historico(equipo, dias):
    tipo = vtipo(equipo)
    periods = dias * 24 * 12
    idx = pd.date_range(end=datetime.now(), periods=periods, freq="5min")
    b = BASE[equipo]
    r = RUIDO_TIPO[tipo]
    rng = np.random.default_rng(seed=42 + abs(hash(equipo)) % 999)
    cols = {}
    vars_list = list(vdict(equipo).keys())
    for i, var in enumerate(vars_list[:len(r)]):
        s = b[i] + np.cumsum(rng.normal(0, r[i] * 0.15, periods))
        mn, mx = vdict(equipo)[var]["r"]
        s = np.clip(s, mn, mx)
        e1 = int(periods * 0.30)
        L = vdict(equipo)[var]
        if L.get("ch"): s[e1:e1+36] += r[i] * 3
        elif L.get("cw"): s[e1:e1+36] -= r[i] * 3
        s = np.clip(s, mn, mx)
        cols[var] = np.round(s, 2)
    df = pd.DataFrame(cols, index=idx)
    df.index.name = "Timestamp"
    return df.reset_index()

def alertas_df():
    return pd.DataFrame([
        {"Timestamp":"2026-05-23 09:15","Equipo":"UPS-01  (80 kVA)",      "Variable":"Nivel Batería (%)","Valor":28.0, "Límite":30.0,"Severidad":"⚠️ Advertencia","Estado":"🔴 Activa"},
        {"Timestamp":"2026-05-23 07:42","Equipo":"AC-01  Sala Servidores","Variable":"T° Ambiente (°C)", "Valor":25.2, "Límite":24.0,"Severidad":"⚠️ Advertencia","Estado":"🔴 Activa"},
        {"Timestamp":"2026-05-22 22:10","Equipo":"GEN-01  (250 kVA)",     "Variable":"Nivel Combustible (%)","Valor":22.0,"Límite":25.0,"Severidad":"⚠️ Advertencia","Estado":"✅ Resuelta"},
        {"Timestamp":"2026-05-22 14:05","Equipo":"UPS-02  (40 kVA)",      "Variable":"T° Batería (°C)",  "Valor":37.5, "Límite":35.0,"Severidad":"⚠️ Advertencia","Estado":"✅ Resuelta"},
        {"Timestamp":"2026-05-21 11:30","Equipo":"AC-02  Sala UPS",       "Variable":"Humedad Relativa (%)","Valor":68.0,"Límite":60.0,"Severidad":"⚠️ Advertencia","Estado":"✅ Resuelta"},
        {"Timestamp":"2026-05-21 03:22","Equipo":"GEN-01  (250 kVA)",     "Variable":"T° Aceite (°C)",   "Valor":98.0, "Límite":90.0,"Severidad":"🔴 Crítico",    "Estado":"✅ Resuelta"},
        {"Timestamp":"2026-05-20 18:50","Equipo":"UPS-01  (80 kVA)",      "Variable":"Nivel Batería (%)", "Valor":12.0, "Límite":15.0,"Severidad":"🔴 Crítico",    "Estado":"✅ Resuelta"},
        {"Timestamp":"2026-05-19 09:00","Equipo":"AC-03  Sala Generadores","Variable":"T° Ambiente (°C)", "Valor":28.5, "Límite":27.0,"Severidad":"🔴 Crítico",    "Estado":"✅ Resuelta"},
    ])

INCIDENTES = [
    {"id":"INC-2026-041","fecha":"2026-05-21","equipo":"GEN-01  (250 kVA)","tipo":"Generador",
     "descripcion":"Temperatura de aceite sobre límite crítico",
     "causa":"Obstrucción en sistema de enfriamiento — filtro de aire colmatado.",
     "duracion":"1h 45min","severidad":"Alta","estado":"Cerrado",
     "acciones":["03:22 — Alarma crítica: T° aceite 98°C (límite 90°C)",
                 "03:25 — Reducción automática de carga al 60%",
                 "03:30 — Notificación técnico de guardia vía SMS",
                 "04:00 — Limpieza de filtros y radiador en campo",
                 "05:07 — Temperatura normalizada (78°C). Operación normal"]},
    {"id":"INC-2026-038","fecha":"2026-05-20","equipo":"UPS-01  (80 kVA)","tipo":"UPS",
     "descripcion":"Nivel de batería crítico — corte de red prolongado",
     "causa":"Falla de red eléctrica por 4.5 horas. Autonomía insuficiente para carga instalada.",
     "duracion":"4h 30min","severidad":"Alta","estado":"Cerrado",
     "acciones":["18:20 — Falla red eléctrica — UPS-01 pasa a batería",
                 "18:50 — Alerta: nivel batería 30% (30 min autonomía)",
                 "19:10 — Alarma crítica: nivel batería 12% (10 min)",
                 "19:15 — Arranque automático GEN-01 como respaldo",
                 "19:20 — Transferencia a generador exitosa",
                 "22:50 — Restauración red eléctrica"]},
    {"id":"INC-2026-035","fecha":"2026-05-19","equipo":"AC-03  Sala Generadores","tipo":"A/C",
     "descripcion":"Temperatura sala generadores sobre límite crítico",
     "causa":"Falla compresor AC-03. T° ambiente alcanzó 28.5°C.",
     "duracion":"3h 10min","severidad":"Alta","estado":"Cerrado",
     "acciones":["09:00 — Alarma crítica: T° ambiente 28.5°C",
                 "09:05 — Notificación técnico HVAC vía SMS",
                 "10:00 — Activación AC-01 como respaldo emergencia",
                 "11:15 — T° normalizada (22°C)",
                 "12:10 — Reemplazo compresor completado"]},
    {"id":"INC-2026-031","fecha":"2026-05-17","equipo":"AC-02  Sala UPS","tipo":"A/C",
     "descripcion":"Humedad fuera de rango — riesgo de condensación",
     "causa":"Falla módulo deshumidificador.",
     "duracion":"2h 20min","severidad":"Media","estado":"Cerrado",
     "acciones":["21:10 — Alerta: humedad 68% (límite 60%)",
                 "22:00 — Técnico convocado",
                 "22:30 — Reparación módulo deshumidificador",
                 "23:30 — Humedad normalizada (48%)"]},
]

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
      <div style="background:{TEAL_D};display:inline-block;padding:8px 14px;
           border-radius:10px;margin-bottom:0.4rem;">
        <span style="color:white;font-size:1.2rem;font-weight:900;letter-spacing:2px;">LR</span>
      </div>
      <div style="color:white;font-size:0.85rem;font-weight:700;letter-spacing:1px;">
        LUXPOWER METRICS
      </div>
      <div style="color:{TEAL_L};font-size:0.62rem;letter-spacing:3px;">PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    pagina = st.radio("Navegación", [
        "🏠  Inicio",
        "⚡  Monitoreo UPS",
        "🔋  Monitoreo Generadores",
        "❄️  Monitoreo A/C",
        "🔔  Gestión de Alarmas",
        "📊  Reporte de Parámetros",
        "📋  Trazabilidad Incidentes",
        "🌐  Arquitectura del Sistema",
    ], label_visibility="collapsed")

    st.markdown("---")
    online = sum(1 for e in EQUIPOS.values() if e["online"])
    offline = len(EQUIPOS) - online
    st.markdown(f"""
    <div style="font-size:0.78rem;color:#607d8b;padding:0 0.3rem;">
      <div style="margin-bottom:4px;">
        🟢 <b style="color:#4CAF50;">{online}</b> equipos online &nbsp;
        🔴 <b style="color:#f44336;">{offline}</b> offline
      </div>
      <div>📡 NOC activo · 24/7</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption(f"👤 {st.session_state.get('user','')} · {st.session_state.get('rol','')}")
    st.caption(f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state["auth"] = False
        st.rerun()

# ─── HEADER STRIP ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(90deg,{TEAL_D},{TEAL},{TEAL_L}22);
     padding:0.9rem 1.4rem;border-radius:10px;margin-bottom:0.7rem;
     border:1px solid {TEAL}44;">
  <span style="color:white;font-size:1.1rem;font-weight:700;">
    ⚡ LUXPOWER METRICS PLATFORM
  </span>
  <span style="color:{TEAL_L};font-size:0.8rem;margin-left:1rem;">
    UPS · Generadores · Aires Acondicionados · Monitoreo IoT 24/7
  </span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: INICIO
# ══════════════════════════════════════════════════════════════════════════════
if pagina == "🏠  Inicio":
    st.markdown("### Project Overview")
    df_a = alertas_df()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📁 Proyectos",          "1")
    c2.metric("📡 Medidores / Sensores", str(len(EQUIPOS)))
    c3.metric("🔔 Alarmas registradas", str(len(df_a)))
    c4.metric("🕐 Uptime plataforma",   "99.97%")

    st.markdown("---")
    col_left, col_right = st.columns([1, 1.6])

    with col_left:
        st.markdown("#### Estado de Dispositivos")
        online  = sum(1 for e in EQUIPOS.values() if e["online"])
        offline = len(EQUIPOS) - online
        alarm   = len(df_a[df_a["Estado"].str.contains("Activa")])
        normal  = online - alarm

        fig_d = go.Figure(go.Pie(
            labels=["Normal", "Con Alarma", "Offline"],
            values=[normal, alarm, offline],
            hole=0.62,
            marker_colors=["#4CAF50", "#FF9800", "#f44336"],
            textinfo="label+value",
            textfont_size=11,
        ))
        fig_d.update_layout(
            paper_bgcolor=CARD2, font_color="white", height=260,
            showlegend=True,
            legend=dict(bgcolor=CARD2, font_color="white", orientation="h",
                        yanchor="bottom", y=-0.15),
            margin=dict(l=10,r=10,t=20,b=30),
            annotations=[dict(text=f"<b>{len(EQUIPOS)}</b><br>Total",
                              x=0.5, y=0.5, showarrow=False,
                              font=dict(size=16, color="white"))],
        )
        st.plotly_chart(fig_d, use_container_width=True)

        st.markdown("#### Información de Alarmas")
        for _, row in df_a[df_a["Estado"].str.contains("Activa")].iterrows():
            cls = "alert-critical" if "Crítico" in row["Severidad"] else "alert-warning"
            st.markdown(f"""
            <div class="{cls}" style="font-size:0.82rem;">
              <b>{row['Equipo']}</b> — {row['Variable']}:
              <b>{row['Valor']}</b> · {row['Timestamp']}
            </div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown("#### Consumo de Energía — Tendencia diaria (kWh)")
        days = pd.date_range(end=datetime.now(), periods=30, freq="D")
        rng0 = np.random.default_rng(0)
        kwh  = 320 + np.cumsum(rng0.normal(0, 12, 30))
        kwh  = np.clip(kwh, 280, 410)

        fig_e = go.Figure()
        fig_e.add_trace(go.Scatter(
            x=days, y=kwh, mode="lines+markers",
            line=dict(color=TEAL_L, width=2),
            fill="tozeroy", fillcolor=f"rgba(38,198,218,0.08)",
            marker=dict(size=4, color=TEAL_L),
        ))
        fig_e.update_layout(
            paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
            height=200, margin=dict(l=40,r=10,t=10,b=30),
            xaxis=dict(gridcolor="#1e2d3e"),
            yaxis=dict(gridcolor="#1e2d3e", title="kWh"),
        )
        st.plotly_chart(fig_e, use_container_width=True)

        st.markdown("#### Estado en tiempo real — todos los equipos")
        for eq, info in EQUIPOS.items():
            tick = int(time.time() // 10)
            vals = live_values(eq, tick)
            var0 = list(vals.keys())[0]
            val0 = list(vals.values())[0]
            L0   = vdict(eq)[var0]
            est  = estado_val(var0, val0, L0)
            dot  = "🟢" if info["online"] else "🔴"
            st.markdown(f"""
            <div class="lux-card" style="margin-bottom:6px;padding:0.6rem 1rem;
                 border-left-color:{info['color']};">
              <span style="color:{info['color']};font-weight:600;">{dot} {eq}</span>
              <span style="color:#90a4ae;font-size:0.8rem;"> · {info['tipo']}</span>
              <span style="float:right;color:white;font-size:0.85rem;">
                {est} {var0}: <b>{fmt_val(var0,val0)}</b>
              </span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN: PANEL DE EQUIPO (reutilizable para UPS, GEN, A/C)
# ══════════════════════════════════════════════════════════════════════════════
def panel_equipo(tipo_filtro):
    equipos_tipo = [e for e, v in EQUIPOS.items() if v["tipo"] == tipo_filtro]
    eq = st.selectbox("Equipo", equipos_tipo, key=f"eq_{tipo_filtro}")
    color = EQUIPOS[eq]["color"]
    VARS  = vdict(eq)

    auto_ref  = st.sidebar.toggle(f"🔴 Tiempo real", value=True, key=f"ar_{tipo_filtro}")
    intervalo = st.sidebar.slider("Intervalo (seg)", 3, 30, 5,
                                  key=f"iv_{tipo_filtro}") if auto_ref else 9999

    t1, t2 = st.tabs(["📊 Tiempo Real", "📈 Histórico & Gráficas"])

    # ── Tiempo Real ──────────────────────────────────────────────────────────
    with t1:
        @st.fragment(run_every=intervalo if auto_ref else None)
        def live_panel():
            tick = int(time.time() // intervalo)
            vals = live_values(eq, tick)

            cols = st.columns(min(len(vals), 4))
            for i, (var, val) in enumerate(vals.items()):
                L   = VARS[var]
                est = estado_val(var, val, L)
                cols[i % 4].metric(f"{est} {var}", fmt_val(var, val))

            st.markdown("---")
            # Gauges
            var_list  = [(v, k) for k, v in vals.items()]
            gauge_vars = [(k, v) for k, v in vals.items()
                          if any(x in VARS[k] for x in ["ah","ch","aw","cw"])][:3]
            gcols = st.columns(len(gauge_vars)) if gauge_vars else []

            for gcol, (var, val) in zip(gcols, gauge_vars):
                L = VARS[var]
                mn, mx = L["r"]
                warn = L.get("ah", L.get("aw", mn + (mx-mn)*0.7))
                crit = L.get("ch", L.get("cw", mx))
                high_bad = "ah" in L
                steps = ([{"range":[mn,warn],"color":CARD2},
                           {"range":[warn,crit],"color":"#2d2010"},
                           {"range":[crit,mx],"color":"#2d1010"}]
                          if high_bad else
                          [{"range":[mn,crit],"color":"#2d1010"},
                           {"range":[crit,warn],"color":"#2d2010"},
                           {"range":[warn,mx],"color":CARD2}])
                fig = go.Figure(go.Indicator(
                    mode="gauge+number", value=val,
                    title={"text": var, "font": {"size":10,"color":"white"}},
                    gauge={"axis":{"range":[mn,mx],"tickcolor":"white",
                                   "tickfont":{"color":"white","size":8}},
                           "bar":{"color":color},"steps":steps,
                           "threshold":{"line":{"color":"red","width":2},
                                        "thickness":0.75,"value":crit}},
                    number={"font":{"color":"white","size":24}},
                ))
                fig.update_layout(height=210,paper_bgcolor=CARD2,
                                  margin=dict(l=10,r=10,t=38,b=5))
                gcol.plotly_chart(fig, use_container_width=True)

            # Sparklines 2h
            st.markdown("#### Tendencia últimas 2 horas")
            n   = 24
            t2h = pd.date_range(end=datetime.now(), periods=n, freq="5min")
            rng = np.random.default_rng(int(time.time()//300) + abs(hash(eq))%999)
            b   = BASE[eq]
            r   = RUIDO_TIPO[vtipo(eq)]
            n_vars = min(len(vals), len(r))

            fig_sp = make_subplots(
                rows=2, cols=min(n_vars, 4),
                subplot_titles=list(vals.keys())[:n_vars],
                vertical_spacing=0.22, horizontal_spacing=0.06,
            )
            for i, (var, val_now) in enumerate(list(vals.items())[:n_vars]):
                row, col_i = divmod(i, 4)
                s = b[i] + np.cumsum(rng.normal(0, r[i]*0.1, n))
                mn2, mx2 = VARS[var]["r"]
                s = np.clip(s, mn2, mx2)
                s[-1] = val_now
                est = estado_val(var, val_now, VARS[var])
                lc  = "#f44336" if est=="🔴" else "#FF9800" if est=="⚠️" else color
                fig_sp.add_trace(
                    go.Scatter(x=t2h, y=s, mode="lines",
                               line=dict(color=lc,width=1.5), showlegend=False),
                    row=row+1, col=col_i+1,
                )
                lim = VARS[var].get("ah", VARS[var].get("aw"))
                if lim:
                    fig_sp.add_hline(y=lim, line_dash="dot", line_color="#FF9800",
                                     line_width=1, row=row+1, col=col_i+1)
            fig_sp.update_layout(paper_bgcolor=CARD2, plot_bgcolor=CARD2,
                                 font_color="white", height=360,
                                 margin=dict(l=25,r=10,t=30,b=15))
            fig_sp.update_xaxes(showticklabels=False, gridcolor="#1e2d3e")
            fig_sp.update_yaxes(gridcolor="#1e2d3e", tickfont=dict(size=8))
            st.plotly_chart(fig_sp, use_container_width=True)
            st.caption(f"Última actualización: {datetime.now().strftime('%H:%M:%S')}  ·  "
                       f"NOC activo · GSM redundante")

        live_panel()

    # ── Histórico ─────────────────────────────────────────────────────────────
    with t2:
        dias = st.select_slider("Período", [7,14,30,60,90], value=30,
                                key=f"dias_{tipo_filtro}")
        df = historico(eq, dias)
        var_sel = st.selectbox("Variable", list(VARS.keys()), key=f"vs_{tipo_filtro}")
        L = VARS[var_sel]
        mn_v, mx_v = L["r"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Timestamp"], y=df[var_sel], mode="lines",
            line=dict(color=color, width=1.2),
            fill="tozeroy", fillcolor=f"rgba(38,198,218,0.06)", name=var_sel,
        ))
        for lk, lc, pos in [("ah","#FF9800","top right"),("ch","#f44336","top right"),
                             ("aw","#FF9800","bottom right"),("cw","#f44336","bottom right")]:
            if lk in L:
                fig.add_hline(y=L[lk], line_dash="dash", line_color=lc,
                              annotation_text={"ah":"Lím. advertencia","ch":"Lím. crítico",
                                               "aw":"Lím. adv. min","cw":"Lím. crít. min"}[lk],
                              annotation_font_color=lc, annotation_position=pos)
        fig.update_layout(paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
                          height=320, xaxis=dict(gridcolor="#1e2d3e"),
                          yaxis=dict(title=var_sel, gridcolor="#1e2d3e"),
                          margin=dict(l=55,r=15,t=10,b=45))
        st.plotly_chart(fig, use_container_width=True)

        s = df[var_sel]
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Mínimo",   f"{s.min():.2f}")
        c2.metric("Máximo",   f"{s.max():.2f}")
        c3.metric("Promedio", f"{s.mean():.2f}")
        c4.metric("Desv.Est", f"{s.std():.2f}")
        exc = int((s>L["ah"]).sum()) if "ah" in L else int((s<L["aw"]).sum()) if "aw" in L else 0
        c5.metric("Excedencias", exc)

        # Heatmap
        df["hora"] = pd.to_datetime(df["Timestamp"]).dt.hour
        df["dia"]  = pd.to_datetime(df["Timestamp"]).dt.date.astype(str)
        pivot = df.pivot_table(values=var_sel, index="dia", columns="hora", aggfunc="mean")
        fig_h = px.imshow(pivot,
                          color_continuous_scale="RdYlGn" if "aw" in L else "RdYlGn_r",
                          labels=dict(x="Hora",y="Fecha",color=var_sel), aspect="auto")
        fig_h.update_layout(paper_bgcolor=CARD2, font_color="white",
                            height=300, margin=dict(l=70,r=15,t=10,b=30))
        st.plotly_chart(fig_h, use_container_width=True)

        # Exportar CSV
        st.markdown("#### Exportar datos")
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            label="⬇️  Descargar historial CSV",
            data=csv_buf.getvalue(),
            file_name=f"{eq.strip()}_{var_sel}_{dias}d_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINAS DE EQUIPOS
# ══════════════════════════════════════════════════════════════════════════════
if pagina == "⚡  Monitoreo UPS":
    st.markdown("### Monitoreo de UPS")
    st.caption("Voltajes de entrada/salida · Corriente · Nivel batería · Temperatura · Autonomía")
    panel_equipo("UPS")

elif pagina == "🔋  Monitoreo Generadores":
    st.markdown("### Monitoreo de Generadores")
    st.caption("Voltaje · Frecuencia · T° aceite · Combustible · RPM · Potencia · Horas operación")
    panel_equipo("Generador")

elif pagina == "❄️  Monitoreo A/C":
    st.markdown("### Monitoreo de Aires Acondicionados")
    st.caption("T° ambiente · Humedad · Corriente compresor · Presión refrigerante · Voltajes")
    panel_equipo("A/C")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: ALARMAS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🔔  Gestión de Alarmas":
    st.markdown("### Gestión de Alarmas — Alertas Tempranas")
    df_a = alertas_df()
    activas   = df_a[df_a["Estado"].str.contains("Activa")]
    resueltas = df_a[df_a["Estado"].str.contains("Resuelta")]

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("🔴 Críticas activas",   int(len(activas[activas["Severidad"].str.contains("Crítico")])))
    c2.metric("⚠️ Advertencias activas",int(len(activas[activas["Severidad"].str.contains("Advertencia")])))
    c3.metric("✅ Resueltas (7 días)",  int(len(resueltas)))
    c4.metric("Total (7 días)",         int(len(df_a)))

    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns(3)
    tipo_f  = col_f1.multiselect("Tipo alarma", ["🔴 Crítico","⚠️ Advertencia"],
                                  default=["🔴 Crítico","⚠️ Advertencia"])
    estado_f= col_f2.multiselect("Estado", ["🔴 Activa","✅ Resuelta"],
                                  default=["🔴 Activa","✅ Resuelta"])
    equipo_f= col_f3.multiselect("Equipo", list(EQUIPOS.keys()),
                                  default=list(EQUIPOS.keys()))
    mask = (df_a["Severidad"].isin(tipo_f)) & \
           (df_a["Estado"].isin(estado_f)) & \
           (df_a["Equipo"].isin(equipo_f))
    df_f = df_a[mask]

    st.markdown("#### Alertas activas")
    for _, row in df_f[df_f["Estado"].str.contains("Activa")].iterrows():
        cls = "alert-critical" if "Crítico" in row["Severidad"] else "alert-warning"
        st.markdown(f"""
        <div class="{cls}">
          <b>{row['Severidad']} · {row['Equipo']}</b><br>
          Variable: <b>{row['Variable']}</b> = <b>{row['Valor']}</b>
          &nbsp;(límite: {row['Límite']}) · {row['Timestamp']}
        </div>""", unsafe_allow_html=True)

    st.markdown("#### Historial de alarmas")
    st.dataframe(df_f, hide_index=True, use_container_width=True)

    csv_a = io.StringIO()
    df_f.to_csv(csv_a, index=False)
    st.download_button("⬇️ Exportar alarmas CSV", csv_a.getvalue(),
                       file_name=f"alarmas_{datetime.now().strftime('%Y%m%d')}.csv",
                       mime="text/csv")

    st.markdown("---")
    ca, cb = st.columns(2)
    with ca:
        st.markdown("#### Por equipo")
        cnt = df_f.groupby("Equipo").size().reset_index(name="n").sort_values("n")
        fig_b = px.bar(cnt, x="n", y="Equipo", orientation="h",
                       color_discrete_sequence=[TEAL], labels={"n":"Alertas","Equipo":""})
        fig_b.update_layout(paper_bgcolor=CARD2,plot_bgcolor=CARD2,font_color="white",
                            height=260,margin=dict(l=10,r=10,t=10,b=25))
        st.plotly_chart(fig_b, use_container_width=True)
    with cb:
        st.markdown("#### Por severidad")
        cnt2 = df_f["Severidad"].value_counts().reset_index()
        cnt2.columns = ["Sev","n"]
        fig_p = px.pie(cnt2, values="n", names="Sev",
                       color_discrete_map={"🔴 Crítico":"#f44336","⚠️ Advertencia":"#FF9800"})
        fig_p.update_layout(paper_bgcolor=CARD2,font_color="white",
                            height=260,margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig_p, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: REPORTE DE PARÁMETROS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📊  Reporte de Parámetros":
    st.markdown("### Reporte de Parámetros Eléctricos")
    st.caption("Visualice, filtre y descargue el historial de cualquier equipo y variable")

    col1, col2, col3 = st.columns(3)
    eq_r   = col1.selectbox("Equipo",    list(EQUIPOS.keys()),  key="eq_rep")
    dias_r = col2.select_slider("Período", [7,14,30,60,90], value=30, key="dias_rep")
    df_r   = historico(eq_r, dias_r)
    var_r  = col3.selectbox("Variable",  list(vdict(eq_r).keys()), key="var_rep")

    # Filtro por rango de fechas
    min_d = pd.to_datetime(df_r["Timestamp"]).min().date()
    max_d = pd.to_datetime(df_r["Timestamp"]).max().date()
    d1, d2 = st.columns(2)
    fecha_ini = d1.date_input("Desde", min_d, min_value=min_d, max_value=max_d)
    fecha_fin = d2.date_input("Hasta", max_d, min_value=min_d, max_value=max_d)

    mask_d = (pd.to_datetime(df_r["Timestamp"]).dt.date >= fecha_ini) & \
             (pd.to_datetime(df_r["Timestamp"]).dt.date <= fecha_fin)
    df_fil = df_r[mask_d]

    # Gráfica
    color_r = EQUIPOS[eq_r]["color"]
    L_r     = vdict(eq_r)[var_r]
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatter(
        x=df_fil["Timestamp"], y=df_fil[var_r], mode="lines",
        line=dict(color=color_r, width=1.2), name=var_r,
        fill="tozeroy", fillcolor=f"rgba(38,198,218,0.06)",
    ))
    for lk, lc in [("ah","#FF9800"),("ch","#f44336"),("aw","#FF9800"),("cw","#f44336")]:
        if lk in L_r:
            fig_r.add_hline(y=L_r[lk], line_dash="dash", line_color=lc,
                            annotation_text=lk, annotation_font_color=lc)
    fig_r.update_layout(paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
                        height=360, xaxis=dict(gridcolor="#1e2d3e"),
                        yaxis=dict(title=var_r, gridcolor="#1e2d3e"),
                        margin=dict(l=55,r=15,t=10,b=45))
    st.plotly_chart(fig_r, use_container_width=True)

    st.markdown(f"**{len(df_fil):,} registros** · intervalo 5 min · "
                f"{fecha_ini} → {fecha_fin}")

    # Log / tabla paginada
    st.markdown("#### Log de eventos y parámetros")
    pg_size = 100
    pg = st.number_input("Página", min_value=1,
                         max_value=max(1,len(df_fil)//pg_size+1), value=1)
    st.dataframe(df_fil[[var_r,"Timestamp"]].iloc[(pg-1)*pg_size:pg*pg_size],
                 hide_index=True, use_container_width=True)

    # Exportar
    st.markdown("---")
    ca2, cb2, cc2 = st.columns(3)
    for fmt, label, col_btn in [
        ("csv","⬇️ CSV", ca2), ("csv","⬇️ Diario (resumen)", cb2),
    ]:
        buf = io.StringIO()
        if label == "⬇️ CSV":
            df_fil.to_csv(buf, index=False)
            data = buf.getvalue()
            fname = f"{eq_r.strip()}_{var_r}_{fecha_ini}_{fecha_fin}.csv"
        else:
            df_daily = df_fil.copy()
            df_daily["Fecha"] = pd.to_datetime(df_daily["Timestamp"]).dt.date
            d_res = df_daily.groupby("Fecha")[var_r].agg(["min","max","mean","std"]).reset_index()
            d_res.to_csv(buf, index=False)
            data = buf.getvalue()
            fname = f"resumen_diario_{eq_r.strip()}_{var_r}.csv"
        col_btn.download_button(label, data, file_name=fname, mime="text/csv",
                                use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: TRAZABILIDAD
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📋  Trazabilidad Incidentes":
    st.markdown("### Trazabilidad de Incidentes")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Incidentes (30 días)", len(INCIDENTES))
    c2.metric("Alta severidad",  sum(1 for i in INCIDENTES if i["severidad"]=="Alta"))
    c3.metric("Media severidad", sum(1 for i in INCIDENTES if i["severidad"]=="Media"))
    c4.metric("Tiempo prom.",    "2h 56min")

    st.markdown("---")
    tipos_sel = st.multiselect("Filtrar tipo de equipo",
                               ["UPS","Generador","A/C"],
                               default=["UPS","Generador","A/C"])

    for inc in INCIDENTES:
        if inc["tipo"] not in tipos_sel:
            continue
        sev_c = "#f44336" if inc["severidad"]=="Alta" else "#FF9800"
        est_c = "#4CAF50" if inc["estado"]=="Cerrado" else TEAL_L
        eq_c  = EQUIPOS.get(inc["equipo"],{}).get("color", TEAL)

        with st.expander(
            f"📋 {inc['id']}  ·  {inc['fecha']}  ·  {inc['equipo']}  —  {inc['descripcion']}"
        ):
            r1,r2,r3 = st.columns([3,1,1])
            with r1:
                st.markdown(f"**Causa raíz:** {inc['causa']}")
                st.markdown(f"**Duración:** `{inc['duracion']}`")
            r2.markdown(f"**Severidad:**<br><span style='color:{sev_c};font-weight:bold'>"
                        f"{inc['severidad']}</span>", unsafe_allow_html=True)
            r3.markdown(f"**Estado:**<br><span style='color:{est_c};font-weight:bold'>"
                        f"{inc['estado']}</span>", unsafe_allow_html=True)
            st.markdown("**Línea de tiempo:**")
            for j, acc in enumerate(inc["acciones"]):
                b_ = "🔴" if j==0 else "🟡" if j<=2 else "🟢"
                st.markdown(f"&nbsp;&nbsp;{b_}&nbsp; `{acc}`")

    st.markdown("---")
    ca_i, cb_i = st.columns(2)
    with ca_i:
        st.markdown("#### Incidentes por tipo")
        tc = {}
        for i in INCIDENTES:
            tc[i["tipo"]] = tc.get(i["tipo"],0)+1
        fig_ti = px.bar(pd.DataFrame(tc.items(),columns=["Tipo","n"]),
                        x="Tipo",y="n",color="Tipo",
                        color_discrete_map={"UPS":TEAL_L,"Generador":"#66BB6A","A/C":"#FFA726"},
                        labels={"n":"Incidentes"})
        fig_ti.update_layout(paper_bgcolor=CARD2,plot_bgcolor=CARD2,font_color="white",
                             height=260,showlegend=False,
                             yaxis=dict(gridcolor="#1e2d3e"),
                             margin=dict(l=40,r=10,t=10,b=40))
        st.plotly_chart(fig_ti, use_container_width=True)
    with cb_i:
        st.markdown("#### Tiempo de resolución (horas)")
        dur_map = {"INC-2026-041":1.75,"INC-2026-038":4.5,
                   "INC-2026-035":3.17,"INC-2026-031":2.33}
        df_dur = pd.DataFrame([{"Incidente":i["id"],"Horas":dur_map.get(i["id"],2),
                                 "Tipo":i["tipo"]} for i in INCIDENTES])
        fig_du = px.bar(df_dur,x="Incidente",y="Horas",color="Tipo",
                        color_discrete_map={"UPS":TEAL_L,"Generador":"#66BB6A","A/C":"#FFA726"},
                        labels={"Horas":"Horas hasta resolución"})
        fig_du.update_layout(paper_bgcolor=CARD2,plot_bgcolor=CARD2,font_color="white",
                             height=260,yaxis=dict(gridcolor="#1e2d3e"),
                             margin=dict(l=40,r=10,t=10,b=40))
        st.plotly_chart(fig_du, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: ARQUITECTURA
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🌐  Arquitectura del Sistema":
    st.markdown("### Arquitectura de Comunicación — LUXPOWER METRICS")

    st.markdown(f"""
    <div class="lux-card" style="margin-bottom:1rem;">
      <p style="color:#b0bec5;line-height:1.8;margin:0;">
        Los sensores de voltaje, corriente, temperatura y humedad se conectan directamente
        al equipo monitoreado (UPS, generador, AACC) a través de un <b style="color:{TEAL_L};">
        controlador inalámbrico</b>. El controlador transmite los datos a la nube mediante
        <b style="color:{TEAL_L};">red GSM con redundancia 4G/3G</b>, garantizando comunicación
        autónoma e independiente de la red del cliente.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Diagrama de arquitectura
    fig_arch = go.Figure()
    nodos = [
        ("Sensores\nUPS·GEN·A/C", 0.5, 0.85, "#1565C0", 0.18),
        ("Controlador\nInalámbrico",0.5, 0.65, TEAL_D,   0.18),
        ("Gateway /\nConcentrador", 0.5, 0.45, TEAL,     0.18),
        ("Red GSM\n4G / 3G",       0.2, 0.25, "#37474F", 0.15),
        ("Protocolo\nIoT / MQTT",  0.8, 0.25, "#37474F", 0.15),
        ("CLOUD\nLUXPOWER",        0.5, 0.12, TEAL_D,   0.20),
        ("NOC\n24/7",              0.15, 0.02, "#1B5E20", 0.13),
        ("Cliente A\nWeb/Móvil",   0.5,  0.02, "#4A148C", 0.13),
        ("Cliente B\nWeb/Móvil",   0.85, 0.02, "#4A148C", 0.13),
    ]
    for txt, x, y, col, sz in nodos:
        fig_arch.add_trace(go.Scatter(
            x=[x], y=[y], mode="markers+text",
            marker=dict(size=sz*180, color=col, opacity=0.85,
                        line=dict(color=TEAL_L, width=1)),
            text=[txt], textposition="middle center",
            textfont=dict(color="white", size=9),
            showlegend=False,
        ))
    for (x0,y0), (x1,y1) in [
        ((0.5,0.80),(0.5,0.72)), ((0.5,0.61),(0.5,0.53)),
        ((0.5,0.42),(0.2,0.31)), ((0.5,0.42),(0.8,0.31)),
        ((0.2,0.19),(0.5,0.17)), ((0.8,0.19),(0.5,0.17)),
        ((0.5,0.07),(0.15,0.05)),((0.5,0.07),(0.5,0.05)),
        ((0.5,0.07),(0.85,0.05)),
    ]:
        fig_arch.add_shape(type="line", x0=x0,y0=y0,x1=x1,y1=y1,
                           line=dict(color=TEAL_L,width=1.5,dash="dot"))

    fig_arch.update_layout(
        paper_bgcolor=CARD, plot_bgcolor=CARD, font_color="white",
        height=480, showlegend=False,
        xaxis=dict(visible=False, range=[0,1]),
        yaxis=dict(visible=False, range=[-0.05,1.0]),
        margin=dict(l=10,r=10,t=20,b=10),
    )
    st.plotly_chart(fig_arch, use_container_width=True)

    st.markdown("### Principales ventajas")
    ventajas = [
        (TEAL_L, "Tiempo real", "Parámetros críticos monitoreados en tiempo real vía IoT."),
        (TEAL_L, "Comunicación independiente", "Conexión 4G/3G/GSM redundante, sin depender de la red del cliente."),
        (TEAL_L, "Almacenamiento prolongado", "Datos y alarmas almacenados hasta 5 años."),
        (TEAL_L, "Alertas tempranas", "El sistema emite alerta si alguna variable se desvía de su rango normal."),
        (TEAL_L, "Trazabilidad", "Registro y trazabilidad de incidentes con historial completo."),
        (TEAL_L, "NOC 24/7", "Centro de control activo las 24h, 365 días. Técnico asignado para emergencias."),
        (TEAL_L, "Multi-nivel", "Roles y niveles de acceso jerárquico para distintos usuarios."),
        (TEAL_L, "Exportación", "Descarga de datos diaria, semanal, mensual o anual en CSV/Excel."),
    ]
    cols_v = st.columns(2)
    for i, (col, titulo, desc) in enumerate(ventajas):
        cols_v[i%2].markdown(f"""
        <div class="lux-card" style="margin-bottom:8px;border-left-color:{col};">
          <b style="color:{col};">✓ {titulo}</b>
          <span style="color:#90a4ae;font-size:0.85rem;"> — {desc}</span>
        </div>""", unsafe_allow_html=True)
