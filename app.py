import streamlit as st
import pandas as pd
import json
import urllib.request
from datetime import datetime

st.set_page_config(page_title="IDIS Premium Platform", page_icon="🌎", layout="wide")

# Safe validation checks for secure cloud database connections
if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
    st.error("🚨 Infrastructure Error: Missing secure Cloud Database Secrets connection tokens.")
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

        # Safety buffer timeout set to 30 seconds to bypass cloud routing lag
        with urllib.request.urlopen(req, timeout=30) as response:
            records = json.loads(response.read().decode('utf-8'))
        if not records:
            return False, "Telemetry ID not found in database registry."

        # Correctly pull the data record from the list array bucket safely
        if isinstance(records, list):
            if len(records) == 0:
                return False, "Telemetry ID not found in database registry."
            client_data = records[0]
        else:
            client_data = records

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

        # --- MULTI-CURRENCY VISUAL SELECTOR TOOL ---
        currency_choice = st.radio(
            "Select Preferred Billing Currency Visualizer:",
            options=["💵 USD (International Accounts)", "🇰🇪 KES (East African Accounts)"],
            horizontal=True
        )

        if "USD" in currency_choice:
            st.info("💳 Enterprise Tier Access: $1,000 USD / Month")
            st.caption("ℹ️ *International payments are cleared securely via automated global settlement networks as KES 130,000.*")
        else:
            st.info("💳 Enterprise Tier Access: KES 130,000 / Month")
            st.caption("ℹ️ *Local accounts support instant mobile money clearing through Safaricom M-Pesa channels.*")

        REAL_PAYSTACK_LINK = "https://paystack.shop/pay/25lh3e-hx5"
        st.write("To initialize secure international credit card or M-Pesa clearance, route through our global financial merchant node:")
        st.markdown(f"[➡️ Proceed to Secure Gateway Checkout]({REAL_PAYSTACK_LINK})")

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
        file_name="idis_premium_template.csv",
        mime="text/csv"
    )
    # Split-view platform interface layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Enterprise Intelligence Controls")
        upload_file = st.file_uploader("Ingiza Telemetry Dataset (CSV)", type=["csv"])

        # Initialize mapping selection keys
        lat_column = None
        lon_column = None

        if upload_file is not None:
            upload_file.seek(0)
            file_peek = pd.read_csv(upload_file, nrows=2)
            # Remove any trailing or leading whitespace from raw file headers
            all_columns = [str(c).strip() for c in file_peek.columns]

            st.markdown("### 🛠️ Smart Column Remapping Interface")
            st.info("Our parsing engine automatically detected the following spreadsheet headers. Select the columns that hold your geographic coordinates:")

            def_lat_idx = 0
            def_lon_idx = 1 if len(all_columns) > 1 else 0

            for i, col in enumerate(all_columns):
                cleaned_name = str(col).strip().lower()
                if cleaned_name in ['lat', 'latitude', 'gps_lat', 'y', 'y_coord', 'timestamp']:
                    def_lat_idx = i
                if cleaned_name in ['lon', 'longitude', 'long', 'gps_lon', 'x', 'x_coord', 'job title', 'job_title']:
                    def_lon_idx = i

            lat_column = st.selectbox("Select Latitude Column:", options=all_columns, index=def_lat_idx)
            lon_column = st.selectbox("Select Longitude Column:", options=all_columns, index=def_lon_idx)

    with col2:
        st.header("Real-Time Spatiotemporal Map Viewer")
        if upload_file is not None and lat_column and lon_column:
            upload_file.seek(0)
            data = pd.read_csv(upload_file)
            # Standardize file headers in memory to align cleanly with selections
            data.columns = [str(c).strip() for c in data.columns]

            st.success("=== TELEMETRY INGESTION SUCCESSFUL ===")
            st.dataframe(data.head(10))

            if lat_column in data.columns and lon_column in data.columns:
                st.info(f"Dynamic System Override: Mapping coordinates using custom columns: [{lat_column}] and [{lon_column}]...")

                # --- SOLID MILITARY DEFENSE LAYER ---
                # Coerce data columns into numbers, automatically converting text errors into blank slots safely
                data['lat_numeric'] = pd.to_numeric(data[lat_column], errors='coerce')
                data['lon_numeric'] = pd.to_numeric(data[lon_column], errors='coerce')

                # Identify which rows are structurally missing numerical elements right now
                missing_mask = data['lat_numeric'].isna() | data['lon_numeric'].isna()
                
                # Check for boundary-breaking items among rows that actually have numbers
                boundary_mask = ~missing_mask & (
                    (data['lat_numeric'] < -90.0) | (data['lat_numeric'] > 90.0) |
                    (data['lon_numeric'] < -180.0) | (data['lon_numeric'] > 180.0)
                )

                # Collect the specific IDs of quarantined items safely even if 'feature_id' doesn't exist
                quarantined_ids = []
                quarantined_rows_df = data[missing_mask | boundary_mask]
                
                if 'feature_id' in data.columns:
                    quarantined_ids = [str(x) for x in quarantined_rows_df['feature_id'].tolist()]
                elif 'id' in data.columns:
                    quarantined_ids = [str(x) for x in quarantined_rows_df['id'].tolist()]
                else:
                    # Fallback to row numbers if no explicit ID column is present in the file
                    quarantined_ids = [str(idx + 1) for idx in quarantined_rows_df.index.tolist()]
                
                quarantined_rows = len(quarantined_ids)

                # Build clean dataframe map inputs cleanly without risking a KeyError crash
                clean_spatial_data = data[~missing_mask & ~boundary_mask].copy()
                clean_spatial_data['latitude'] = clean_spatial_data['lat_numeric']
                clean_spatial_data['longitude'] = clean_spatial_data['lon_numeric']

                # Display a clean alert dashboard if bad rows were successfully intercepted
                if quarantined_rows > 0:
                    st.warning(f"⚠️ Security Guard Active: {quarantined_rows} row(s) contained unparseable or physically impossible coordinates and were safely isolated to prevent an application crash.")

                # Safely render the mapping canvas with the verified dataset
                st.map(clean_spatial_data[['latitude', 'longitude']])

                # --- PREMIUM EXPORT REPORT GENERATION UTILITY ---
                st.markdown("### 📊 Operational Summary Report")
                total_assets = len(clean_spatial_data)
                report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S EAT")

                report_text = "==================================================\n"
                report_text += "        SOVEREIGN DISASTER INFORMATICS SYSTEM     \n"
                report_text += "             CRITICAL SYSTEM MAP REPORT           \n"
                report_text += "==================================================\n"
                report_text += f"Generated On: {report_time}\n"
                report_text += f"Authorized Corporate Node: {st.session_state.user_node}\n"
                report_text += f"Total Active Telemetry Hotspots Mapped: {total_assets}\n"
                report_text += f"Quarantined Anomalous Records: {quarantined_rows}\n"
                
                # Write out the exact faulty codes to the text export
                if quarantined_rows > 0:
                    report_text += f"⚠️ Flagged Broken Record IDs: {', '.join(quarantined_ids)}\n"
                
                report_text += "------------------ MAPPED COORDINATES ------------------\n"

                for idx, row in clean_spatial_data.iterrows():
                    if 'feature_id' in clean_spatial_data.columns:
                        display_id = row['feature_id']
                    elif 'id' in clean_spatial_data.columns:
                        display_id = row['id']
                    else:
                        display_id = idx + 1
                    report_text += f"📍 Record ID {display_id}: Lat {row['latitude']} | Lon {row['longitude']}\n"

                report_text += "\n==================================================\n"
                report_text += "END OF TELEMETRY REPORT | SECURE ENTERPRISE LAYER\n"

                st.download_button(
                    label="💾 Export Map Report (.TXT)",
                    data=report_text,
                    file_name=f"idis_disaster_map_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Mapping Refused: Selected remapping column nodes do not exist in dataset memory.")
        else:
            st.info("Standby Mode: Displaying Base Operational Grid...")
            st.map(pd.DataFrame({'lat': [-0.0051], 'lon': [34.6036]}), zoom=14)
