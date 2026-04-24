import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# -------------------------------
# Setup
# -------------------------------
st.set_page_config(page_title="Smart Attendance System", page_icon="🎓")

st.title("🎓 Smart Attendance Management System")
st.markdown("### AI-Based Attendance Tracking (Prototype)")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Home", "Upload Data", "Results", "Analytics"])

# Create folder
os.makedirs("student_images", exist_ok=True)

# -------------------------------
# HOME
# -------------------------------
if menu == "Home":
    st.subheader("Welcome")
    st.write("This system demonstrates automated attendance tracking using facial recognition concepts.")
    st.info("Upload student images and an attendance image to simulate recognition.")

# -------------------------------
# UPLOAD DATA
# -------------------------------
elif menu == "Upload Data":
    st.subheader("Upload Data")

    # Upload student images
    student_files = st.file_uploader(
        "Upload student images (filename = student name)",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png"]
    )

    if student_files:
        for file in student_files:
            with open(os.path.join("student_images", file.name), "wb") as f:
                f.write(file.getbuffer())
        st.success(f"{len(student_files)} student images uploaded successfully.")

    # Upload attendance image
    attendance_file = st.file_uploader(
        "Upload attendance image",
        type=["jpg", "jpeg", "png"]
    )

    if attendance_file:
        st.image(attendance_file, caption="Attendance Image", use_column_width=True)

    # Run recognition (simulated)
    if st.button("Run Recognition"):
        if not student_files:
            st.warning("Please upload student images first.")
        elif not attendance_file:
            st.warning("Please upload an attendance image.")
        else:
            # Simulated recognition: assume all uploaded students are present
            recognized_students = [file.name.split(".")[0] for file in student_files]

            now = datetime.now()

            df = pd.DataFrame({
                "Name": recognized_students,
                "Date": [now.strftime("%Y-%m-%d")] * len(recognized_students),
                "Time": [now.strftime("%H:%M:%S")] * len(recognized_students),
                "Status": ["Present"] * len(recognized_students)
            })

            # Store in session
            st.session_state["attendance"] = df

            # Save to CSV
            df.to_csv("attendance.csv", index=False)

            st.success("Recognition completed successfully!")
            st.write("### Recognized Students:")
            st.dataframe(df)

# -------------------------------
# RESULTS
# -------------------------------
elif menu == "Results":
    st.subheader("Attendance Results")

    if "attendance" in st.session_state:
        st.dataframe(st.session_state["attendance"])
    elif os.path.exists("attendance.csv"):
        df = pd.read_csv("attendance.csv")
        st.dataframe(df)
    else:
        st.warning("No attendance data available yet.")

# -------------------------------
# ANALYTICS
# -------------------------------
elif menu == "Analytics":
    st.subheader("Attendance Analytics")

    if os.path.exists("attendance.csv"):
        df = pd.read_csv("attendance.csv")

        st.metric("Total Attendance Records", len(df))
        st.metric("Unique Students", df["Name"].nunique())

        st.markdown("### Attendance Frequency")
        st.bar_chart(df["Name"].value_counts())
    else:
        st.warning("No attendance data available.")
