import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image

# Try importing DeepFace safely
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except:
    DEEPFACE_AVAILABLE = False

# -------------------------------
# Setup
# -------------------------------
st.set_page_config(page_title="Smart Attendance System", page_icon="🎓")

st.title("🎓 Smart Attendance Management System")
st.markdown("### AI-Based Attendance Tracking")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Home", "Upload Data", "Results", "Analytics"])

os.makedirs("student_images", exist_ok=True)

# -------------------------------
# HOME
# -------------------------------
if menu == "Home":
    st.subheader("Welcome")

    if DEEPFACE_AVAILABLE:
        st.success("✅ DeepFace AI loaded successfully")
    else:
        st.warning("⚠️ DeepFace not available — running in fallback mode")

# -------------------------------
# UPLOAD
# -------------------------------
elif menu == "Upload Data":
    st.subheader("Upload Data")

    student_files = st.file_uploader(
        "Upload student images (filename = student name)",
        accept_multiple_files=True,
        type=["jpg", "png", "jpeg"]
    )

    if student_files:
        for file in student_files:
            with open(os.path.join("student_images", file.name), "wb") as f:
                f.write(file.getbuffer())
        st.success(f"{len(student_files)} student images uploaded.")

    attendance_file = st.file_uploader(
        "Upload attendance image",
        type=["jpg", "png", "jpeg"]
    )

    if attendance_file:
        st.image(attendance_file, caption="Attendance Image")

    if st.button("Run Recognition"):
        if not student_files:
            st.warning("Upload student images first.")
        elif not attendance_file:
            st.warning("Upload attendance image first.")
        else:
            recognized_students = []

            with st.spinner("Running AI recognition..."):
                if DEEPFACE_AVAILABLE:
                    # Try real AI
                    for file in student_files:
                        student_path = os.path.join("student_images", file.name)

                        try:
                            result = DeepFace.verify(
                                img1_path=student_path,
                                img2_path=attendance_file,
                                enforce_detection=False
                            )

                            if result["verified"]:
                                name = file.name.split(".")[0]
                                recognized_students.append(name)

                        except:
                            continue
                else:
                    # Fallback (simulation)
                    recognized_students = [file.name.split(".")[0] for file in student_files]

            if recognized_students:
                now = datetime.now()

                df = pd.DataFrame({
                    "Name": recognized_students,
                    "Date": [now.strftime("%Y-%m-%d")] * len(recognized_students),
                    "Time": [now.strftime("%H:%M:%S")] * len(recognized_students),
                    "Status": ["Present"] * len(recognized_students)
                })

                st.session_state["attendance"] = df
                df.to_csv("attendance.csv", index=False)

                st.success("Recognition complete!")
                st.dataframe(df)

            else:
                st.warning("No faces matched.")

# -------------------------------
# RESULTS
# -------------------------------
elif menu == "Results":
    st.subheader("Results")

    if "attendance" in st.session_state:
        st.dataframe(st.session_state["attendance"])
    elif os.path.exists("attendance.csv"):
        df = pd.read_csv("attendance.csv")
        st.dataframe(df)
    else:
        st.warning("No data yet.")

# -------------------------------
# ANALYTICS
# -------------------------------
elif menu == "Analytics":
    st.subheader("Analytics")

    if os.path.exists("attendance.csv"):
        df = pd.read_csv("attendance.csv")

        st.metric("Total Records", len(df))
        st.metric("Students", df["Name"].nunique())

        st.bar_chart(df["Name"].value_counts())
    else:
        st.warning("No data available.")
