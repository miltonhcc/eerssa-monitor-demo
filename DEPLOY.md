# Despliegue en Streamlit Community Cloud (gratis)

## Paso 1 — Subir a GitHub

1. Crear cuenta en https://github.com (si no tienen)
2. Crear repositorio nuevo: `eerssa-monitor-demo` (público o privado)
3. Subir los 2 archivos: `app.py` y `requirements.txt`

## Paso 2 — Desplegar en Streamlit Cloud

1. Ir a https://share.streamlit.io
2. Iniciar sesión con la cuenta de GitHub
3. Click **"New app"**
4. Seleccionar el repositorio `eerssa-monitor-demo`
5. Main file path: `app.py`
6. Click **Deploy**

## Resultado

En ~2 minutos obtendrán una URL pública:

```
https://eerssa-monitor-demo.streamlit.app
```

Esta URL es la que se adjunta a la oferta junto con:
- Usuario/contraseña: no requerido (app pública)
- El link ya cumple el requisito de "link y demo de plataforma"

## Probar localmente (opcional)

```bash
pip install streamlit plotly pandas numpy
streamlit run app.py
```
