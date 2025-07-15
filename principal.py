import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Leer API key desde secretos
API_KEY = 'F5F8E718-78E6-40F1-9E32-9E0AF21C17F3' # Esto se configura en Streamlit Cloud

# Fechas: últimos 7 días
fecha_inicio = (datetime.now() - timedelta(days=7)).strftime("%d-%m-%Y")
fecha_fin = datetime.now().strftime("%d-%m-%Y")

# UI Streamlit
st.title("🗂️ Licitaciones - Últimos 7 días")
st.write(f"Buscando licitaciones desde **{fecha_inicio}** hasta **{fecha_fin}**")

# Botón para consultar
if st.button("🔍 Buscar licitaciones"):
    url = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
    params = {
        "ticket": API_KEY,
        "estado": "publicada",
        "pagina": 1
    }

    response = requests.get(url, params=params)
    data = response.json()
    listado = data.get("Listado", [])

    if not listado:
        st.warning("No se encontraron licitaciones en el rango de fechas.")
    else:
        df = pd.DataFrame(listado)

        # Mostrar columnas disponibles
        st.subheader(f"🔢 {len(df)} licitaciones encontradas")
        st.markdown("### 🧾 Columnas disponibles en el resultado:")
        st.code(df.columns.tolist(), language="python")

        # Mostrar tabla completa
        st.markdown("### 📋 Resultado completo:")
        st.dataframe(df)

        # Descargar CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar como CSV", csv, file_name="licitaciones.csv")