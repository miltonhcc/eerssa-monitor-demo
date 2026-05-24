# LUXPOWER METRICS Platform

Sistema de monitoreo remoto IoT para infraestructura eléctrica crítica. Supervisión en tiempo real de UPS, generadores ELETRIOS, aires de precisión CRAC/CRAH, sistema contraincendios, media tensión, energía fotovoltaica y ambiente. Diseñado bajo criterios de alta disponibilidad, redundancia y continuidad operativa asociados a un nivel Tier IV.

---

## Acceso

| Entorno | URL |
|---|---|
| Demo en la nube | https://eerssa-monitor-demo.streamlit.app |
| Local | http://localhost:8502 |

**Credenciales de prueba:**

| Usuario | Clave | Rol |
|---|---|---|
| `DEMO` | `1234` | Operador |
| `EERSSA` | `monitor2026` | Administrador |
| `COMITE` | `eval2026` | Auditor |

---

## Módulos del sistema

| Página | Descripción |
|---|---|
| Inicio | KPIs globales, estado general, consumo energético |
| Sala 3D · Equipos | Vista 3D interactiva Three.js de toda la sala de equipos |
| Diagrama Unifilar | Diagrama SVG animado subestación 15 kV en tiempo real |
| Monitoreo UPS | Voltaje, corriente, batería, temperatura, autonomía |
| Monitoreo Generadores | Voltaje, RPM, T° aceite, combustible, horas operación |
| Monitoreo A/C | Temperatura, humedad, compresor, refrigerante |
| Media Tensión 3D | Celdas KYN28, transformadores de distribución, vista 3D |
| Ambiente & Sensores | Temperatura/humedad por sala, detectores humo/agua |
| Análisis Energético | Consumo mensual, demanda, factor de potencia, CO₂ |
| Solar FV | Inversores GoodWe, strings, curva de generación, baterías |
| **Generadores ELETRIOS** | Monitoreo específico unidades ELETRIOS ETG-500/250 |
| **Aires de Precisión** | Monitoreo CRAC Vertiv Liebert DS + CRAH APC InRow |
| **Contraincendios** | Sistema FM-200, zonas, cilindros, presión, pruebas |
| Gestión de Alarmas | Alarmas activas, historial, filtros, exportación CSV |
| Reporte de Parámetros | Historial configurable, heatmap, exportación |
| Trazabilidad Incidentes | Línea de tiempo, causa raíz, tiempo de resolución |
| Arquitectura del Sistema | Diagrama de comunicaciones IoT, ventajas del sistema |

---

## Estructura de archivos

```
DEMO_MONITOREO/
├── app.py                        ← Aplicación principal Streamlit
├── requirements.txt              ← Dependencias Python
├── .gitignore
├── README.md
└── assets/
    ├── images/
    │   └── 3d/
    │       ├── datacenter/       ← Imagen render sala general Data Center
    │       ├── ups/              ← Sala UPS y baterías
    │       ├── batteries/        ← Bancos de baterías de respaldo
    │       ├── generators/       ← Sala generadores ELETRIOS
    │       ├── cooling/          ← Aires de precisión CRAC/CRAH
    │       ├── fire_suppression/ ← Sistema contraincendios FM-200
    │       ├── electrical/       ← Sala eléctrica MV/BT
    │       ├── monitoring/       ← Centro de control NOC
    │       └── dashboards/       ← Capturas de dashboard
    └── prompts/
        └── image_generation/     ← Prompts para generar imágenes 3D con IA
            ├── prompt_datacenter_general_3d.txt
            ├── prompt_ups_battery_room_3d.txt
            ├── prompt_generator_room_3d.txt
            ├── prompt_precision_cooling_3d.txt
            ├── prompt_fire_suppression_3d.txt
            ├── prompt_electrical_distribution_3d.txt
            └── prompt_monitoring_dashboard_3d.txt
```

---

## Agregar imágenes 3D

Las carpetas `assets/images/3d/` están preparadas para recibir imágenes render de cada subsistema.

1. Usar los prompts en `assets/prompts/image_generation/` con Midjourney, DALL-E 3 o Stable Diffusion XL
2. Guardar cada imagen en la subcarpeta correspondiente con nombre descriptivo
3. La aplicación puede mostrarlas via `st.image()` en la página de cada módulo

---

## Despliegue en Streamlit Community Cloud (gratuito)

### Paso 1 — Subir a GitHub

1. Crear repositorio `eerssa-monitor-demo` (público)
2. Subir los archivos: `app.py`, `requirements.txt`, `.gitignore`, `README.md`
3. Subir la carpeta `assets/` completa (con los `.gitkeep` para mantener estructura)

### Paso 2 — Desplegar

1. Ir a https://share.streamlit.io
2. Iniciar sesión con la cuenta de GitHub
3. Click **New app** → seleccionar repositorio → Main file: `app.py`
4. Click **Deploy** — URL disponible en ~2 minutos

---

## Ejecutar localmente

```bash
pip install streamlit plotly pandas numpy
streamlit run app.py --server.port 8502
```

---

## Tecnologías

- **Streamlit** ≥ 1.33 — framework de aplicación web
- **Three.js r134** — visualización 3D interactiva de salas de equipos
- **Plotly** ≥ 5.18 — gráficas interactivas, gauges, heatmaps
- **SVG dinámico** — diagrama unifilar y diagrama de strings FV en tiempo real
- **Python 3.11+** — backend de simulación de datos y lógica de negocio

---

## Infraestructura representada

El sistema monitorea una infraestructura diseñada bajo criterios de alta disponibilidad,
redundancia y continuidad operativa asociados a un nivel Tier IV:

- **Alimentación**: 2N — doble alimentación 15 kV redundante
- **Generadores**: N+1 — 3 grupos electrógenos ELETRIOS (2×500 kVA + 1×250 kVA)
- **UPS**: N+1 — UPS-01 80 kVA + UPS-02 40 kVA con baterías independientes
- **Enfriamiento**: N+1 — 2 CRAC Vertiv Liebert DS + 2 CRAH APC InRow
- **Contraincendios**: FM-200 (HFC-227ea) por zonas independientes
- **Conectividad**: Dual-path GSM 4G/3G redundante para telemetría IoT

---

*LUXPOWER METRICS Platform — NOC 24/7 — Monitoreo IoT de Infraestructura Crítica*
