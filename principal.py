import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# Leer API key desde secretos
API_KEY = 'F5F8E718-78E6-40F1-9E32-9E0AF21C17F3' # Esto se configura en Streamlit Cloud
# Fechas
fecha_inicio = (datetime.now() - timedelta(days=7)).strftime("%d-%m-%Y")
fecha_fin = datetime.now().strftime("%d-%m-%Y")

st.title("📋 Licitaciones últimos 75días")

st.write(f"Licitaciones publicadas entre **{fecha_inicio}** y **{fecha_fin}**")

# Estado de la sesión para manejar licitación seleccionada
if "detalle" not in st.session_state:
    st.session_state.detalle = None

if st.button("🔍 Buscar licitaciones"):
    url = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
    params = {
        "ticket": API_KEY,
        "pagina": 1
    }

    with st.spinner("🔄 Cargando licitaciones..."):
        response = requests.get(url, params=params)
        data = response.json()
        listado = data.get("Listado", [])

    if not listado:
        st.warning("No se encontraron licitaciones.")
    else:
        df = pd.DataFrame(listado)
        st.success(f"{len(df)} licitaciones encontradas.")

        for i, row in df.iterrows():
            with st.expander(f"{row['CodigoExterno']} — {row['Nombre']}"):
                st.write(f"🕓 **Cierre**: {row['FechaCierre']}")
                st.write(f"💰 **Monto estimado**: {row.get('MontoEstimado', 'No informado')}")

                # Leer detalle automáticamente al expandir
                with st.spinner("📡 Consultando detalle..."):
                    time.sleep(0.5)  # Simula carga

                    detalle_url = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
                    r = requests.get(detalle_url, params={"ticket": API_KEY, "codigo": row["CodigoExterno"]})
                    detalle = r.json()

                    if detalle.get("Listado"):
                        lic = detalle["Listado"][0]
                        st.markdown("### 📄 Resumen de Licitación")
                        for clave, valor in lic.items():
                            # Si el valor es un diccionario (como 'Comprador'), lo desplegamos también
                            if isinstance(valor, dict):
                                st.markdown(f"**🔹 {clave}**:")
                                for subclave, subvalor in valor.items():
                                    st.write(f" • {subclave}: {subvalor}")
                            else:
                                st.write(f"**{clave}**: {valor}")
                    else:
                        st.error("No se pudo obtener el detalle.")