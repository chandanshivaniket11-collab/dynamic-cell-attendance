import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Attendance Tracker", layout="wide")

# --- DATABASE SETUP (Simple Text File) ---
DB_FILE = "members.txt"

def load_members():
    if not os.path.exists(DB_FILE):
        return ["Ethan"] # Default name if file is empty
    with open(DB_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def add_member(name):
    with open(DB_FILE, "a") as f:
        f.write(name + "\n")

# --- APP START ---
st.title("📊 Universal Attendance Tracker")

# Load the current list of members
all_members = load_members()
all_members.sort()

# --- SIDEBAR: MEETING & NEW MEMBERS ---
with st.sidebar:
    st.header("Meeting Info")
    meeting_name = st.text_input("Meeting Name", "Dynamic Cell")
    meeting_date = st.date_input("Date", datetime.now())
    
    st.divider()
    
    st.header("Add New Member")
    new_name = st.text_input("Full Name")
    if st.button("Add to List"):
        if new_name and new_name not in all_members:
            add_member(new_name)
            st.success(f"Added {new_name}!")
            st.rerun() # Refresh the app to show the new name
        else:
            st.warning("Name is empty or already exists.")

# --- MAIN AREA: SEARCH & ATTENDANCE ---
st.subheader(f"Mark Attendance: {meeting_name}")

search_query = st.text_input("🔍 Search for a member...", "")
filtered_members = [m for m in all_members if search_query.lower() in m.lower()]

attendance_data = []

if filtered_members:
    cols = st.columns(3) 
    for i, member in enumerate(filtered_members):
        with cols[i % 3]:
            if st.checkbox(member, key=member):
                attendance_data.append(member)
else:
    st.warning("No members found.")

# --- SUBMIT & DOWNLOAD ---
st.divider()
if st.button("Submit & Save Report", type="primary"):
    if attendance_data:
        df = pd.DataFrame({
            "Meeting": [meeting_name] * len(attendance_data),
            "Date": [meeting_date] * len(attendance_data),
            "Attendee": attendance_data
        })
        
        st.success(f"Done! {len(attendance_data)} people recorded.")
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV Report", data=csv, file_name=f"{meeting_name}_{meeting_date}.csv")
    else:
        st.error("Please select at least one person.")
