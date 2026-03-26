import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Dynamic Cell Tracker", layout="wide")

# --- LOGO HELPER ---
def get_logo():
    # Checking for the two most likely filenames from your uploads
    if os.path.exists("logo.png.jpeg"):
        return "logo.png.jpeg"
    elif os.path.exists("logo.jpeg"):
        return "logo.jpeg"
    return None

LOGO_PATH = get_logo()

# --- DATABASE SETUP ---
DB_FILE = "members.txt"

def load_members():
    if not os.path.exists(DB_FILE):
        return ["Ethan"]
    with open(DB_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def add_member(name):
    with open(DB_FILE, "a") as f:
        f.write(name + "\n")

# --- APP START ---
all_members = load_members()
all_members.sort()

# --- SIDEBAR: LOGO & SETTINGS ---
with st.sidebar:
    if LOGO_PATH:
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.error("Logo not found. Ensure 'logo.jpeg' is in the folder.")
    
    st.divider()
    st.header("Meeting Info")
    meeting_name = st.text_input("Meeting Name", "Dynamic Cell")
    meeting_date = st.date_input("Date", datetime.now())
    
    st.divider()
    st.header("Add New Member")
    new_name = st.text_input("Full Name")
    if st.button("Add to List", use_container_width=True):
        if new_name and new_name not in all_members:
            add_member(new_name)
            st.success(f"Added {new_name}!")
            st.rerun() 
        else:
            st.warning("Name is empty or already exists.")

# --- MAIN AREA: LOGO & TITLE ---
col1, col2 = st.columns([0.15, 0.85])
with col1:
    if LOGO_PATH:
        st.image(LOGO_PATH, width=80)
with col2:
    st.title("Dynamic Cell Attendance Tracker")

st.write("---")

# --- LIVE COUNTER ---
# This part updates instantly as you check boxes
attendance_data = []
search_query = st.text_input("🔍 Search for a member...", "")
filtered_members = [m for m in all_members if search_query.lower() in m.lower()]

# --- ATTENDANCE CHECKLIST ---
st.subheader(f"Marking Attendance: {meeting_name}")

if filtered_members:
    cols = st.columns(3) 
    for i, member in enumerate(filtered_members):
        with cols[i % 3]:
            if st.checkbox(member, key=f"att_{member}"):
                attendance_data.append(member)
else:
    st.warning("No members found.")

# Display the Live Count in a nice metric box
st.write("---")
c1, c2 = st.columns(2)
with c1:
    st.metric(label="Total Present Today", value=len(attendance_data))

# --- SUBMIT & DOWNLOAD ---
if st.button("Submit & Save Report", type="primary", use_container_width=True):
    if attendance_data:
        df = pd.DataFrame({
            "Meeting": [meeting_name] * len(attendance_data),
            "Date": [meeting_date] * len(attendance_data),
            "Attendee": attendance_data
        })
        
        st.success(f"Done! {len(attendance_data)} people recorded.")
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📩 Download CSV Report", data=csv, file_name=f"{meeting_name}_{meeting_date}.csv", use_container_width=True)
        st.balloons()
    else:
        st.error("Please select at least one person.")
