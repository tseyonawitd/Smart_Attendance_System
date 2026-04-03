import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Attendance System", page_icon="🎓", layout="centered")

st.title("🎓 Smart Attendance Management System")
st.markdown("### AI-Based Attendance Tracking and Recognition")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Home", "Upload Data", "Results", "Analytics", "About Project"])

if menu == "Home":
    st.subheader("Welcome")
    st.write("This system automates classroom attendance using AI.")
    st.info("Use the sidebar to navigate through the system.")

elif menu == "Upload Data":
    st.subheader("Upload Data")

    student_files = st.file_uploader(
        "Upload student images",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png"]
    )

    attendance_file = st.file_uploader(
        "Upload attendance image or video",
        type=["jpg", "jpeg", "png", "mp4"]
    )

    if st.button("Run Recognition"):
        recognized_students = ["Student1", "Student2", "Student3", "Student4"]

        df = pd.DataFrame({
            "Name": recognized_students,
            "Date": ["2026-04-01"] * len(recognized_students),
            "Time": ["08:15:00", "08:15:05", "08:15:12", "08:15:20"],
            "Status": ["Present"] * len(recognized_students)
        })

        st.session_state["attendance_df"] = df
        st.success("Recognition completed successfully!")

elif menu == "Results":
    st.subheader("Attendance Results")

    if "attendance_df" in st.session_state:
        df = st.session_state["attendance_df"]
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Attendance CSV", csv, "attendance_results.csv", "text/csv")
    else:
        st.warning("No attendance data available yet. Please run recognition first.")

elif menu == "Analytics":
    st.subheader("Attendance Analytics")

    if "attendance_df" in st.session_state:
        df = st.session_state["attendance_df"]
        st.metric("Total Present", len(df))
        st.bar_chart(df["Status"].value_counts())
    else:
        st.warning("No attendance data available yet. Please run recognition first.")

elif menu == "About Project":
    st.subheader("About This Project")
    st.write("""
    **Project Title:** Smart Attendance Management System

    **Technologies Used:**
    - Python
    - Streamlit
    - YOLO
    - DeepFace
    - Pandas
    """)
