import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import time
import io
import json
import streamlit.components.v1 as components

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

# ─── DATOS: MEDIA TENSIÓN / TRANSFORMADORES / SENSORES / SOLAR / BATERÍAS ─────
EQUIPOS_MV = {
    "CELDA MV-1  Entrada":      {"kv":15.0,"i_a":320,"tipo":"Entrada",    "estado":"online", "color":TEAL_L},
    "CELDA MV-2  Protección":   {"kv":15.0,"i_a":280,"tipo":"Protección", "estado":"online", "color":TEAL},
    "CELDA MV-3  Medición":     {"kv":15.0,"i_a":305,"tipo":"Medición",   "estado":"online", "color":TEAL},
    "CELDA MV-4  Salida Trafo1":{"kv":15.0,"i_a":298,"tipo":"Salida",     "estado":"alarma", "color":"#FF9800"},
    "CELDA MV-5  Salida Trafo2":{"kv":15.0,"i_a":201,"tipo":"Salida",     "estado":"online", "color":TEAL_L},
    "CELDA MV-6  Seccionador":  {"kv":15.0,"i_a":  0,"tipo":"Seccionador","estado":"offline","color":"#607d8b"},
}
EQUIPOS_TRAFO = {
    "TRAFO-01  630 kVA": {"kv_p":15.0,"kv_s":0.44,"kva":630,"t_aceite":65.2,"carga_pct":72,"estado":"online"},
    "TRAFO-02  315 kVA": {"kv_p":15.0,"kv_s":0.22,"kva":315,"t_aceite":58.7,"carga_pct":58,"estado":"online"},
    "TRAFO-03  200 kVA": {"kv_p":15.0,"kv_s":0.22,"kva":200,"t_aceite":42.0,"carga_pct":15,"estado":"standby"},
}
SENSORES_AMB = {
    "Sala Servidores":    {"temp":21.5,"hum":48.0,"smoke":False,"water":False,"lim_t":24,"lim_h":60},
    "Sala UPS":           {"temp":22.0,"hum":50.0,"smoke":False,"water":False,"lim_t":25,"lim_h":65},
    "Sala Generadores":   {"temp":23.0,"hum":55.0,"smoke":False,"water":False,"lim_t":27,"lim_h":70},
    "Pasillo Central":    {"temp":24.5,"hum":52.0,"smoke":False,"water":False,"lim_t":28,"lim_h":70},
    "Sala Media Tensión": {"temp":28.2,"hum":45.0,"smoke":False,"water":False,"lim_t":35,"lim_h":65},
    "Bajo Piso / Foso":   {"temp": None,"hum":None, "smoke":False,"water":False,"lim_t":None,"lim_h":None},
}
EQUIPOS_SOLAR = {
    "Inversor FV-01  50 kW": {"p_kw":42.5,"p_max":50,"e_dia":285.3,"e_mes":5840,"pr":82.1,"estado":"online"},
    "Inversor FV-02  50 kW": {"p_kw":38.2,"p_max":50,"e_dia":261.7,"e_mes":5321,"pr":79.4,"estado":"online"},
    "Inversor FV-03  30 kW": {"p_kw": 0.0,"p_max":30,"e_dia":  0.0,"e_mes":3102,"pr": 0.0,"estado":"offline"},
}
BATERIAS = {
    "Banco Baterías A": {"soc":85,"soh":96,"v":48.2,"i":-12.5,"t_cel":28.3,"ciclos":142,"cap_kwh":120,"estado":"cargando"},
    "Banco Baterías B": {"soc":72,"soh":91,"v":47.8,"i": -8.2,"t_cel":27.1,"ciclos":198,"cap_kwh": 80,"estado":"cargando"},
    "Banco Baterías C": {"soc":35,"soh":78,"v":46.5,"i":  0.0,"t_cel":26.5,"ciclos":412,"cap_kwh": 60,"estado":"standby"},
}

# ─── FUNCIÓN: SALA 3D CON THREE.JS ────────────────────────────────────────────
def sala_3d_html(tick, height=500):
    statuses = {}
    for eq, info in EQUIPOS.items():
        if not info["online"]:
            statuses[eq] = "off"; continue
        vals = live_values(eq, tick)
        worst = "ok"
        for var, val in vals.items():
            L = vdict(eq)[var]
            s = estado_val(var, val, L)
            if s == "🔴": worst = "crit"; break
            elif s == "⚠️" and worst != "crit": worst = "warn"
        statuses[eq] = worst

    def st_(key): return statuses.get(key, "ok")

    equip_3d = [
        # Transformadores — gabinete color arena/beige (estilo carcasa metálica)
        {"name":"TRAFO-01 630kVA",  "val":"15kV→440V · 72%",  "x":-7.0,"z":-6.5,"w":2.5,"h":3.0,"d":1.5,"baseColor":0xc8c0a0,"status":"ok"},
        {"name":"TRAFO-02 315kVA",  "val":"15kV→220V · 58%",  "x":-4.2,"z":-6.5,"w":2.0,"h":2.8,"d":1.5,"baseColor":0xc8c0a0,"status":"ok"},
        # Celdas MV — blanco/gris claro estilo KYN28
        {"name":"CELDA MV-1",       "val":"15kV · 320A",       "x":-0.9,"z":-6.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0xd8dce4,"status":"ok"},
        {"name":"CELDA MV-2",       "val":"15kV · 280A",       "x": 0.2,"z":-6.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0xd8dce4,"status":"ok"},
        {"name":"CELDA MV-3",       "val":"15kV · 305A",       "x": 1.3,"z":-6.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0xd8dce4,"status":"ok"},
        {"name":"CELDA MV-4",       "val":"⚠ ALARMA · 298A",  "x": 2.4,"z":-6.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0xd8dce4,"status":"warn"},
        {"name":"CELDA MV-5",       "val":"15kV · 201A",       "x": 3.5,"z":-6.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0xd8dce4,"status":"ok"},
        # UPS — blanco grisáceo (gabinete tipo rack)
        {"name":"UPS-01 80kVA",     "val":"220V · Bat:85%",    "x":-5.0,"z":-1.0,"w":1.2,"h":2.2,"d":0.8,"baseColor":0xd0d8e0,"status":st_("UPS-01  (80 kVA)")},
        {"name":"UPS-02 40kVA",     "val":"220V · Bat:92%",    "x":-3.5,"z":-1.0,"w":1.0,"h":2.2,"d":0.8,"baseColor":0xd0d8e0,"status":st_("UPS-02  (40 kVA)")},
        # Generadores — verde-gris industrial
        {"name":"GEN-01 250kVA",    "val":"220V · 1500rpm",    "x": 5.5,"z":-2.0,"w":2.8,"h":1.8,"d":1.4,"baseColor":0xc8d4c4,"status":st_("GEN-01  (250 kVA)")},
        {"name":"GEN-02 150kVA",    "val":"OFFLINE",           "x": 5.5,"z": 0.5,"w":2.2,"h":1.6,"d":1.2,"baseColor":0xd4c8c8,"status":st_("GEN-02  (150 kVA)")},
        # Aires acondicionados — gris claro
        {"name":"AC-01 Servidores", "val":"21.5°C · 48%HR",   "x":-4.0,"z": 5.5,"w":0.9,"h":1.9,"d":0.6,"baseColor":0xe4e0d8,"status":st_("AC-01  Sala Servidores")},
        {"name":"AC-02 Sala UPS",   "val":"22.0°C · 50%HR",   "x":-2.5,"z": 5.5,"w":0.9,"h":1.9,"d":0.6,"baseColor":0xe4e0d8,"status":st_("AC-02  Sala UPS")},
        {"name":"AC-03 Generadores","val":"23.0°C · 55%HR",   "x":-1.0,"z": 5.5,"w":0.9,"h":1.9,"d":0.6,"baseColor":0xe4e0d8,"status":st_("AC-03  Sala Generadores")},
        # Tableros BT — gris azulado
        {"name":"TABLERO BT-1",     "val":"440V · 450A",       "x": 2.0,"z":-1.5,"w":0.9,"h":2.0,"d":0.5,"baseColor":0xd0d0e0,"status":"ok"},
        {"name":"TABLERO BT-2",     "val":"220V · 280A",       "x": 3.2,"z":-1.5,"w":0.9,"h":2.0,"d":0.5,"baseColor":0xd0d0e0,"status":"ok"},
    ]
    eq_json = json.dumps(equip_3d)
    H = height

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0e1a;overflow:hidden;font-family:monospace}}
#cc{{position:relative;width:100%;height:{H}px}}
canvas{{display:block;width:100%!important;height:{H}px!important}}
.lbl{{position:absolute;pointer-events:none;color:#d0eaff;font-size:10px;
      background:rgba(8,25,80,.88);padding:4px 10px;border-radius:5px;
      border:1px solid rgba(38,198,218,.65);white-space:nowrap;
      transform:translate(-50%,-115%);line-height:1.7;
      box-shadow:0 2px 8px rgba(0,80,200,.35)}}
.lbl.ok  {{border-color:rgba(76,175,80,.8)}}
.lbl.warn{{border-color:rgba(255,152,0,.9)}}
.lbl.crit{{border-color:rgba(244,67,54,.9)}}
.lbl.off {{border-color:rgba(96,125,139,.6);opacity:.55}}
#tip{{position:absolute;bottom:8px;right:10px;color:#37474f;font-size:9px}}
</style></head><body>
<div id="cc"><canvas id="c"></canvas><div id="lbls"></div>
<div id="tip">⟳ arrastrar · scroll zoom · clic-derecho pan</div></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.134.0/examples/js/controls/OrbitControls.js"></script>
<script>
const equipData={eq_json};
const cc=document.getElementById('cc');
const W=cc.clientWidth||900,H={H};
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x081428);
scene.fog=new THREE.Fog(0x081428,30,55);
const camera=new THREE.PerspectiveCamera(52,W/H,.1,100);
camera.position.set(10,12,17);
const renderer=new THREE.WebGLRenderer({{canvas:document.getElementById('c'),antialias:true}});
renderer.setSize(W,H);renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const ctrl=new THREE.OrbitControls(camera,renderer.domElement);
ctrl.enableDamping=true;ctrl.dampingFactor=.08;ctrl.target.set(0,1.5,0);
ctrl.maxPolarAngle=Math.PI/2.05;ctrl.minDistance=5;ctrl.maxDistance=38;
scene.add(new THREE.AmbientLight(0xc0d8f0,5.5));
const sun=new THREE.DirectionalLight(0xffffff,2.0);
sun.position.set(8,15,8);sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.near=.5;sun.shadow.camera.far=60;
sun.shadow.camera.left=sun.shadow.camera.bottom=-16;
sun.shadow.camera.right=sun.shadow.camera.top=16;
scene.add(sun);
scene.add(new THREE.DirectionalLight(0x26C6DA,.35));
const fl=new THREE.Mesh(new THREE.PlaneGeometry(28,24),new THREE.MeshLambertMaterial({{color:0x1535a0}}));
fl.rotation.x=-Math.PI/2;fl.receiveShadow=true;scene.add(fl);
const grid=new THREE.GridHelper(28,28,0x2040b0,0x1030a0);grid.position.y=.005;scene.add(grid);
const wallM=new THREE.MeshLambertMaterial({{color:0x0e1e50,side:THREE.BackSide}});
const roomM=new THREE.Mesh(new THREE.BoxGeometry(28,10,24),wallM);
roomM.position.y=5;scene.add(roomM);
for(let x=-9;x<=9;x+=9)for(let z=-7;z<=7;z+=7){{
  const pl=new THREE.PointLight(0x26C6DA,.35,15);pl.position.set(x,9,z);scene.add(pl);
  const fx=new THREE.Mesh(new THREE.BoxGeometry(1.8,.07,.28),new THREE.MeshBasicMaterial({{color:0x1a4a5a}}));
  fx.position.set(x,9.8,z);scene.add(fx);
}}
const SC={{ok:0x4CAF50,warn:0xFF9800,crit:0xf44336,off:0x607d8b}};
const groups=[];
function mkEq(e){{
  const g=new THREE.Group();g.position.set(e.x,e.h/2,e.z);
  const body=new THREE.Mesh(new THREE.BoxGeometry(e.w,e.h,e.d),
    new THREE.MeshPhongMaterial({{color:e.baseColor,specular:0x777777,shininess:90}}));
  body.castShadow=true;body.receiveShadow=true;g.add(body);
  const stripe=new THREE.Mesh(new THREE.BoxGeometry(e.w+.01,0.13,e.d+.01),
    new THREE.MeshBasicMaterial({{color:0xCC2222}}));
  stripe.position.set(0,e.h/2-0.065,0);g.add(stripe);
  const sc=SC[e.status]||SC.ok;
  g.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(e.w,e.h,e.d)),
    new THREE.LineBasicMaterial({{color:sc}})));
  const panC=e.status==='ok'?0x003018:e.status==='warn'?0x301800:e.status==='crit'?0x300000:0x101010;
  const pan=new THREE.Mesh(new THREE.PlaneGeometry(e.w*.88,e.h*.82),
    new THREE.MeshBasicMaterial({{color:panC,opacity:.75,transparent:true}}));
  pan.position.set(0,0,e.d/2+.01);g.add(pan);
  for(let i=-2;i<=2;i++){{
    const ln=new THREE.Mesh(new THREE.PlaneGeometry(e.w*.82,.022),
      new THREE.MeshBasicMaterial({{color:sc,opacity:.45,transparent:true}}));
    ln.position.set(0,i*e.h*.17,e.d/2+.015);g.add(ln);
  }}
  const led=new THREE.Mesh(new THREE.SphereGeometry(.07,8,8),new THREE.MeshBasicMaterial({{color:sc}}));
  led.position.set(e.w/2-.12,e.h/2-.12,e.d/2+.01);g.add(led);
  const ll=new THREE.PointLight(sc,e.status==='off'?.05:.6,2.5);
  ll.position.copy(led.position);g.add(ll);
  g.userData={{...e,ll}};
  scene.add(g);groups.push(g);
}}
equipData.forEach(mkEq);
const lblsDiv=document.getElementById('lbls');
const lblEls=equipData.map(e=>{{
  const d=document.createElement('div');
  d.className='lbl '+e.status;
  d.innerHTML='<b>'+e.name+'</b><br><span style="color:#90a4ae">'+e.val+'</span>';
  lblsDiv.appendChild(d);return d;
}});
function proj(p3){{
  const v=p3.clone().project(camera);
  return{{x:(v.x+1)/2*W,y:-(v.y-1)/2*H,z:v.z}};
}}
const clk=new THREE.Clock();
(function animate(){{
  requestAnimationFrame(animate);
  const t=clk.getElapsedTime();
  groups.forEach(g=>{{
    const s=g.userData.status,ll=g.userData.ll;
    if(s==='crit')ll.intensity=.4+.7*Math.abs(Math.sin(t*3.2));
    else if(s==='warn')ll.intensity=.4+.35*Math.abs(Math.sin(t*1.6));
    else if(s==='off')ll.intensity=0;
    else ll.intensity=.55;
  }});
  ctrl.update();renderer.render(scene,camera);
  groups.forEach((g,i)=>{{
    const tp=g.position.clone();tp.y+=equipData[i].h/2+.7;
    const sc=proj(tp),lb=lblEls[i];
    lb.style.display=sc.z<1?'block':'none';
    lb.style.left=sc.x+'px';lb.style.top=sc.y+'px';
  }});
}})();
</script></body></html>"""

# ─── FUNCIÓN: DIAGRAMA UNIFILAR SVG ───────────────────────────────────────────
def unifilar_html(tick):
    rng = np.random.default_rng(tick % 9999)
    def nv(b, n): return b + float(rng.uniform(-n, n))

    feeders = [
        {"x":140,"name":"MV-1 ENTRADA",  "sub":"Red 15kV",         "ia":nv(320,5),"ib":nv(318,5),"ic":nv(321,5),"p":nv(4.82,.2),"q":nv(1.21,.1),"pf":nv(0.943,.008),"epi":85230,"state":"closed","alarm":False,"arrow_up":True},
        {"x":300,"name":"MV-2 PROTECC.", "sub":"Protección",        "ia":nv(280,4),"ib":nv(278,4),"ic":nv(282,4),"p":nv(4.12,.15),"q":nv(0.98,.08),"pf":nv(0.972,.006),"epi":72100,"state":"closed","alarm":False,"arrow_up":False},
        {"x":460,"name":"MV-3 MEDICIÓN", "sub":"TC + TP zona A",    "ia":nv(305,4),"ib":nv(303,4),"ic":nv(307,4),"p":nv(4.51,.15),"q":nv(1.05,.08),"pf":nv(0.974,.006),"epi":78500,"state":"closed","alarm":False,"arrow_up":False},
        {"x":620,"name":"MV-4 SAL-T1",   "sub":"→ TRAFO-01 630kVA", "ia":nv(298,6),"ib":nv(296,6),"ic":nv(300,6),"p":nv(4.45,.2),"q":nv(1.15,.1),"pf":nv(0.968,.01),"epi":76820,"state":"closed","alarm":True,"arrow_up":False},
        {"x":780,"name":"MV-5 SAL-T2",   "sub":"→ TRAFO-02 315kVA", "ia":nv(201,4),"ib":nv(199,4),"ic":nv(203,4),"p":nv(2.98,.1),"q":nv(0.74,.07),"pf":nv(0.970,.006),"epi":51230,"state":"closed","alarm":False,"arrow_up":False},
        {"x":940,"name":"MV-6 SECCION.", "sub":"Seccionador",        "ia":0,"ib":0,"ic":0,"p":0,"q":0,"pf":1.0,"epi":0,"state":"open","alarm":False,"arrow_up":False},
    ]

    svg_parts = []
    for f in feeders:
        x = f["x"]
        lc  = "#FF9800" if f["alarm"] else "#607d8b" if f["state"]=="open" else "#CC2222"
        led = "#FF9800" if f["alarm"] else "#607d8b" if f["state"]=="open" else "#4CAF50"
        dash = 'stroke-dasharray="8,5"' if f["state"]=="open" else ""
        gc   = "#607d8b" if f["state"]=="open" else "#4CAF50"

        if f.get("arrow_up"):
            svg_parts += [
                f'<line x1="{x}" y1="44" x2="{x}" y2="86" stroke="#CC2222" stroke-width="3"/>',
                f'<polygon points="{x},44 {x-8},60 {x+8},60" fill="#CC2222"/>',
                f'<text x="{x}" y="40" fill="#90a4ae" font-size="9" text-anchor="middle" font-family="monospace">RED 15kV</text>',
            ]
        svg_parts += [
            f'<line x1="{x}" y1="200" x2="{x}" y2="450" stroke="{lc}" stroke-width="2.5" {dash}/>',
            f'<rect x="{x-13}" y="262" width="26" height="16" fill="#060d1e" stroke="{lc}" stroke-width="2" rx="2"/>',
        ]
        if f["state"]=="closed":
            svg_parts.append(f'<line x1="{x-10}" y1="270" x2="{x+10}" y2="270" stroke="{led}" stroke-width="2.5"/>')
        else:
            svg_parts.append(f'<line x1="{x-9}" y1="265" x2="{x+9}" y2="275" stroke="#607d8b" stroke-width="1.8"/>')
        svg_parts += [
            f'<ellipse cx="{x}" cy="332" rx="13" ry="7" fill="none" stroke="#FF9800" stroke-width="1.5"/>',
            f'<circle cx="{x+16}" cy="270" r="5" fill="{led}"/>',
            f'<polygon points="{x},450 {x-17},472 {x+17},472" fill="none" stroke="{gc}" stroke-width="2"/>',
            f'<line x1="{x}" y1="472" x2="{x}" y2="488" stroke="{gc}" stroke-width="2"/>',
            f'<line x1="{x-13}" y1="488" x2="{x+13}" y2="488" stroke="{gc}" stroke-width="2"/>',
            f'<line x1="{x-8}" y1="495" x2="{x+8}" y2="495" stroke="{gc}" stroke-width="1.5"/>',
            f'<line x1="{x-3}" y1="502" x2="{x+3}" y2="502" stroke="{gc}" stroke-width="1"/>',
            f'<text x="{x}" y="197" fill="#546e7a" font-size="8.5" text-anchor="middle" font-family="monospace">{f["name"]}</text>',
        ]
        bx, by, bw, bh = x-80, 520, 160, 100 if f["state"]!="open" else 38
        aks = "#FF9800" if f["alarm"] else "#1a2d3e"
        svg_parts += [
            f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="3" fill="rgba(6,14,32,.92)" stroke="{aks}" stroke-width="1.2"/>',
            f'<text x="{x}" y="{by+13}" fill="{"#FF9800" if f["alarm"] else "#26C6DA"}" font-size="9" text-anchor="middle" font-family="monospace" font-weight="bold">{f["name"]}</text>',
            f'<text x="{x}" y="{by+25}" fill="#546e7a" font-size="8" text-anchor="middle" font-family="monospace">{f["sub"]}</text>',
        ]
        if f["state"] != "open":
            y0 = by + 38
            svg_parts += [
                f'<text x="{bx+5}" y="{y0}" fill="#90a4ae" font-size="8" font-family="monospace">Ia <tspan fill="white">{f["ia"]:.0f}A</tspan>  Ib <tspan fill="white">{f["ib"]:.0f}A</tspan>  Ic <tspan fill="white">{f["ic"]:.0f}A</tspan></text>',
                f'<text x="{bx+5}" y="{y0+14}" fill="#90a4ae" font-size="8" font-family="monospace">P <tspan fill="#4CAF50">{f["p"]:.2f}kW</tspan>   Q <tspan fill="white">{f["q"]:.2f}kVar</tspan>   PF <tspan fill="white">{f["pf"]:.3f}</tspan></text>',
                f'<text x="{bx+5}" y="{y0+28}" fill="#90a4ae" font-size="8" font-family="monospace">EPI <tspan fill="#FDD835">{f["epi"]:,.0f} kWh</tspan></text>',
                f'<text x="{bx+5}" y="{y0+42}" fill="#546e7a" font-size="7.5" font-family="monospace">Ua {nv(15.0,.05):.2f}kV  Ub {nv(15.0,.05):.2f}kV  Uc {nv(15.0,.05):.2f}kV</text>',
            ]
        else:
            svg_parts.append(f'<text x="{x}" y="{by+32}" fill="#607d8b" font-size="8.5" text-anchor="middle" font-family="monospace">ABIERTO / SIN CARGA</text>')

    body = "\n  ".join(svg_parts)
    ts   = datetime.now().strftime("%H:%M:%S")

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0}}body{{background:#060d1e;overflow:hidden}}</style>
</head><body>
<svg viewBox="0 0 1080 645" style="width:100%;height:645px;background:#060d1e">
  <!-- Header -->
  <rect x="0" y="0" width="1080" height="36" fill="#0a1628"/>
  <text x="540" y="23" fill="#26C6DA" font-size="13" font-family="monospace"
        text-anchor="middle" font-weight="bold">
    CENTROSUR · DIAGRAMA UNIFILAR SUBESTACIÓN 15 kV
  </text>
  <circle cx="18" cy="18" r="5" fill="#4CAF50">
    <animate attributeName="opacity" values="1;0.15;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="28" y="22" fill="#4CAF50" font-size="8" font-family="monospace">EN VIVO</text>
  <text x="1070" y="22" fill="#546e7a" font-size="8" font-family="monospace" text-anchor="end">{ts}</text>

  <!-- Transformer -->
  <line x1="140" y1="36" x2="140" y2="68" stroke="#CC2222" stroke-width="3"/>
  <circle cx="140" cy="93" r="24" fill="none" stroke="#CC2222" stroke-width="2.5"/>
  <circle cx="140" cy="140" r="24" fill="none" stroke="#CC2222" stroke-width="2.5"/>
  <text x="140" y="97" fill="#CC2222" font-size="11" text-anchor="middle">Y</text>
  <text x="140" y="145" fill="#CC2222" font-size="10" text-anchor="middle">Δ</text>
  <line x1="140" y1="164" x2="140" y2="200" stroke="#CC2222" stroke-width="3"/>
  <!-- Trafo data -->
  <rect x="170" y="72" width="150" height="88" rx="3" fill="rgba(6,14,32,.9)" stroke="#1a2d3e" stroke-width="1"/>
  <text x="177" y="87" fill="#FDD835" font-size="9" font-family="monospace" font-weight="bold">TRAFO-P  630 kVA</text>
  <text x="177" y="101" fill="#90a4ae" font-size="8.5" font-family="monospace">66 kV / 15 kV  Dyn11</text>
  <text x="177" y="115" fill="#90a4ae" font-size="8.5" font-family="monospace">Carga: <tspan fill="#4CAF50">72%</tspan>   T° <tspan fill="white">65.2°C</tspan></text>
  <text x="177" y="129" fill="#90a4ae" font-size="8.5" font-family="monospace">EPI: <tspan fill="#FDD835">485,230 kWh</tspan></text>
  <text x="177" y="143" fill="#90a4ae" font-size="8.5" font-family="monospace">Estado: <tspan fill="#4CAF50">NORMAL</tspan></text>
  <text x="177" y="157" fill="#546e7a" font-size="8" font-family="monospace">Pn: 344.1 kW  Qn: -4.1 kVar</text>

  <!-- 15kV BUSBAR -->
  <line x1="50" y1="200" x2="1030" y2="200" stroke="#CC2222" stroke-width="6"/>
  <rect x="50" y="193" width="980" height="4" fill="rgba(204,0,0,.2)"/>
  <text x="28" y="205" fill="#CC2222" font-size="10" font-family="monospace" font-weight="bold">15kV</text>

  <!-- FEEDERS -->
  {body}

  <!-- Legend -->
  <rect x="940" y="44" width="130" height="148" rx="4" fill="rgba(6,14,32,.92)" stroke="#1a2d3e" stroke-width="1"/>
  <text x="948" y="60" fill="#26C6DA" font-size="9" font-family="monospace" font-weight="bold">LEYENDA</text>
  <line x1="948" y1="72" x2="968" y2="72" stroke="#CC2222" stroke-width="2.5"/>
  <text x="973" y="75" fill="#90a4ae" font-size="8" font-family="monospace">Conductor 15kV</text>
  <rect x="948" y="82" width="16" height="10" fill="none" stroke="#4CAF50" stroke-width="1.5" rx="1"/>
  <line x1="948" y1="87" x2="964" y2="87" stroke="#4CAF50" stroke-width="2"/>
  <text x="973" y="91" fill="#90a4ae" font-size="8" font-family="monospace">Inter. cerrado</text>
  <rect x="948" y="98" width="16" height="10" fill="none" stroke="#607d8b" stroke-width="1.5" rx="1"/>
  <line x1="950" y1="100" x2="964" y2="108" stroke="#607d8b" stroke-width="1.5"/>
  <text x="973" y="107" fill="#90a4ae" font-size="8" font-family="monospace">Inter. abierto</text>
  <ellipse cx="956" cy="122" rx="9" ry="5" fill="none" stroke="#FF9800" stroke-width="1.5"/>
  <text x="973" y="125" fill="#90a4ae" font-size="8" font-family="monospace">TC (transf. corriente)</text>
  <polygon points="956,135 948,150 964,150" fill="none" stroke="#4CAF50" stroke-width="1.5"/>
  <text x="973" y="146" fill="#90a4ae" font-size="8" font-family="monospace">Tierra / neutro</text>
  <circle cx="956" cy="162" r="5" fill="#FF9800"/>
  <text x="973" y="165" fill="#90a4ae" font-size="8" font-family="monospace">Alarma activa</text>
  <circle cx="956" cy="178" r="5" fill="#4CAF50"/>
  <text x="973" y="181" fill="#90a4ae" font-size="8" font-family="monospace">Normal / OK</text>
</svg>
</body></html>"""

# ─── FUNCIÓN: DIAGRAMA DE STRINGS FV ──────────────────────────────────────────
def pv_string_html():
    rng = np.random.default_rng(int(time.time()//120))
    def nv(b,n): return b + float(rng.uniform(-n,n))
    strings = [
        {"label":"String 1A","panels":12,"vdc":nv(502,8),"idc":nv(2.1,.15),"kwp":11.5,"side":"left"},
        {"label":"String 1B","panels":12,"vdc":nv(498,8),"idc":nv(2.05,.15),"kwp":11.5,"side":"left"},
        {"label":"String 2A","panels":12,"vdc":nv(582,8),"idc":nv(3.0,.2),"kwp":11.5,"side":"right"},
        {"label":"String 2B","panels":12,"vdc":nv(599,8),"idc":nv(1.9,.15),"kwp":11.5,"side":"right"},
    ]
    inv = [
        {"id":"INV-01","brand":"GoodWe","model":"GW20K-DT","pmax_dc":26,"pmax_ac":20,
         "ua":nv(235.2,.8),"ub":nv(224,.8),"uc":nv(237.1,.8),
         "ia":nv(4.7,.3),"ib":nv(4.7,.3),"ic":nv(4.7,.3),
         "p_kw":nv(3.47,.2),"pf":"—","hz":50.0,"x":230},
        {"id":"INV-02","brand":"GoodWe","model":"GW20K-DT","pmax_dc":26,"pmax_ac":20,
         "ua":nv(235.2,.8),"ub":nv(224,.8),"uc":nv(237.1,.8),
         "ia":nv(5.4,.3),"ib":nv(5.3,.3),"ic":nv(5.3,.3),
         "p_kw":nv(3.83,.2),"pf":"—","hz":50.0,"x":730},
    ]
    total_kw = sum(v["p_kw"] for v in inv)
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0}}body{{background:#050b10;overflow:hidden;font-family:monospace}}</style>
</head><body>
<svg viewBox="0 0 1000 560" style="width:100%;height:560px;background:#050b10">
  <!-- Title -->
  <rect x="0" y="0" width="1000" height="34" fill="#080f14"/>
  <text x="500" y="22" fill="#FDD835" font-size="12" text-anchor="middle" font-weight="bold" font-family="monospace">
    CENTROSUR · DIAGRAMA FV — SISTEMA 47 kWp · Generación actual: {total_kw:.2f} kW
  </text>

  <!-- Left strings (INV-01) -->
  <!-- String 1A -->
  <!-- Solar panels row (3 panels icon) -->
  <rect x="60" y="44" width="160" height="60" rx="4" fill="rgba(20,40,20,.8)" stroke="#4CAF50" stroke-width="1.5"/>
  <text x="140" y="62" fill="#FDD835" font-size="9" text-anchor="middle">String 1A  12×250W</text>
  <text x="140" y="76" fill="white" font-size="9" text-anchor="middle">U:{strings[0]["vdc"]:.0f}V  I:{strings[0]["idc"]:.2f}A</text>
  <text x="140" y="90" fill="#90a4ae" font-size="8" text-anchor="middle">11.5 kWp</text>
  <!-- String 1B -->
  <rect x="60" y="120" width="160" height="60" rx="4" fill="rgba(20,40,20,.8)" stroke="#4CAF50" stroke-width="1.5"/>
  <text x="140" y="138" fill="#FDD835" font-size="9" text-anchor="middle">String 1B  12×250W</text>
  <text x="140" y="152" fill="white" font-size="9" text-anchor="middle">U:{strings[1]["vdc"]:.0f}V  I:{strings[1]["idc"]:.2f}A</text>
  <text x="140" y="166" fill="#90a4ae" font-size="8" text-anchor="middle">11.5 kWp</text>

  <!-- Lines to INV-01 -->
  <line x1="220" y1="74" x2="310" y2="250" stroke="#FDD835" stroke-width="1.8" stroke-dasharray="6,3"/>
  <line x1="220" y1="150" x2="310" y2="250" stroke="#FDD835" stroke-width="1.8" stroke-dasharray="6,3"/>
  <text x="140" y="110" fill="#FF9800" font-size="8" text-anchor="middle">Total: 23 kWp</text>

  <!-- Right strings (INV-02) -->
  <rect x="770" y="44" width="160" height="60" rx="4" fill="rgba(20,40,20,.8)" stroke="#4CAF50" stroke-width="1.5"/>
  <text x="850" y="62" fill="#FDD835" font-size="9" text-anchor="middle">String 2A  12×250W</text>
  <text x="850" y="76" fill="white" font-size="9" text-anchor="middle">U:{strings[2]["vdc"]:.0f}V  I:{strings[2]["idc"]:.2f}A</text>
  <text x="850" y="90" fill="#90a4ae" font-size="8" text-anchor="middle">11.5 kWp</text>
  <rect x="770" y="120" width="160" height="60" rx="4" fill="rgba(20,40,20,.8)" stroke="#4CAF50" stroke-width="1.5"/>
  <text x="850" y="138" fill="#FDD835" font-size="9" text-anchor="middle">String 2B  12×250W</text>
  <text x="850" y="152" fill="white" font-size="9" text-anchor="middle">U:{strings[3]["vdc"]:.0f}V  I:{strings[3]["idc"]:.2f}A</text>
  <text x="850" y="166" fill="#90a4ae" font-size="8" text-anchor="middle">11.5 kWp</text>
  <line x1="770" y1="74" x2="690" y2="250" stroke="#FDD835" stroke-width="1.8" stroke-dasharray="6,3"/>
  <line x1="770" y1="150" x2="690" y2="250" stroke="#FDD835" stroke-width="1.8" stroke-dasharray="6,3"/>
  <text x="850" y="110" fill="#FF9800" font-size="8" text-anchor="middle">Total: 24 kWp</text>

  <!-- Inverter 1 -->
  <rect x="250" y="218" width="175" height="115" rx="5" fill="rgba(30,18,0,.9)" stroke="#FF9800" stroke-width="2"/>
  <text x="337" y="236" fill="#FF9800" font-size="10" text-anchor="middle" font-weight="bold">1# Inversor</text>
  <text x="337" y="249" fill="#90a4ae" font-size="8" text-anchor="middle">{inv[0]["brand"]} {inv[0]["model"]}</text>
  <text x="258" y="263" fill="#90a4ae" font-size="8">Ua:{inv[0]["ua"]:.1f}V  Ub:{inv[0]["ub"]:.1f}V</text>
  <text x="258" y="276" fill="#FF9800" font-size="8">Uc:<tspan fill="white">{inv[0]["uc"]:.1f}V</tspan></text>
  <text x="258" y="289" fill="#90a4ae" font-size="8">Ia:{inv[0]["ia"]:.2f}A  Ib:{inv[0]["ib"]:.2f}A  Ic:{inv[0]["ic"]:.2f}A</text>
  <text x="258" y="302" fill="#90a4ae" font-size="8">P_ac: <tspan fill="#4CAF50">{inv[0]["p_kw"]:.2f} kW</tspan>   Hz: {inv[0]["hz"]:.1f}</text>
  <text x="258" y="315" fill="#546e7a" font-size="7.5">Máx DC: {inv[0]["pmax_dc"]}kW  Máx AC: {inv[0]["pmax_ac"]}kW</text>

  <!-- Inverter 2 -->
  <rect x="575" y="218" width="175" height="115" rx="5" fill="rgba(30,18,0,.9)" stroke="#FF9800" stroke-width="2"/>
  <text x="662" y="236" fill="#FF9800" font-size="10" text-anchor="middle" font-weight="bold">2# Inversor</text>
  <text x="662" y="249" fill="#90a4ae" font-size="8" text-anchor="middle">{inv[1]["brand"]} {inv[1]["model"]}</text>
  <text x="583" y="263" fill="#90a4ae" font-size="8">Ua:{inv[1]["ua"]:.1f}V  Ub:{inv[1]["ub"]:.1f}V</text>
  <text x="583" y="276" fill="#FF9800" font-size="8">Uc:<tspan fill="white">{inv[1]["uc"]:.1f}V</tspan></text>
  <text x="583" y="289" fill="#90a4ae" font-size="8">Ia:{inv[1]["ia"]:.2f}A  Ib:{inv[1]["ib"]:.2f}A  Ic:{inv[1]["ic"]:.2f}A</text>
  <text x="583" y="302" fill="#90a4ae" font-size="8">P_ac: <tspan fill="#4CAF50">{inv[1]["p_kw"]:.2f} kW</tspan>   Hz: {inv[1]["hz"]:.1f}</text>
  <text x="583" y="315" fill="#546e7a" font-size="7.5">Máx DC: {inv[1]["pmax_dc"]}kW  Máx AC: {inv[1]["pmax_ac"]}kW</text>

  <!-- AC wires inverter → AC bus box -->
  <line x1="337" y1="333" x2="337" y2="390" stroke="#FF9800" stroke-width="2"/>
  <line x1="662" y1="333" x2="662" y2="390" stroke="#FF9800" stroke-width="2"/>
  <line x1="337" y1="390" x2="662" y2="390" stroke="#FF9800" stroke-width="2.5"/>
  <line x1="500" y1="390" x2="500" y2="410" stroke="#FF9800" stroke-width="2"/>

  <!-- AC Bus Box -->
  <rect x="438" y="408" width="124" height="38" rx="4" fill="rgba(30,18,0,.85)" stroke="#FF9800" stroke-width="1.8"/>
  <text x="500" y="422" fill="#FDD835" font-size="9" text-anchor="middle" font-weight="bold">Caja AC Bus</text>
  <text x="500" y="438" fill="#90a4ae" font-size="8" text-anchor="middle">P total: {total_kw:.2f} kW</text>
  <line x1="500" y1="446" x2="500" y2="476" stroke="#FF9800" stroke-width="2"/>

  <!-- Medidor / Grid tie -->
  <rect x="456" y="474" width="88" height="32" rx="3" fill="rgba(10,25,10,.85)" stroke="#4CAF50" stroke-width="1.5"/>
  <text x="500" y="488" fill="#4CAF50" font-size="8.5" text-anchor="middle" font-weight="bold">⚡ MEDIDOR</text>
  <text x="500" y="500" fill="#90a4ae" font-size="7.5" text-anchor="middle">10kV / Baja tensión</text>
  <line x1="500" y1="506" x2="500" y2="530" stroke="#4CAF50" stroke-width="2"/>

  <!-- Grid symbol -->
  <line x1="460" y1="530" x2="540" y2="530" stroke="#4CAF50" stroke-width="2.5"/>
  <line x1="468" y1="538" x2="532" y2="538" stroke="#4CAF50" stroke-width="2"/>
  <line x1="478" y1="546" x2="522" y2="546" stroke="#4CAF50" stroke-width="1.5"/>
  <line x1="490" y1="554" x2="510" y2="554" stroke="#4CAF50" stroke-width="1"/>
  <text x="500" y="530" fill="#4CAF50" font-size="8" text-anchor="middle">RED</text>
</svg>
</body></html>"""

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
        "🏭  Sala 3D · Equipos",
        "🔲  Diagrama Unifilar",
        "⚡  Monitoreo UPS",
        "🔋  Monitoreo Generadores",
        "❄️  Monitoreo A/C",
        "🔌  Media Tensión 3D",
        "🌡️  Ambiente & Sensores",
        "📈  Análisis Energético",
        "☀️  Solar FV",
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

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: SALA 3D · EQUIPOS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🏭  Sala 3D · Equipos":
    st.markdown("### Sala de Equipos — Vista 3D Interactiva")
    st.caption("Arrastrar para rotar · Scroll para zoom · Clic derecho para desplazar")

    tick = int(time.time() // 10)
    components.html(sala_3d_html(tick, height=510), height=515, scrolling=False)

    st.markdown("---")
    st.markdown("#### Estado en tiempo real")
    cols_3d = st.columns(min(len(EQUIPOS), 4))
    for i, (eq, info) in enumerate(EQUIPOS.items()):
        vals = live_values(eq, tick)
        var0, val0 = list(vals.items())[0]
        est = estado_val(var0, val0, vdict(eq)[var0])
        dot = "🟢" if info["online"] else "🔴"
        cols_3d[i % 4].markdown(f"""
        <div style="background:#111827;border-radius:8px;padding:8px 10px;margin-bottom:6px;
             border-left:3px solid {info['color']};">
          <div style="color:{info['color']};font-size:0.68rem;font-weight:600;">{dot} {eq.split('(')[0].strip()}</div>
          <div style="color:white;font-size:0.85rem;">{est} {fmt_val(var0, val0)}</div>
          <div style="color:#546e7a;font-size:0.7rem;">{info['tipo']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    ca3, cb3, cc3 = st.columns(3)
    mv_ok  = sum(1 for v in EQUIPOS_MV.values()   if v["estado"]=="online")
    tr_ok  = sum(1 for v in EQUIPOS_TRAFO.values() if v["estado"]=="online")
    bat_ok = sum(1 for v in BATERIAS.values()      if v["estado"]!="falla")
    ca3.metric("Celdas MV online",        f"{mv_ok}/{len(EQUIPOS_MV)}")
    cb3.metric("Transformadores activos", f"{tr_ok}/{len(EQUIPOS_TRAFO)}")
    cc3.metric("Bancos batería OK",       f"{bat_ok}/{len(BATERIAS)}")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: MEDIA TENSIÓN 3D
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🔌  Media Tensión 3D":
    st.markdown("### Subestación Media Tensión — 15 kV")
    st.caption("Celdas de media tensión · Transformadores de distribución")

    # KPIs
    c1m, c2m, c3m, c4m = st.columns(4)
    mv_online = sum(1 for v in EQUIPOS_MV.values() if v["estado"]=="online")
    c1m.metric("Celdas MV online",  f"{mv_online}/{len(EQUIPOS_MV)}")
    c2m.metric("Tensión nominal",   "15 kV")
    c3m.metric("Trafo principal",   "630 kVA · 72%")
    c4m.metric("T° aceite TRAFO-01","65.2 °C")

    st.markdown("---")
    col_mv, col_tr = st.columns([1.1, 1])

    with col_mv:
        st.markdown("#### Celdas de Media Tensión")
        for celda, v in EQUIPOS_MV.items():
            est_c = "#4CAF50" if v["estado"]=="online" else "#FF9800" if v["estado"]=="alarma" else "#607d8b"
            icon  = "🟢" if v["estado"]=="online" else "⚠️" if v["estado"]=="alarma" else "🔴"
            st.markdown(f"""
            <div style="background:#111827;border-radius:8px;padding:10px 14px;margin-bottom:6px;
                 border-left:4px solid {est_c};">
              <span style="color:{est_c};font-weight:700;">{icon} {celda}</span>
              <span style="color:#90a4ae;font-size:0.82rem;"> · {v['tipo']}</span>
              <span style="float:right;color:white;font-size:0.9rem;font-weight:600;">
                {v['kv']:.1f} kV &nbsp; | &nbsp; {v['i_a']} A
              </span>
            </div>""", unsafe_allow_html=True)

        # 3D mini vista de sala MV
        st.markdown("#### Vista 3D — Sala Media Tensión")
        mv_3d = [
            {"name":"TRAFO-01 630kVA","val":"15kV→440V · 65.2°C","x":-4.5,"z":-1,"w":2.5,"h":3.0,"d":1.5,"baseColor":0x1a1200,"status":"ok"},
            {"name":"TRAFO-02 315kVA","val":"15kV→220V · 58.7°C","x":-1.5,"z":-1,"w":2.0,"h":2.8,"d":1.5,"baseColor":0x1a1200,"status":"ok"},
            {"name":"TRAFO-03 200kVA","val":"STANDBY · 42°C",    "x": 1.0,"z":-1,"w":1.8,"h":2.5,"d":1.5,"baseColor":0x150808,"status":"off"},
            {"name":"CELDA MV-1","val":"15kV · 320A","x":-5.0,"z":2.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0x0d1520,"status":"ok"},
            {"name":"CELDA MV-2","val":"15kV · 280A","x":-4.0,"z":2.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0x0d1520,"status":"ok"},
            {"name":"CELDA MV-3","val":"15kV · 305A","x":-3.0,"z":2.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0x0d1520,"status":"ok"},
            {"name":"CELDA MV-4","val":"⚠ 298A ALARMA", "x":-2.0,"z":2.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0x0d1520,"status":"warn"},
            {"name":"CELDA MV-5","val":"15kV · 201A","x":-1.0,"z":2.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0x0d1520,"status":"ok"},
            {"name":"CELDA MV-6","val":"OFFLINE",     "x": 0.0,"z":2.5,"w":0.8,"h":2.5,"d":1.0,"baseColor":0x0d1520,"status":"off"},
        ]
        components.html(sala_3d_html(int(time.time()//10), height=360), height=365, scrolling=False)

    with col_tr:
        st.markdown("#### Transformadores de Distribución")
        rng_t = np.random.default_rng(int(time.time()//60))
        for tr_name, tv in EQUIPOS_TRAFO.items():
            t_noise = float(rng_t.uniform(-1, 1))
            t_now   = tv["t_aceite"] + t_noise
            t_color = "#f44336" if t_now > 80 else "#FF9800" if t_now > 70 else "#4CAF50"
            est_c2  = "#4CAF50" if tv["estado"]=="online" else "#FF9800" if tv["estado"]=="standby" else "#607d8b"
            st.markdown(f"""
            <div style="background:#111827;border-radius:10px;padding:12px 16px;margin-bottom:10px;
                 border:1px solid {est_c2}33;">
              <div style="color:white;font-weight:700;">{tr_name}</div>
              <div style="color:#90a4ae;font-size:0.8rem;margin:3px 0;">
                {tv['kv_p']:.0f} kV → {int(tv['kv_s']*1000)} V &nbsp;·&nbsp; {tv['kva']} kVA
              </div>
              <div style="display:flex;gap:1rem;margin-top:6px;">
                <div><span style="color:#90a4ae;font-size:0.75rem;">Carga</span><br>
                     <span style="color:{TEAL_L};font-weight:700;">{tv['carga_pct']}%</span></div>
                <div><span style="color:#90a4ae;font-size:0.75rem;">T° aceite</span><br>
                     <span style="color:{t_color};font-weight:700;">{t_now:.1f}°C</span></div>
                <div><span style="color:#90a4ae;font-size:0.75rem;">Estado</span><br>
                     <span style="color:{est_c2};font-weight:600;">{tv['estado'].upper()}</span></div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Carga de transformadores — gauge
        st.markdown("#### Carga de transformadores")
        fig_tr = go.Figure()
        names_tr = list(EQUIPOS_TRAFO.keys())
        cargas   = [v["carga_pct"] for v in EQUIPOS_TRAFO.values()]
        colors_tr = ["#4CAF50" if c<70 else "#FF9800" if c<90 else "#f44336" for c in cargas]
        fig_tr.add_trace(go.Bar(
            x=[n.split()[0] for n in names_tr], y=cargas,
            marker_color=colors_tr,
            text=[f"{c}%" for c in cargas], textposition="outside",
            textfont=dict(color="white"),
        ))
        fig_tr.add_hline(y=80, line_dash="dash", line_color="#FF9800",
                         annotation_text="Límite recomendado 80%", annotation_font_color="#FF9800")
        fig_tr.update_layout(paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
                             height=230, yaxis=dict(range=[0,105], title="Carga (%)", gridcolor="#1e2d3e"),
                             margin=dict(l=40,r=10,t=10,b=30))
        st.plotly_chart(fig_tr, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: AMBIENTE & SENSORES
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🌡️  Ambiente & Sensores":
    st.markdown("### Monitoreo de Ambiente y Sensores de Seguridad")

    rng_amb = np.random.default_rng(int(time.time()//30))

    # Tarjetas de sensores
    sens_cols = st.columns(3)
    for i, (sala, s) in enumerate(SENSORES_AMB.items()):
        col_s = sens_cols[i % 3]
        if s["temp"] is None:
            status_s = "⚠️ ALARMA" if s["smoke"] or s["water"] else "✓ NORMAL"
            border_c = "#f44336" if s["smoke"] or s["water"] else "#4CAF50"
            body_html = f"""
              <div style="text-align:center;padding:6px 0;">
                <div style="font-size:1.6rem;">{'🔥' if s['smoke'] else '💧' if s['water'] else '✅'}</div>
                <div style="color:{border_c};font-size:1rem;font-weight:700;margin-top:4px;">{status_s}</div>
                <div style="color:#546e7a;font-size:0.72rem;margin-top:2px;">{'Detector humo/agua' if 'Bajo' in sala else 'Detector humo'}</div>
              </div>"""
        else:
            t_now = s["temp"] + float(rng_amb.uniform(-.4,.4))
            h_now = s["hum"]  + float(rng_amb.uniform(-.8,.8))
            t_c   = "#f44336" if t_now >= s["lim_t"] else "#FF9800" if t_now >= s["lim_t"]-2 else "#4CAF50"
            h_c   = "#FF9800" if h_now >= s["lim_h"] else "#4CAF50"
            border_c = "#f44336" if t_now>=s["lim_t"] or h_now>=s["lim_h"] else "#FF9800" if t_now>=s["lim_t"]-2 else "#4CAF50"
            body_html = f"""
              <div style="display:flex;justify-content:space-around;padding:6px 0;">
                <div style="text-align:center;">
                  <div style="font-size:1.4rem;">🌡️</div>
                  <div style="color:{t_c};font-size:1.15rem;font-weight:700;">{t_now:.1f}°C</div>
                  <div style="color:#546e7a;font-size:0.7rem;">Lím {s['lim_t']}°C</div>
                </div>
                <div style="text-align:center;">
                  <div style="font-size:1.4rem;">💧</div>
                  <div style="color:{h_c};font-size:1.15rem;font-weight:700;">{h_now:.0f}%</div>
                  <div style="color:#546e7a;font-size:0.7rem;">Lím {s['lim_h']}%</div>
                </div>
              </div>"""
        col_s.markdown(f"""
        <div style="background:#111827;border-radius:10px;padding:10px 12px;margin-bottom:10px;
             border:1px solid {border_c}44;border-top:3px solid {border_c};">
          <div style="color:white;font-size:0.78rem;font-weight:600;margin-bottom:4px;">📍 {sala}</div>
          {body_html}
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Tendencia de temperatura — últimas 24 h (°C)")
    sals = [s for s, d in SENSORES_AMB.items() if d["temp"] is not None]
    colors_amb = [TEAL_L, TEAL, "#66BB6A", "#FFA726", "#FF7043"]
    t24 = pd.date_range(end=datetime.now(), periods=288, freq="5min")
    fig_amb = go.Figure()
    rng_h = np.random.default_rng(42)
    for j, sala in enumerate(sals):
        s = SENSORES_AMB[sala]
        base_t = s["temp"]
        ts = base_t + np.cumsum(rng_h.normal(0,.06,288))
        ts = np.clip(ts, base_t-2, base_t+3)
        lc = colors_amb[j % len(colors_amb)]
        fig_amb.add_trace(go.Scatter(x=t24, y=ts, mode="lines", name=sala,
                                     line=dict(color=lc, width=1.5)))
        if s.get("lim_t"):
            fig_amb.add_hline(y=s["lim_t"], line_dash="dot", line_color=lc, line_width=.8,
                               opacity=.4)
    fig_amb.update_layout(paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
                          height=280, margin=dict(l=45,r=10,t=10,b=35),
                          xaxis=dict(gridcolor="#1e2d3e"),
                          yaxis=dict(gridcolor="#1e2d3e", title="°C"),
                          legend=dict(bgcolor=CARD2, font=dict(size=10)))
    st.plotly_chart(fig_amb, use_container_width=True)

    st.markdown("#### Tendencia de humedad relativa — últimas 24 h (%)")
    fig_hum = go.Figure()
    rng_h2 = np.random.default_rng(99)
    for j, sala in enumerate(sals):
        s = SENSORES_AMB[sala]
        base_h = s["hum"]
        hs = base_h + np.cumsum(rng_h2.normal(0,.12,288))
        hs = np.clip(hs, base_h-5, base_h+8)
        lc = colors_amb[j % len(colors_amb)]
        fig_hum.add_trace(go.Scatter(x=t24, y=hs, mode="lines", name=sala,
                                      line=dict(color=lc, width=1.5)))
    fig_hum.update_layout(paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
                          height=240, margin=dict(l=45,r=10,t=10,b=35),
                          xaxis=dict(gridcolor="#1e2d3e"),
                          yaxis=dict(gridcolor="#1e2d3e", title="%HR"),
                          legend=dict(bgcolor=CARD2, font=dict(size=10)))
    st.plotly_chart(fig_hum, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: ANÁLISIS ENERGÉTICO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📈  Análisis Energético":
    st.markdown("### Análisis Energético — Consumo y Demanda")

    rng_e = np.random.default_rng(7)
    months = ["Dic'25","Ene'26","Feb'26","Mar'26","Abr'26","May'26"]
    kwh_month = [9420, 9780, 9150, 10320, 9870, 5840]

    c1e,c2e,c3e,c4e = st.columns(4)
    c1e.metric("Consumo mes actual", f"{kwh_month[-1]:,} kWh", f"{kwh_month[-1]-kwh_month[-2]:+,} vs mes ant.")
    c2e.metric("Demanda máx. actual","148.2 kW", "+4.1 kW vs mes ant.")
    c3e.metric("Factor de potencia", "0.924", "+0.012")
    c4e.metric("CO₂ evitado (FV)",   "3.8 t",  "+0.4 t")

    st.markdown("---")
    col_e1, col_e2 = st.columns(2)

    with col_e1:
        st.markdown("#### Consumo mensual (kWh)")
        fig_mon = go.Figure()
        bar_cols = ["#26C6DA" if i < len(months)-1 else TEAL for i in range(len(months))]
        fig_mon.add_trace(go.Bar(
            x=months, y=kwh_month,
            marker_color=bar_cols,
            text=[f"{v:,}" for v in kwh_month],
            textposition="outside",
            textfont=dict(color="white", size=10),
        ))
        fig_mon.update_layout(paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
                              height=280, margin=dict(l=40,r=10,t=10,b=30),
                              yaxis=dict(gridcolor="#1e2d3e", title="kWh"),
                              xaxis=dict(gridcolor="#1e2d3e"))
        st.plotly_chart(fig_mon, use_container_width=True)

    with col_e2:
        st.markdown("#### Distribución por tipo de equipo")
        equip_types = ["UPS (80 kVA)","UPS (40 kVA)","Generadores","Aires A/C","Iluminación","Otros"]
        kwh_equip   = [1420, 820, 680, 1580, 340, 1000]
        fig_pie_e = go.Figure(go.Pie(
            labels=equip_types, values=kwh_equip, hole=0.55,
            marker_colors=[TEAL_L, TEAL, "#66BB6A", "#FFA726", "#AB47BC", "#607d8b"],
            textinfo="label+percent", textfont_size=10,
        ))
        fig_pie_e.update_layout(paper_bgcolor=CARD2, font_color="white",
                                height=280, margin=dict(l=10,r=10,t=10,b=10),
                                showlegend=False,
                                annotations=[dict(text=f"<b>{sum(kwh_equip):,}</b><br>kWh",
                                                  x=.5,y=.5, showarrow=False,
                                                  font=dict(size=13,color="white"))])
        st.plotly_chart(fig_pie_e, use_container_width=True)

    st.markdown("#### Curva de demanda diaria — promedio últimos 30 días (kW)")
    horas = list(range(24))
    base_dem = [45,40,38,36,35,36,42,68,112,135,148,142,
                138,145,150,148,140,132,118,98,82,72,62,52]
    noise_d = rng_e.normal(0, 3, 24)
    dem_hoy = np.array(base_dem, dtype=float) + noise_d
    dem_hoy = np.clip(dem_hoy, 30, 165)
    fig_dem = go.Figure()
    fig_dem.add_trace(go.Scatter(
        x=horas, y=dem_hoy, mode="lines+markers",
        line=dict(color=TEAL_L, width=2.5),
        fill="tozeroy", fillcolor="rgba(38,198,218,0.08)",
        marker=dict(size=5, color=TEAL_L),
        name="Demanda hoy",
    ))
    fig_dem.add_trace(go.Scatter(
        x=horas, y=base_dem, mode="lines",
        line=dict(color="#607d8b", width=1.2, dash="dot"),
        name="Promedio 30d",
    ))
    fig_dem.add_hline(y=150, line_dash="dash", line_color="#f44336",
                      annotation_text="Límite contratado 150 kW",
                      annotation_font_color="#f44336")
    fig_dem.update_layout(
        paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
        height=300, margin=dict(l=45,r=10,t=10,b=35),
        xaxis=dict(title="Hora", tickvals=list(range(0,24,2)),
                   ticktext=[f"{h:02d}:00" for h in range(0,24,2)],
                   gridcolor="#1e2d3e"),
        yaxis=dict(title="kW", gridcolor="#1e2d3e"),
        legend=dict(bgcolor=CARD2),
    )
    st.plotly_chart(fig_dem, use_container_width=True)

    st.markdown("#### Reporte comparativo mensual")
    df_cmp = pd.DataFrame({
        "Mes":     months,
        "kWh":     kwh_month,
        "kW Máx":  [132,138,128,145,142,148],
        "FP":      [0.91,0.912,0.908,0.918,0.921,0.924],
        "CO₂ (t)": [4.2,4.4,4.1,4.6,4.4,2.6],
        "$/kWh":   [0.098,0.101,0.097,0.103,0.099,0.102],
    })
    df_cmp["Costo ($)"] = (df_cmp["kWh"] * df_cmp["$/kWh"]).round(2)
    st.dataframe(df_cmp, hide_index=True, use_container_width=True)
    buf_e = io.StringIO()
    df_cmp.to_csv(buf_e, index=False)
    st.download_button("⬇️ Exportar CSV", buf_e.getvalue(),
                       file_name=f"energia_{datetime.now().strftime('%Y%m')}.csv", mime="text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA: SOLAR FV
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🔲  Diagrama Unifilar":
    st.markdown("### Diagrama Unifilar — Subestación 15 kV")
    st.caption("Valores en tiempo real · interruptores · TC · estados de celda")
    tick_u = int(time.time() // 8)
    components.html(unifilar_html(tick_u), height=650, scrolling=False)

elif pagina == "☀️  Solar FV":
    st.markdown("### Monitoreo Solar Fotovoltaico — Sistema FV 130 kWp")

    total_p  = sum(v["p_kw"]  for v in EQUIPOS_SOLAR.values())
    total_ed = sum(v["e_dia"] for v in EQUIPOS_SOLAR.values())
    total_em = sum(v["e_mes"] for v in EQUIPOS_SOLAR.values())
    invs_on  = sum(1 for v in EQUIPOS_SOLAR.values() if v["estado"]=="online")

    c1s,c2s,c3s,c4s = st.columns(4)
    c1s.metric("Potencia actual",    f"{total_p:.1f} kW",   f"de 130 kWp")
    c2s.metric("Energía hoy",        f"{total_ed:.0f} kWh", "+12% vs ayer")
    c3s.metric("Energía este mes",   f"{total_em:,.0f} kWh")
    c4s.metric("Inversores online",  f"{invs_on}/{len(EQUIPOS_SOLAR)}")

    st.markdown("---")
    col_s1, col_s2 = st.columns([1.3, 1])

    with col_s1:
        st.markdown("#### Curva de generación diaria (kW)")
        horas_s = list(range(6, 19))
        gen_curve = [0.2,2.8,12.5,28.4,40.2,52.8,62.1,72.4,68.3,58.9,44.2,26.7,8.3]
        rng_s = np.random.default_rng(int(time.time()//600))
        now_h = datetime.now().hour
        gen_now = [v + float(rng_s.uniform(-.8,.8)) for v in gen_curve]
        gen_now = [v if h <= now_h else None for h, v in zip(horas_s, gen_now)]
        gen_pred = gen_curve[:]
        hora_labels = [f"{h:02d}:00" for h in horas_s]
        fig_fv = go.Figure()
        fig_fv.add_trace(go.Scatter(
            x=hora_labels, y=gen_now, mode="lines+markers",
            line=dict(color="#FDD835", width=2.5),
            fill="tozeroy", fillcolor="rgba(253,216,53,0.1)",
            marker=dict(size=5, color="#FDD835"), name="Generación real",
        ))
        fig_fv.add_trace(go.Scatter(
            x=hora_labels, y=gen_pred, mode="lines",
            line=dict(color="#607d8b", width=1.2, dash="dot"), name="Pronóstico",
        ))
        fig_fv.update_layout(paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
                             height=290, margin=dict(l=45,r=10,t=10,b=30),
                             xaxis=dict(gridcolor="#1e2d3e"),
                             yaxis=dict(title="kW", gridcolor="#1e2d3e"),
                             legend=dict(bgcolor=CARD2))
        st.plotly_chart(fig_fv, use_container_width=True)

        st.markdown("#### Generación mensual — últimos 6 meses (kWh)")
        meses_s = ["Dic'25","Ene'26","Feb'26","Mar'26","Abr'26","May'26"]
        gen_mes  = [12840,11520,13180,14250,13820,6180]
        fig_gm = go.Figure(go.Bar(
            x=meses_s, y=gen_mes,
            marker_color=["#FDD835" if i==len(meses_s)-1 else "#F9A825" for i in range(len(meses_s))],
            text=[f"{v:,}" for v in gen_mes], textposition="outside",
            textfont=dict(color="white",size=10),
        ))
        fig_gm.update_layout(paper_bgcolor=CARD2, plot_bgcolor=CARD2, font_color="white",
                             height=240, margin=dict(l=40,r=10,t=10,b=30),
                             yaxis=dict(gridcolor="#1e2d3e",title="kWh"))
        st.plotly_chart(fig_gm, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Diagrama de Strings — Conexión FV → Inversores → Red")
    components.html(pv_string_html(), height=565, scrolling=False)

    st.markdown("---")
    with col_s2:
        st.markdown("#### Estado de inversores")
        for inv_name, iv in EQUIPOS_SOLAR.items():
            est_c = TEAL_L if iv["estado"]=="online" else "#607d8b"
            pr_c  = "#4CAF50" if iv["pr"]>75 else "#FF9800" if iv["pr"]>60 else "#f44336"
            st.markdown(f"""
            <div style="background:#111827;border-radius:10px;padding:12px 14px;margin-bottom:10px;
                 border-left:4px solid {est_c};">
              <div style="color:white;font-weight:700;">{inv_name}</div>
              <div style="display:flex;gap:1rem;margin-top:6px;flex-wrap:wrap;">
                <div><span style="color:#90a4ae;font-size:0.72rem;">Potencia</span><br>
                     <span style="color:{TEAL_L};font-size:1rem;font-weight:700;">{iv['p_kw']:.1f} kW</span>
                     <span style="color:#546e7a;font-size:0.7rem;">/{iv['p_max']} kW</span></div>
                <div><span style="color:#90a4ae;font-size:0.72rem;">E. hoy</span><br>
                     <span style="color:white;font-weight:600;">{iv['e_dia']:.1f} kWh</span></div>
                <div><span style="color:#90a4ae;font-size:0.72rem;">PR</span><br>
                     <span style="color:{pr_c};font-weight:700;">{iv['pr']:.1f}%</span></div>
                <div><span style="color:#90a4ae;font-size:0.72rem;">Estado</span><br>
                     <span style="color:{est_c};font-weight:600;">{iv['estado'].upper()}</span></div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Baterías de respaldo
        st.markdown("#### Bancos de baterías")
        for bat_name, bv in BATERIAS.items():
            soc_c = "#4CAF50" if bv["soc"]>50 else "#FF9800" if bv["soc"]>20 else "#f44336"
            soh_c = "#4CAF50" if bv["soh"]>85 else "#FF9800" if bv["soh"]>70 else "#f44336"
            est_c = TEAL_L if bv["estado"]=="cargando" else "#607d8b"
            st.markdown(f"""
            <div style="background:#111827;border-radius:10px;padding:10px 14px;margin-bottom:8px;
                 border-left:4px solid {soc_c};">
              <div style="color:white;font-size:0.85rem;font-weight:700;">{bat_name}</div>
              <div style="background:#0d1520;border-radius:4px;height:8px;margin:6px 0;overflow:hidden;">
                <div style="background:{soc_c};width:{bv['soc']}%;height:100%;border-radius:4px;"></div>
              </div>
              <div style="display:flex;gap:1rem;font-size:0.75rem;">
                <span style="color:{soc_c};">SOC <b>{bv['soc']}%</b></span>
                <span style="color:{soh_c};">SOH <b>{bv['soh']}%</b></span>
                <span style="color:#90a4ae;">{bv['v']:.1f} V &nbsp; {bv['i']:+.1f} A</span>
                <span style="color:{est_c};">{bv['estado'].upper()}</span>
              </div>
            </div>""", unsafe_allow_html=True)
