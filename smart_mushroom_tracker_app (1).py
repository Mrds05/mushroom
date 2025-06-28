# Smart Mushroom Growth Tracker with Extended Features

import streamlit as st
from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt
import base64
import os

st.set_page_config(page_title="Smart Mushroom Growth Tracker", layout="centered")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Dashboard", "New Log Entry", "Visual Trends", "Logbook",
    "Reports & Analytics", "Settings"
])

# Initialize session state data
if "data" not in st.session_state:
    st.session_state.data = []

if "alerts" not in st.session_state:
    st.session_state.alerts = {"temp_max": 30.0, "humidity_min": 80.0}

if "language" not in st.session_state:
    st.session_state.language = "English"

# Dashboard
if page == "Dashboard":
    st.title("📊 Smart Mushroom Growth Tracker")
    if st.session_state.data:
        latest = st.session_state.data[-1]
        st.metric("Temperature", f"{latest['Temperature']}°C")
        st.metric("Humidity", f"{latest['Humidity']}%")
        st.write(f"**Stage:** {latest['Growth Stage']}")
        st.write(f"**Note:** {latest['Notes']}")
        if latest['Temperature'] > st.session_state.alerts['temp_max']:
            st.warning("🔥 Temperature is above optimal range!")
        if latest['Humidity'] < st.session_state.alerts['humidity_min']:
            st.warning("💧 Humidity is below optimal range!")
    else:
        st.info("No entries yet. Go to 'New Log Entry' to start.")

# New Log Entry
elif page == "New Log Entry":
    st.title("📝 New Growth Log")
    with st.form("entry_form"):
        entry_date = st.date_input("Date", value=date.today())
        temp = st.number_input("Temperature (°C)", step=0.1)
        humidity = st.number_input("Humidity (%)", step=0.1)
        stage = st.selectbox("Growth Stage", ["Mycelium", "Pinhead", "Fruiting", "Mature", "Harvested"])
        notes = st.text_area("Observation Notes")
        photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Submit")

        if submit:
            st.session_state.data.append({
                "Date": entry_date,
                "Temperature": temp,
                "Humidity": humidity,
                "Growth Stage": stage,
                "Notes": notes,
                "Photo": photo.name if photo else None
            })
            if photo:
                with open(f"photos/{photo.name}", "wb") as f:
                    f.write(photo.getbuffer())
            st.success("Entry added!")

# Visual Trends
elif page == "Visual Trends":
    st.title("📈 Visual Trends")
    if not st.session_state.data:
        st.warning("No data yet.")
    else:
        df = pd.DataFrame(st.session_state.data)
        df["Date"] = pd.to_datetime(df["Date"])
        fig, ax = plt.subplots()
        ax.plot(df["Date"], df["Temperature"], label="Temperature (°C)", marker="o")
        ax.plot(df["Date"], df["Humidity"], label="Humidity (%)", marker="s")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# Logbook
elif page == "Logbook":
    st.title("📚 Logbook")
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        st.dataframe(df.drop(columns=["Photo"]))
        for log in st.session_state.data:
            if log['Photo']:
                st.image(f"photos/{log['Photo']}", width=300, caption=f"{log['Date']} - {log['Growth Stage']}")
    else:
        st.info("No logs yet.")

# Reports & Analytics
elif page == "Reports & Analytics":
    st.title("📤 Reports & Analytics")
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        csv = df.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv).decode()
        st.download_button("📥 Download CSV Report", data=csv, file_name="mushroom_growth_log.csv", mime="text/csv")
    else:
        st.info("No data to export.")

# Settings
elif page == "Settings":
    st.title("⚙️ Settings")
    st.subheader("Alert Thresholds")
    st.session_state.alerts['temp_max'] = st.slider("Max Temperature Alert (°C)", 20.0, 40.0, st.session_state.alerts['temp_max'])
    st.session_state.alerts['humidity_min'] = st.slider("Min Humidity Alert (%)", 60.0, 100.0, st.session_state.alerts['humidity_min'])

    st.subheader("Language (future use)")
    st.selectbox("Select Language", ["English", "Marathi", "Hindi"], index=0, key="language")

