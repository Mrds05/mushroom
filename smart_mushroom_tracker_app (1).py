
import streamlit as st
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt

# Title and sidebar navigation
st.set_page_config(page_title="Smart Mushroom Growth Tracker", layout="centered")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "New Log Entry", "Visual Trends", "Logbook", "Export Report"])

# Initialize session state data
if "data" not in st.session_state:
    st.session_state.data = []

# Dashboard Page
if page == "Dashboard":
    st.title("📊 Smart Mushroom Growth Tracker")
    st.subheader("Welcome! Track your mushroom growth here.")

    if st.session_state.data:
        latest = st.session_state.data[-1]
        st.metric("Last Recorded Temperature", f"{latest['Temperature']}°C")
        st.metric("Last Recorded Humidity", f"{latest['Humidity']}%")
        st.write(f"**Last Stage:** {latest['Growth Stage']}")
        st.write(f"**Notes:** {latest['Notes']}")
    else:
        st.info("No entries yet. Go to 'New Log Entry' to begin.")

# New Log Entry
elif page == "New Log Entry":
    st.title("📝 New Growth Log")
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            entry_date = st.date_input("Date", value=date.today())
            temp = st.number_input("Temperature (°C)", step=0.1)
        with col2:
            humidity = st.number_input("Humidity (%)", step=0.1)
            stage = st.selectbox("Growth Stage", ["Mycelium", "Pinhead", "Fruiting", "Mature", "Harvested"])

        notes = st.text_area("Observation Notes")
        photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Submit Entry")

        if submit:
            st.session_state.data.append({
                "Date": entry_date,
                "Temperature": temp,
                "Humidity": humidity,
                "Growth Stage": stage,
                "Notes": notes,
                "Photo": photo
            })
            st.success("Entry submitted successfully!")

# Visual Trends
elif page == "Visual Trends":
    st.title("📈 Growth Trends")
    if not st.session_state.data:
        st.warning("No data to display. Please add log entries.")
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
    else:
        st.info("No logs available yet.")

# Export Report
elif page == "Export Report":
    st.title("📤 Export Report")
    st.write("Feature coming soon: Export logs to PDF or CSV.")
