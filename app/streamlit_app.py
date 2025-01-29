import streamlit as st
import pandas as pd
from calculate_confidence import calculate_confidence_for_interval

# Streamlit app setup
st.set_page_config(
    page_title="Location Confidence Calculator", page_icon="📍", layout="centered"
)
st.title("📍 Location Confidence Calculator")
st.markdown(
    """
This app allows you to upload a CSV file containing cell tower triangulation data
and calculates the confidence of the subscriber's location for a specified time interval.

**Steps to Use:**
1. Upload your CSV file.
2. Enter the start and end time for the interval.
3. View the dominant state and confidence level.
"""
)

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file is not None:
    # Load the data
    data = pd.read_csv(uploaded_file)
    data["Local Date & Time"] = pd.to_datetime(
        data["Local Date & Time"], format="%m/%d/%y %H:%M", errors="coerce"
    )

    # Display a preview of the uploaded data
    st.write("### Uploaded Data Preview")
    st.dataframe(data.head(), use_container_width=True)

    # Input fields for interval selection
    st.write("### Select Time Interval")
    start_time = st.text_input("Start Time (YYYY-MM-DD HH:MM:SS)")
    end_time = st.text_input("End Time (YYYY-MM-DD HH:MM:SS)")

    if st.button("Calculate Confidence"):
        # Validate inputs
        try:
            start_time = pd.to_datetime(start_time)
            end_time = pd.to_datetime(end_time)

            if start_time >= end_time:
                st.error("🚨 Start time must be before end time.")
            else:
                # Calculate confidence for the selected interval
                result = calculate_confidence_for_interval(data, start_time, end_time)
                st.write("### Confidence Calculation Result")
                st.dataframe(result, use_container_width=True)

                # Show a summary
                st.success(
                    f"✅ Calculation complete for interval: {start_time} to {end_time}"
                )
        except Exception as e:
            st.error(f"❌ Invalid input: {e}")
else:
    st.info("💡 Please upload a CSV file to get started.")
