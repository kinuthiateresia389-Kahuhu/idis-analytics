import streamlit as st
import pandas as pd
import json
import urllib.request
from datetime import datetime

st.set_page_config(page_title="IDIS Premium Platform", page_icon="📡", layout="wide")

# Safe validation checks for secure database connections
if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
    st.error("🔒 Infrastructure Error: Missing secure Cloud Database Secrets connection tokens.")
    st.stop()

URL = st.secrets["SUPABASE_URL"].strip("/")
API_KEY = st.secrets["SUPABASE_KEY"]

# Initialize robust core authentication states
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_node' not in st.session_state:
    st.session_state.user_node = None

def verify_cloud_login(username, password):
    """Secure direct web API database lookup for traditional credentials"""
    try:
        endpoint = f"{URL}/rest/v1/clients?username=eq.{urllib.parse.quote(username)}&select=*"
        req = urllib.request.Request(endpoint)
        req.add_header("apikey", API_KEY)
        req.add_header("Authorization", f"Bearer {API_KEY}")
        
        with urllib.request.urlopen(req, timeout=5) as response:
            records = json.loads(response.read().decode('utf-8'))
            if not records:
                return False, "Telemetry ID not found in database registry."
            client_data = records[0]
            if client_data.get("password") != password:
                return False, "Invalid Telemetry Credentials. Access Revoked."
            
            # Subscription Expiration Clock Check
            expiry_str = client_data.get("expiry_date")
            if expiry_str:
                if datetime.now().date() > datetime.strptime(expiry_str, "%Y-%m-%d").date():
                    return False, f"🔴 Access Terminated: Subscription expired on {expiry_str}."
            return True, client_data.get("company_name", "Authorized Node")
    except Exception:
        return False, "Database Node communication delay."

def verify_magic_token(token_string):
    """Premium Passwordless Token Authenticator via URL Query parameters"""
    try:
        # Pinging database to find a matching token code in your data rows
        endpoint = f"{URL}/rest/v1/clients?username=eq.{urllib.parse.quote(token_string)}&select=*"
        req = urllib.request.Request(endpoint)
        req.add_header("apikey", API_KEY)
        req.add_header("Authorization", f"Bearer {API_KEY}")
        
        with urllib.request.urlopen(req, timeout=5) as response:
            records = json.loads(response.read().decode('utf-8'))
            if records:
                client_data = records[0]
                expiry_str = client_data.get("expiry_date")
                if expiry_str and datetime.now().date() > datetime.strptime(expiry_str, "%Y-%m-%d").date():
                    return False
                return client_data.get("company_name", "Premium Enterprise Token Node")
            return None
    except Exception:
        return None

# --- AUTOMATED PASSWORDS-BYPASS DETECTOR ENGINE ---
query_params = st.query_params
if "token" in query_params and not st.session_state.authenticated:
    provided_token = query_params["token"]
    verified_company = verify_magic_token(provided_token)
    if verified_company:
        st.session_state.authenticated = True
        st.session_state.user_node = verified_company
        st.rerun()

st.title("Sovereign Disaster Informatics System (IDIS)")

# --- ACCESS MANAGEMENT LAYER (SECURE STOREFRONT GATE) ---
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
        
        REAL_PAYSTACK_LINK = "https://paystack.shop"
        st.markdown(f"[💳 Proceed to Secure Gateway Checkout]({REAL_PAYSTACK_LINK})")

# --- ENTERPRISE INTERACTIVE WORKSPACE (FULLY UNLOCKED) ---
else:
    st.write(f"Authorized Node: **{st.session_state.user_node}** | Session Status: **PREMIUM SECURE LIFELINE ACTIVE** ✅")
    if st.sidebar.button("Log Out of Session"):
        st.session_state.authenticated = False
        st.session_state.user_node = None
        st.query_params.clear() # Clear URL token string on log out
        st.rerun()

    st.sidebar.header("Client Onboarding Suite")
    demo_df = pd.DataFrame({
        'latitude': [-1.2921, -1.3005, -4.0435, -0.0051],
        'longitude': [36.8219, 36.7995, 39.6682, 34.6036],
        'incident_type': ['Severe Flash Flooding', 'Landslide / Grid Failure', 'Coastal Surge', 'Drainage Overflow'],
        'severity': ['Critical', 'Severe', 'Critical', 'Moderate'],
        'impact_est_usd': [450000, 210000, 850000, 350000]
    })
    st.sidebar.download_button(
        label="📥 Download Sample Telemetry CSV",
        data=demo_df.to_csv(index=False).encode('utf-8'),
        file_name="idis_premium_demo_template.csv",
        mime="text/csv"
    )

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
                st.map(data.dropna(subset=['latitude', 'longitude']))
            else:
                st.error("Telemetry Error: Missing 'latitude' or 'longitude' columns.")
        else:
            st.info("Standby Mode: Displaying Base Operational Grid...")
            st.map(pd.DataFrame({'lat': [-0.0051], 'lon': [34.6036]}), zoom=14)
