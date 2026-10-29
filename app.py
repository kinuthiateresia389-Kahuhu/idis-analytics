import streamlit as st
import pandas as pd
import numpy as np

# Hardening the spatiotemporal architecture against runtime exceptions
st.set_page_config(page_title="IDIS Premium Platform", page_icon="📡", layout="wide")

# Simple, secure authentication state management
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Layout header
st.title("Sovereign Disaster Informatics System (IDIS)")

# --- ACCESS MANAGEMENT SUB-LAYER (THE PAYWALL GATE) ---
if not st.session_state.authenticated:
    st.warning("🔒 SYSTEM SECURITY LOCK: Secure Enterprise Session Awaiting Activation.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.header("Corporate Access Login")
        user = st.text_input("Username / Client ID")
        password = st.text_input("Security Access Code", type="password")
        if st.button("Unlock Mission Command Node"):
            if user == "enterprise_client" and password == "MasenoIDIS2026!":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Telemetry Credentials. Access Revoked.")
                
    with col_b:
        st.header("Procure Platform Subscription")
        st.write("Unlock unlimited global Web-GIS telemetry mapping, multi-column analytics, and localized climate crisis alerts.")
        st.info("💳 Enterprise Tier Access: $999 USD / Month")
        
        # Simulated secure transaction endpoint loop
        if st.button("💳 Purchase Corporate Token (Initialize Stripe Gateway)"):
            st.success("Redirecting safely to secure checkout server... Use Test Account to activate.")
            st.session_state.authenticated = True
            st.rerun()

# --- ENTERPRISE INTERACTIVE WORKSPACE (LOCKED BEHIND THE CREDIT CARD GATE) ---
else:
    st.write("Operator Node: Teresia Wangui Kinuthia | **PREMIUM ACTIVE NODE** ✅")
    if st.sidebar.button("Log Out of Session"):
        st.session_state.authenticated = False
        st.rerun()

    # Split-view system interface layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Enterprise Intelligence Controls")
        upload_file = st.file_uploader("Ingiza Telemetry Dataset (CSV)", type=["csv"])
        lat_base = -0.0051
        lon_base = 34.6036

    with col2:
        st.header("Real-Time Spatiotemporal Map Viewer")
        if upload_file is not None:
            data = pd.read_csv(upload_file)
            st.success("=== TELEMETRY INGESTION SUCCESSFUL ===")
            st.dataframe(data.head(10))
            
            data.columns = data.columns.str.strip().str.lower()
            if 'latitude' in data.columns and 'longitude' in data.columns:
                st.info("Dynamic System Override: Re-centering Map to Active Ingestion Data Assets...")
                spatial_data = data.dropna(subset=['latitude', 'longitude'])
                st.map(spatial_data)
            else:
                st.error("Telemetry Error: Missing 'latitude' or 'longitude' coordinate columns in dataset.")
        else:
            st.info("Standby Mode: Displaying Base Operational Grid...")
            map_data = pd.DataFrame({'lat': [lat_base], 'lon': [lon_base]})
            st.map(map_data, zoom=14)
