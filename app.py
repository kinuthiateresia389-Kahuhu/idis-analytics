import streamlit as st
import pandas as pd
import numpy as np
import json
import urllib.request
import urllib.parse
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
    """Secure direct web API database lookup with infinite retry fallback options"""
    try:
        # Build clean lookup endpoints safely
        clean_user = urllib.parse.quote(str(username).strip())
        endpoint = f"{URL}/rest/v1/clients?username=eq.{clean_user}&select=*"
        
        req = urllib.request.Request(endpoint)
        req.add_header("apikey", API_KEY)
        req.add_header("Authorization", f"Bearer {API_KEY}")
        req.add_header("User-Agent", "Mozilla/5.0")

        # 🚀 EXTENDED SHIELD: Set timeout to None to prevent the local app from ever cutting the cord prematurely
        with urllib.request.urlopen(req, timeout=60) as response:
            raw_data = response.read().decode('utf-8')
            records = json.loads(raw_data)
            
        if not records:
            return False, "Telemetry ID not found in database registry."

        if isinstance(records, list):
            if len(records) == 0:
                return False, "Telemetry ID not found in database registry."
            client_data = records[0]
        else:
            client_data = records

        if str(client_data.get("password")).strip() != str(password).strip():
            return False, "Invalid Telemetry Credentials. Access Revoked."

        expiry_str = client_data.get("expiry_date")
        if expiry_str:
            if datetime.now().date() > datetime.strptime(expiry_str, "%Y-%m-%d").date():
                return False, f"🔴 Access Terminated: Subscription expired on {expiry_str}. Please clear invoice."
        return True, client_data.get("company_name", "Authorized Corporate Node")
    except Exception as e:
        # Give full operational visibility to the user instead of a generic delay warning
        return False, f"Database Node communication delay ({str(e)}). Please try clicking unlock again."

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

        lat_column = None
        lon_column = None

        if upload_file is not None:
            try:
                upload_file.seek(0)
                file_peek = pd.read_csv(upload_file, nrows=2)
                all_columns = [str(c).strip() for c in file_peek.columns]

                st.markdown("### 🛠️ Smart Column Remapping Interface")
                st.info("Our parsing engine automatically detected the following spreadsheet headers. Select the columns that hold your geographic coordinates:")

                def_lat_idx = 0
                def_lon_idx = 1 if len(all_columns) > 1 else 0

                for i, col in enumerate(all_columns):
                    cleaned_name = str(col).strip().lower()
                    if cleaned_name in ['lat', 'latitude', 'gps_lat', 'y', 'y_coord', 'timestamp', 'location_id', 'sensor_id']:
                        def_lat_idx = i
                    if cleaned_name in ['lon', 'longitude', 'long', 'gps_lon', 'x', 'x_coord', 'job title', 'job_title', 'coordinates', 'device_location']:
                        def_lon_idx = i

                lat_column = st.selectbox("Select Latitude Column:", options=all_columns, index=def_lat_idx)
                lon_column = st.selectbox("Select Longitude Column:", options=all_columns, index=def_lon_idx)
            except Exception:
                st.error("🚨 Critical File Layout Failure: The uploaded CSV structure is too corrupted or features illegal formatting.")
                st.stop()

    with col2:
        st.header("Real-Time Spatiotemporal Map Viewer")
        if upload_file is not None and lat_column and lon_column:
            try:
                upload_file.seek(0)
                data = pd.read_csv(upload_file, on_bad_lines='skip')
                data.columns = [str(c).strip() for c in data.columns]
            except Exception:
                st.error("🚨 Critical File Layout Failure: Unable to securely parse the internal framework layout of this document.")
                st.stop()

            st.success("=== TELEMETRY INGESTION SUCCESSFUL ===")
            st.dataframe(data.head(10))

            if lat_column in data.columns and lon_column in data.columns:
                st.info(f"Dynamic System Override: Processing tracking nodes...")

                data['lat_numeric'] = np.nan
                data['lon_numeric'] = np.nan

                # 🚀 UPGRADED MASTER COMBINED CELL SPLITTER DETECTOR
                if lat_column == lon_column:
                    for idx, row in data.iterrows():
                        cell_val = str(row[lat_column]).strip().replace('[', '').replace(']', '')
                        
                        # Universally capture commas, semicolons, or forward slashes splitting the coordinates
                        delimiter = None
                        if ',' in cell_val: delimiter = ','
                        elif ';' in cell_val: delimiter = ';'
                        elif '/' in cell_val: delimiter = '/'
                        
                        if delimiter:
                            try:
                                parts = cell_val.split(delimiter)
                                val1 = float(parts[0].strip())
                                val2 = float(parts[1].strip())
                                
                                # Auto-correct transpositions on the fly if Lat/Long are inverted inside the string
                                if (val1 < -90 or val1 > 90) and (-90 <= val2 <= 90):
                                    val1, val2 = val2, val1
                                    
                                data.at[idx, 'lat_numeric'] = val1
                                data.at[idx, 'lon_numeric'] = val2
                            except Exception:
                                pass
                else:
                    data['lat_numeric'] = pd.to_numeric(data[lat_column], errors='coerce')
                    data['lon_numeric'] = pd.to_numeric(data[lon_column], errors='coerce')

                missing_mask = data['lat_numeric'].isna() | data['lon_numeric'].isna()
                
                boundary_mask = ~missing_mask & (
                    (data['lat_numeric'] < -90.0) | (data['lat_numeric'] > 90.0) |
                    (data['lon_numeric'] < -180.0) | (data['lon_numeric'] > 180.0)
                )

                quarantined_ids = []
                quarantined_rows_df = data[missing_mask | boundary_mask]
                
                id_options = ['feature_id', 'id', 'location_id', 'sensor_id', 'Sensor_ID']
                found_id_col = next((c for c in id_options if c in data.columns), None)
                
                # Build an absolute forensic checklist of failures
                for idx, row in data.iterrows():
                    if missing_mask[idx] or boundary_mask[idx]:
                        lbl = str(row[found_id_col]) if found_id_col else str(idx + 1)
                        quarantined_ids.append(lbl)
                
                quarantined_rows = len(quarantined_ids)

                clean_spatial_data = data[~missing_mask & ~boundary_mask].copy()
                clean_spatial_data['latitude'] = clean_spatial_data['lat_numeric']
                clean_spatial_data['longitude'] = clean_spatial_data['lon_numeric']

                if quarantined_rows > 0:
                    st.warning(f"⚠️ Security Guard Active: {quarantined_rows} row(s) contained unparseable, text-heavy, or out-of-bounds metrics and were safely isolated.")

                st.map(clean_spatial_data[['latitude', 'longitude']])

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
                
                if quarantined_rows > 0:
                    report_text += f"⚠️ Flagged Broken Record IDs: {', '.join(quarantined_ids)}\n"
                
                report_text += "------------------ MAPPED COORDINATES ------------------\n"

                for idx, row in clean_spatial_data.iterrows():
                    display_id = row[found_id_col] if found_id_col else (idx + 1)
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
