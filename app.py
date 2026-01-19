import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import pandas as pd
import os

# --- 1. FIREBASE CONNECTION ---
if not firebase_admin._apps:
    try:
        if "firebase" in st.secrets:
            fb_dict = dict(st.secrets["firebase"])
            fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
            cred = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(cred)
        elif os.path.exists("firebase_key.json"):
            cred = credentials.Certificate("firebase_key.json")
            firebase_admin.initialize_app(cred)
        else:
            st.error("❌ Firebase Key Missing!")
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")

db = firestore.client()

# --- 2. DATA UTILS ---
def load_data(center, month):
    try:
        doc_id = f"{center}_{month}".replace(" ", "_")
        doc = db.collection("jamiat_erp_final").document(doc_id).get(timeout=10)
        return doc.to_dict() if doc.exists else {}
    except: return {}

def save_data(center, month, d):
    try:
        doc_id = f"{center}_{month}".replace(" ", "_")
        db.collection("jamiat_erp_final").document(doc_id).set(d)
        return True
    except: return False

def load_fixed(center):
    try:
        doc = db.collection("fixed_assets").document(center).get()
        return doc.to_dict() if doc.exists else {"ramzan": 0, "telethon": 0}
    except: return {"ramzan": 0, "telethon": 0}

# --- 3. USERS DATABASE ---
USER_DB = {
    "admin@jamiat.com": {"name": "ADMIN PORTAL JAMIATUL MADINA KOLKATA REGION", "role": "admin", "title": "Rukne Majlis", "pass": "admin786"},
    "tu.kolkataregion@gmail.com": {"name": "Jamiatul Madina Kolkata", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "jamiasilchar01@gmail.com": {"name": "Jamiatul Madina Silchar", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "jamiatulmadinaasansol@gmail.com": {"name": "Jamiatul Madina Asansole", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "jamiatulmadinakhizarpur@gmail.com": {"name": "Jamiatul Madina Khidderpore", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "kolkatajamia01@gmail.com": {"name": "Jamiatul Madina Matiaburuz", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "jamiajamshedpur@gmail.com": {"name": "Jamiatul Madina Jamshedpur", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "jamiatulmadinadhanbaad@gmail.com": {"name": "Jamiatul Madina Dhanbad", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "ranchijamia@gmail.com": {"name": "Jamiatul Madina Ranchi", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "jamiasoro@gmail.com": {"name": "Jamiatul Madina Soro", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "jamiabhadrak@gmail.com": {"name": "Jamiatul Madina Bhadrak", "role": "nazim", "title": "Nazim", "pass": "jamiat123"},
    "medukolkataregion@gmail.com": {"name": "CHAND SIR", "role": "zimmadar", "title": "REGION ASRI ZIMMADAR", "pass": "jamiat123"},
    "jtmqiraatkolkataregion@gmail.com": {"name": "AQBAR RAZA", "role": "zimmadar", "title": "REGION SHOBA QIRAT ZIMMADAR", "pass": "jamiat123"},
    "rpkolkataregion26@gmail.com": {"name": "BAHAUDDIN MADANI", "role": "zimmadar", "title": "REGION PROMOTER", "pass": "jamiat123"},
    "jtmwestbengalassam@gmail.com": {"name": "BAHAUDDIN MADANI", "role": "zimmadar", "title": "STATE NAZIM E AALA", "pass": "jamiat123"},
    "tu.kolkataregion_zim@gmail.com": {"name": "SHABBIR ALI", "role": "zimmadar", "title": "REGION TALEEMI UMOOR ZIMMADAR", "pass": "jamiat123"},
    "preppclasskolkataregion@gmail.com": {"name": "BAQAR KHAN", "role": "zimmadar", "title": "REGION PREP CLASS", "pass": "jamiat123"},
}

st.set_page_config(page_title="Jamiat ERP Admin", layout="wide")

# --- 4. CSS STYLING ---
st.markdown("""<style>
    div.stButton > button:first-child { background-color: #d9534f; color: white; border-radius: 8px; font-weight: bold; height: 45px; }
    .header-ribbon { background: white; padding: 15px; border-radius: 12px; border: 2px solid #1a938a; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .header-left { color: #d9534f; font-size: 20px; font-weight: bold; }
    .stat-pill { background: #f8f9fa; padding: 5px 15px; border-radius: 20px; border-left: 5px solid #d9534f; font-weight: bold; font-size: 14px; }
    .stat-card-red { background: #d9534f; color: white; padding: 20px; border-radius: 12px; text-align: center; }
    .login-box { background: white; padding: 40px; border-radius: 15px; box-shadow: 0px 10px 30px rgba(0,0,0,0.1); border-top: 5px solid #d9534f; }
    .section-head { background: #1a938a; color: white; padding: 10px; border-radius: 5px; font-weight: bold; margin-top: 20px; }
    .myt { width:100%; border-collapse: collapse; text-align: center; font-size: 12px; background: white; color: black; }
    .myt th, .myt td { border: 1px solid black; padding: 4px; }
    .bg-g { background-color: #D3D3D3; color: black; font-weight: bold; }
    .bg-v { background-color: #8A2BE2; color: white; font-weight: bold; }
    .bg-gr { background-color: #2E8B57; color: white; font-weight: bold; }
    .t-rd { color: red; font-weight: bold; animation: bk 1s linear infinite; }
    @keyframes bk { 50% { opacity: 0; } }
</style>""", unsafe_allow_html=True)

# --- 5. LOGIN PAGE ---
if 'user_info' not in st.session_state:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, l_col, _ = st.columns([1, 1.2, 1])
    with l_col:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>🔒 JAMIATUL MADINA KOLKATA REGION ERP PORTAL</h3>", unsafe_allow_html=True)
        l_type = st.radio("SELECT LOGIN TYPE:", ["USER", "ZIMMADAR", "ADMIN"], horizontal=True)
        u_email = st.text_input("Email Address")
        u_pass = st.text_input("Password", type="password")
        if st.button("LOG IN"):
            if u_email in USER_DB and USER_DB[u_email]["pass"] == u_pass:
                u_role = USER_DB[u_email]["role"]
                if (l_type == "ADMIN" and u_role == "admin") or (l_type == "ZIMMADAR" and u_role == "zimmadar") or (l_type == "USER" and u_role == "nazim"):
                    st.session_state['user_info'] = USER_DB[u_email]
                    st.rerun()
                else: st.error(f"Email not registered as {l_type}")
            else: st.error("Invalid Credentials")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. MAIN DASHBOARD ---
else:
    user = st.session_state['user_info']
    is_admin = (user['role'] == 'admin')
    
    st.markdown(f'<div style="background-color: #d9534f; padding: 15px; border-radius: 10px; color: white; margin-bottom: 10px; text-align: center;"><h3 style="margin:0;">Assalamu Alaikum, {user["name"]}</h3></div>', unsafe_allow_html=True)
    
    st.progress(100)
    st.write("---")
    c1, c2 = st.columns(2)
    sel_date = c1.date_input("Month Selection", value=datetime.now())
    m_key = sel_date.strftime("%B %Y")
    j_list = sorted([v["name"] for k,v in USER_DB.items() if v["role"]=="nazim"])
    target = c2.selectbox("Select Center", j_list) if is_admin else user['name']

    d = load_data(target, m_key)
    fix_main = load_fixed(target)
    def v(k): return float(d.get(k, 0.0))

    inc_fields = ['gsb', 'mab', 'dp_cash', 'dp_ashiya', 'staff_cash', 'staff_ashiya']
    rf, tf = float(fix_main.get('ramzan', 0)), float(fix_main.get('telethon', 0))
    t_inc = sum([v(k) for k in inc_fields]) + rf + tf
    exp_fields = ['salary', 'rent', 'electric', 'kitchen', 'travel', 'other_exp']
    t_exp = sum([v(k) for k in exp_fields])

    s_count = int(v('staff_count'))
    st_count = int(v('student_count'))
    total_heads = s_count + st_count
    per_head = t_exp / total_heads if total_heads > 0 else 0.0

    st.markdown(f'''<div class="header-ribbon"><div class="header-left">{user['name']}<br><small>{user['title']}</small></div>
        <div class="header-right" style="display:flex; gap:10px;"><div class="stat-pill">STAFF: {s_count}</div><div class="stat-pill">STUDENTS: {st_count}</div><div class="stat-pill">PER HEAD: ₹{per_head:,.0f}</div></div></div>''', unsafe_allow_html=True)

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.markdown(f'<div class="stat-card-red">TOTAL INCOME<h2>₹{t_inc:,.0f}</h2></div>', unsafe_allow_html=True)
    sc2.markdown(f'<div class="stat-card-red">TOTAL EXPENSE<h2>₹{t_exp:,.0f}</h2></div>', unsafe_allow_html=True)
    sc3.markdown(f'<div class="stat-card-red">DEFICIT/SURPLUS<h2>₹{t_inc-t_exp:,.0f}</h2></div>', unsafe_allow_html=True)
    sc4.markdown(f'<div class="stat-card-red">COVERAGE<h2>{(t_inc/t_exp*100 if t_exp>0 else 0):.1f}%</h2></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation Tabs
    tab_list = ["🏫 JAMIATUL MADINA DATA", "👤 ZIMMADARAN WORK", "🌎 REGION REVIEW", "📊 ALL OVER REPORTS"]
    active_tab = st.radio("SELECT SECTION:", tab_list, horizontal=True)

    if active_tab == "🏫 JAMIATUL MADINA DATA":
        if is_admin:
            with st.form("jamia_form"):
                st.markdown('<div class="section-head">👥 HEADCOUNTS</div>', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                f_sc = col1.number_input("Total Staff", value=s_count)
                f_stc = col2.number_input("Total Students", value=st_count)
                st.markdown('<div class="section-head">📉 EXPENSES</div>', unsafe_allow_html=True)
                e1, e2, e3 = st.columns(3)
                f_sal, f_ren, f_ele = e1.number_input("Salary", value=v('salary')), e2.number_input("Rent", value=v('rent')), e3.number_input("Electric", value=v('electric'))
                f_kit, f_tra, f_oth = e1.number_input("Kitchen", value=v('kitchen')), e2.number_input("Travel", value=v('travel')), e3.number_input("Other Expenses", value=v('other_exp'))
                st.markdown('<div class="section-head">💰 INCOME</div>', unsafe_allow_html=True)
                i1, i2, i3, i4 = st.columns(4)
                f_gsb, f_mab, f_dpc, f_dpa = i1.number_input("GSB", value=v('gsb')), i2.number_input("MAB", value=v('mab')), i3.number_input("DP Cash", value=v('dp_cash')), i4.number_input("DP Ashiya", value=v('dp_ashiya'))
                f_stcc, f_stca = i1.number_input("Staff Cash", value=v('staff_cash')), i2.number_input("Staff Ashiya", value=v('staff_ashiya'))
                st.markdown('<div class="section-head">🌙 RAMZAN & 📞 TELETHON</div>', unsafe_allow_html=True)
                c_ram, c_tel = st.columns(2)
                f_ram = c_ram.number_input("Ramzan Amount", value=rf)
                f_tel = c_tel.number_input("Telethon Amount", value=tf)
                if st.form_submit_button("SAVE DATA"):
                    save_data(target, m_key, {"staff_count": f_sc, "student_count": f_stc, "salary": f_sal, "rent": f_ren, "electric": f_ele, "kitchen": f_kit, "travel": f_tra, "other_exp": f_oth, "gsb": f_gsb, "mab": f_mab, "dp_cash": f_dpc, "dp_ashiya": f_dpa, "staff_cash": f_stcc, "staff_ashiya": f_stca})
                    db.collection("fixed_assets").document(target).set({"ramzan": f_ram, "telethon": f_tel})
                    st.success("Saved Successfully!"); st.rerun()
        else:
            st.markdown('<div class="section-head">👥 HEADCOUNTS (View Only)</div>', unsafe_allow_html=True)
            # (Rest of Nazim view logic here...)
            st.info("Data entry disabled for Nazim.")

    elif active_tab == "👤 ZIMMADARAN WORK":
        st.markdown('<div class="section-head">👤 MONITORING INPUTS</div>', unsafe_allow_html=True)
        # Zimmadar specific forms here
        st.write("Form for Zimmadaran will appear here.")

    elif active_tab == "🌎 REGION REVIEW" and is_admin:
        st.markdown('<div class="section-head">🌎 REGIONAL PERFORMANCE</div>', unsafe_allow_html=True)
        # Your Pandas Table logic here...
        st.write("Regional data table loading...")

    st.sidebar.button("🔒 Logout", on_click=lambda: st.session_state.clear())
