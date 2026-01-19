import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# --- 1. FIREBASE CONNECTION ---
if not firebase_admin._apps:
    try:
        fb_dict = dict(st.secrets["firebase"])
        fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(cred)
    except:
        st.error("Firebase connection error")

db = firestore.client()

# --- 2. HEADER ---
st.markdown("""<style>
    .welcome-red { background-color: #d9534f; color: white; padding: 20px; border-radius: 12px; text-align: center; font-weight: 700; font-size: 22px; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="welcome-red">ASSALAMU ALAIKUM - ERP DASHBOARD</div>', unsafe_allow_html=True)

# --- 3. TABS (DIRECT SHOW) ---
tab1, tab2, tab3 = st.tabs(["📊 Nazim Dashboard", "👤 Zimmadar View", "📜 Reports"])

with tab1:
    st.write("### Welcome Nazim Sahab")
    st.info("Kolkata Region ki progress yahan show hogi.")

with tab2:
    st.write("### 👤 Zimmadar Monitoring Form")
    z_type = st.radio("Zimmadar Select Karein:", ["Qari Akbar (Qirat)", "Chand Sir (Asri)", "Bahauddin Bhai (Promotion)"], horizontal=True)
    
    if z_type == "Qari Akbar (Qirat)":
        st.subheader("📖 Qirat Darja-war Jaiza")
        col1, col2 = st.columns(2)
        jamia = col1.selectbox("Select Jamia:", ["Kolkata", "Howrah", "Ranchi"])
        darja = col2.selectbox("Select Darja:", ["Ula", "Saniya", "Salisa", "Rabiya"])
        t_std = st.number_input("Total Talba", min_value=0)
        if st.button("SAVE QIRAT REPORT"):
            st.success("Report saved successfully!")

    elif z_type == "Chand Sir (Asri)":
        st.subheader("🎓 Asri Education (English/Math)")
        sub = st.selectbox("Subject:", ["English", "Math"])
        score = st.slider("Average Performance %", 0, 100, 70)
        st.button("SUBMIT ASRI DATA")

with tab3:
    st.write("### Reports Section")
    st.write("Monthly data download karne ka option yahan aayega.")
