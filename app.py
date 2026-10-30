import streamlit as st
import pandas as pd
import json
import urllib.request
from datetime import datetime

st.set_page_config(page_title="IDIS Premium Platform", page_icon="📡", layout="wide")

# Safe validation checks for secure cloud database connections
if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
    st.error("🔒 Infrastructure Error: Missing secure Cloud Database Secrets connection tokens.")
    st.stop()

URL = st.secrets["SUPABASE_URL"].strip("/")
API_KEY = st.secrets["SUPABASE_KEY"]

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_node' not in st.session_state:
    st.session_state.user_node = None

def verify_cloud_login(username, password):
    """Secure direct web API database lookup for customer security verification"""
    try:
        endpoint = f"{URL}/rest/v1/clients?username=eq.{urllib.parse.quote(username)}&select=*"
        req = urllib.request.Request(endpoint)
        req.add_header("apikey", API_KEY)
        req.add_header("Authorization", f"Bearer {API_KEY}")
        
        with urllib.request.urlopen(req, timeout=5) as response:
            records = json.loads(response.read().decode('utf-8'))
            if not records:
                return False, "Telemetry ID not found in database registry."
            client_data = records[0] if isinstance(records, list) else records
            if client_data.get("password") != password:
                return False, "Invalid Telemetry Credentials. Access Revoked."
            
            # Automated 30-Day Subscription Countdown Clock Verification
            expiry_str = client_data.get("expiry_date")
            if expiry_str:
                if datetime.now().date() > datetime.strptime(expiry_str, "%Y-%m-%d").date():
                    return False, f"🔴 Access Terminated: Subscription expired on {expiry_str}. Please clear invoice."
            return True, client_data.get("company_name", "Authorized Corporate Node")
    except Exception:
        return False, "Database Node communication delay. Please try again."

st.title("Sovereign Disaster Informatics System (IDIS)")

# --- ACCESS MANAGEMENT LAYER (SECURE HARDENED GATE) ---
if not st.session_state.authenticated:
    st.warning("🔒 SYSTEM SECURITY LOCK: Secure Enterprise Session Awaiting Activation.")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.header("Corporate Access Login")
        user = st.text_input("Username / Client ID")
        pwd = st.text_input("Security Access Code", type="password")
        if st.button("Unlock Mission Command Node"):
            if user and pwd:
                success, response_msg = verify_cloud_login(user, pwd)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_node = response_msg
                    st.rerun()
                else:
                    st.error(response_msg)
            else:
                st.info("Please fill in all security credential nodes.")
                
    with col_b:
        st.header("Procure Platform Subscription")
        st.write("Unlock unlimited global Web-GIS telemetry mapping, multi-column analytics, and localized climate crisis alerts.")
        st.info("💳 Enterprise Tier Access: $1,000 USD / Month")
        st.caption("ℹ️ *International accounts are processed securely via local conversion nodes as KES 130,000.*")
        
        REAL_PAYSTACK_LINK = "https://paystack.shop/pay/25lh3e-hx5"
        st.write("To initialize secure international credit card or M-Pesa clearance, route through our global financial merchant node below:")
        st.markdown(f"[💳 Proceed to Secure Gateway Checkout]({REAL_PAYSTACK_LINK})")

# --- ENTERPRISE INTERACTIVE WORKSPACE (LOCKED BEHIND VALID SUBSCRIPTION) ---
else:
    st.write(f"Authorized Node: **{st.session_state.user_node}** | Session Status: **PREMIUM SECURE LIFELINE ACTIVE** ✅")
    if st.sidebar.button("Log Out of Session"):
        st.session_state.authenticated = False
        st.session_state.user_node = None
        st.rerun()

    st.sidebar.header("Client Onboarding Suite")
    st.sidebar.write("Download our standard multi-county trial telemetry template to test system integration responsiveness:")
    
    demo_df = pd.DataFrame({
        'latitude': [-1.2921, -1.3005, -4.0435, -0.0051],
        'longitude': [36.8219, 36.7995, 39.6682, 34.6036],
        'incident_type': ['Severe Flash Flooding', 'Landslide / Grid Failure', 'Coastal Surge', 'Drainage Overflow'],
        'severity': ['Critical', 'Severe', 'Critical', 'Moderate']
    })
    st.sidebar.download_button(
        label="📥 Download Sample Telemetry CSV",
        data=demo_df.to_csv(index=False).encode('utf-8'),
        file_name="idis_premium_demo_template.csv",
        mime="text/csv"
    )

    # Split-view platform interface layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Enterprise Intelligence Controls")
        upload_file = st.file_uploader("Ingiza Telemetry Dataset (CSV)", type=["csv"])
        
        # --- GLOBAL DATA RE-MAPPING SUITE ---
        lat_column = "latitude"
        lon_column = "longitude"
        
        if upload_file is not None:
            # Smart peek at the incoming file structure to harvest the raw column list
            file_peek = pd.read_csv(upload_file, nrows=2)
            all_columns = list(file_peek.columns)
            
            st.markdown("### 🛠️ Smart Column Remapping Interface")
            st.info("Our parsing engine automatically detected the following spreadsheet headers. Select the columns that hold your geographic coordinates:")
            
            # Try to guess smart defaults to save the corporate user time
            def_lat_idx = 0
            def_lon_idx = 1 if len(all_columns) > 1 else 0
            
            for i, col in enumerate(all_columns):
                cleaned_name = str(col).strip().lower()
                if cleaned_name in ['lat', 'latitude', 'gps_lat', 'y', 'y_coord']:
                    def_lat_idx = i
                if cleaned_name in ['lon', 'longitude', 'long', 'gps_lon', 'x', 'x_coord']:
                    def_lon_idx = i

            lat_column = st.selectbox("Select Latitude Column:", options=all_columns, index=def_lat_idx)
            lon_column = st.selectbox("Select Longitude Column:", options=all_columns, index=def_lon_idx)

    with col2:
        st.header("Real-Time Spatiotemporal Map Viewer")
        if upload_file is not None:
	    upload_file.seek(0)
            data = pd.read_csv(upload_file)
            st.success("=== TELEMETRY INGESTION SUCCESSFUL ===")
            st.dataframe(data.head(10))
            
            # Verify user mapping choices exist and execute defense filters against missing metrics
            if lat_column in data.columns and lon_column in data.columns:
                st.info(f"Dynamic System Override: Mapping coordinates using custom columns: [{lat_column}] and [{lon_column}]...")
                
                # Standardize mapping names for internal Streamlit map rendering engine configurations
                mapping_df = data[[lat_column, lon_column]].copy()
                mapping_df.columns = ['latitude', 'longitude']
                
                # Drop rows with corrupted or blank cell coordinates to avoid runtime crashing exceptions
                clean_spatial_data = mapping_df.dropna(subset=['latitude', 'longitude'])
                st.map(clean_spatial_data)
            else:
                st.error("Mapping Refused: Selected remapping column nodes do not exist in dataset memory.")
        else:
            st.info("Standby Mode: Displaying Base Operational Grid...")
            st.map(pd.DataFrame({'lat': [-0.0051], 'lon': [34.6036]}), zoom=14)
