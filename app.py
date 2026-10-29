import streamlit as st
import pandas as pd
import numpy as np

# Hardening the spatiotemporal architecture against runtime thread-boundary exceptions under load
st.set_page_config(page_title="IDIS Sovereign Platform", page_icon="📡", layout="wide")

st.title("Sovereign Disaster Informatics System (IDIS)")
st.write("Operator Node: Teresia Wangui Kinuthia | Systems Architecture Framework")

# Engineering a split-view system interface layout
col1, col2 = st.columns(2)

with col1:
    st.header("Enterprise Intelligence Controls")
    upload_file = st.file_uploader("Ingiza Telemetry Dataset (CSV)", type=["csv"])
    
    # Core anchoring coordinates (Maseno University Technical Cockpit Core)
    lat_base = -0.0051
    lon_base = 34.6036

with col2:
    st.header("Real-Time Spatiotemporal Map Viewer")
    
    if upload_file is not None:
        data = pd.read_csv(upload_file)
        st.success("=== TELEMETRY INGESTION SUCCESSFUL ===")
        st.dataframe(data.head(10))
        
        # Standardizing column headers to handle capitalization variations automatically
        data.columns = data.columns.str.strip().str.lower()
        
        # Dynamic Mapping Machinery: Extract and plot data dynamically if spatial logs exist
        if 'latitude' in data.columns and 'longitude' in data.columns:
            st.info("Dynamic System Override: Re-centering Map to Active Ingestion Data Assets...")
            # Drops rows missing coordinate values to protect from thread breaks
            spatial_data = data.dropna(subset=['latitude', 'longitude'])
            st.map(spatial_data)
        else:
            st.error("Telemetry Error: Missing 'latitude' or 'longitude' coordinate columns in dataset.")
    else:
        st.info("Standby Mode: Displaying Base Operational Grid...")
        # Compiling a baseline spatial array pointing directly to your room coordinate matrix hapo Maseno
        map_data = pd.DataFrame({'lat': [lat_base], 'lon': [lon_base]})
        st.map(map_data, zoom=14)
