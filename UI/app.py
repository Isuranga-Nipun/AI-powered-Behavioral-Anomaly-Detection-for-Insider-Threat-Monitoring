import pandas as pd
import plotly.express as px
import streamlit as st
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["Instruction"]

# Load collections
file_access_collection = db["File_abnormalities"]
keyboard_collection = db["Keyboard_abnormalities"]
mouse_collection = db["Mouse_abnormalities"]


# Utility function to fetch data from MongoDB
def fetch_data(collection, limit=1000):
    return pd.DataFrame(list(collection.find().limit(limit)))


# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Choose a section:",
    ["Dashboard", "File Access Patterns", "Keyboard Patterns", "Mouse Patterns"]
)

# Bootstrap integration
st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

st.title("Abnormal Activity Monitoring Dashboard")

if section == "Dashboard":
    st.subheader("Overview")
    st.markdown("This dashboard visualizes abnormal patterns detected in File Access, Keyboard, and Mouse data.")

    # Overview metrics
    file_count = file_access_collection.count_documents({})
    keyboard_count = keyboard_collection.count_documents({})
    mouse_count = mouse_collection.count_documents({})

    col1, col2, col3 = st.columns(3)
    col1.metric("Abnormal File Events", file_count)
    col2.metric("Abnormal Keyboard Events", keyboard_count)
    col3.metric("Abnormal Mouse Events", mouse_count)

    # Frequency over time
    st.subheader("Abnormal Events Over Time")
    file_data = fetch_data(file_access_collection)

    print(file_data["time"], 'head')
    print(file_data)

    file_data["time"] = pd.to_datetime(file_data["time"], errors='coerce')
    file_time_chart = px.line(file_data, x="time", y=file_data.index, title="File Events Over Time")
    st.plotly_chart(file_time_chart, use_container_width=True)

elif section == "File Access Patterns":
    st.subheader("File Access Patterns")
    file_data = fetch_data(file_access_collection)
    if not file_data.empty:
        st.dataframe(file_data)

        # Visualizations
        st.subheader("Event Types Distribution")
        event_type_chart = px.bar(file_data, x="event_type", title="Event Types Distribution")
        st.plotly_chart(event_type_chart, use_container_width=True)

        st.subheader("File Access Timeline")
        file_time_chart = px.line(file_data, x="time", y=file_data.index, title="File Events Timeline")
        st.plotly_chart(file_time_chart, use_container_width=True)
    else:
        st.warning("No abnormal file access data available.")

elif section == "Keyboard Patterns":
    st.subheader("Keyboard Patterns")
    keyboard_data = fetch_data(keyboard_collection)
    if not keyboard_data.empty:
        st.dataframe(keyboard_data)

        # Visualizations
        st.subheader("Inter-Key Interval Distribution")
        interval_chart = px.histogram(keyboard_data, x="inter_key_interval", title="Inter-Key Interval Distribution")
        st.plotly_chart(interval_chart, use_container_width=True)
    else:
        st.warning("No abnormal keyboard data available.")

elif section == "Mouse Patterns":
    st.subheader("Mouse Patterns")
    mouse_data = fetch_data(mouse_collection)
    if not mouse_data.empty:
        st.dataframe(mouse_data)

        # Visualizations
        st.subheader("Mouse Speed Over Time")
        mouse_speed_chart = px.line(mouse_data, x="time", y="speed", title="Mouse Speed Over Time")
        st.plotly_chart(mouse_speed_chart, use_container_width=True)

        st.subheader("Mouse Movement Flow")

        if mouse_data.empty:
            st.error("No data available for heatmap")
        else:
            # Convert records to a DataFrame
            st.dataframe(mouse_data)
            df = pd.DataFrame(mouse_data)
            print(df["x"],'df')

            # Generate heatmap
            plt.figure(figsize=(10, 8))
            sns.kdeplot(x=df["x"], y=df["y"], cmap="Blues", color='Red', fill=True)
            plt.title("Mouse Flow Heatmap")
            plt.xlabel("X Coordinates")
            plt.ylabel("Y Coordinates")

            # Save the heatmap to a buffer and display it in Streamlit
            st.pyplot(plt)

    else:
        st.warning("No abnormal mouse data available.")

# Footer
st.markdown(
    """
    <footer class="bg-light text-center text-lg-start">
    <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
        © 2024 Abnormal Activity Monitoring | Built with Streamlit and Bootstrap
    </div>
    </footer>
    """,
    unsafe_allow_html=True,
)
