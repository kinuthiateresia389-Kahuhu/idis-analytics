import streamlit as st
import pandas as pd
import numpy as np

# Hardening the spatiotemporal architecture against runtime exceptions under load
st.set_page_config(page_title="IDIS Premium Platform", page_icon="📡", layout="wide")

# Simple, secure authentication state management
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

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
        st.info("💳 Enterprise Tier Access: KES 130,000 / Month")
        
        # PRODUCTION TRANSACTING EDGE (Live Paystack Link Integrated!)
        REAL_PAYSTACK_LINK = "https://paystack.shop/pay/25lh3e-hx5"
        
        st.write("To initialize secure international credit card or M-Pesa clearance, route through our global financial merchant node below:")
        st.markdown(f"[💳 Proceed to Secure Gateway Checkout]({REAL_PAYSTACK_LINK})")
        
        st.markdown("---")
        # Developer back-channel bypass button for local demonstration
        if st.button("🔌 Developer Simulation Bypass (For Client Pitch Demos)"):
            st.session_state.authenticated = True
            st.rerun()

# --- ENTERPRISE INTERACTIVE WORKSPACE (LOCKED BEHIND THE CREDIT CARD GATE) ---
else:
    st.write("Operator Node: Teresia Wangui Kinuthia | **PREMIUM ACTIVE NODE** ✅")
    if st.sidebar.button("Log Out of Session"):
        st.session_state.authenticated = False
        st.rerun()

    # --- CLIENT ONBOARDING TOOLS (The Sample Downloader) ---
    st.sidebar.header("Client Onboarding Suite")
    st.sidebar.write("Download our standard multi-county trial telemetry template to test system integration responsiveness:")
    
    # Compiling the local demo data stream straight into browser memory
    demo_df = pd.DataFrame({
        'latitude': [-1.2921, -1.3005, -4.0435, -0.0051],
        'longitude': [36.8219, 36.7995, 39.6682, 34.6036],
        'incident_type': ['Severe Flash Flooding', 'Landslide / Grid Failure', 'Coastal Surge', 'Drainage Overflow'],
        'severity': ['Critical', 'Severe', 'Critical', 'Moderate'],
        'impact_est_usd': [450000, 210000, 850000, 350000]
    })
    csv_data = demo_df.to_csv(index=False).encode('utf-8')
    
    st.sidebar.download_button(
        label="📥 Download Sample Telemetry CSV",
        data=csv_data,
        file_name="idis_premium_demo_template.csv",
        mime="text/csv"
    )

    # Split-view system interface layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Enterprise Intelligence Controls")
        upload_file = st.file_uploader("Ingiza Telemetry Dataset (CSV)", type=["csv"])

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
            st.map(pd.DataFrame({'lat': [-0.0051], 'lon': [34.6036]}), zoom=14)
