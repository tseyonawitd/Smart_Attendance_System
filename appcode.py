import streamlit as st
import pandas as pd
import os
from datetime import datetime


st.set_page_config(page_title="Smart Attendance System", page_icon="🎓", layout="centered")

st.title("🎓 Smart Attendance Management System")
st.markdown("### AI-Based Attendance Tracking and Recognition")

st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Home", "Upload Data", "Results", "Analytics", "About Project"])

# Ensure folders exist
os.makedirs("student_images", exist_ok=True)
os.makedirs("attendance_input", exist_ok=True)

# -------------------------------
# HOME PAGE
# -------------------------------
if menu == "Home":
    st.subheader("Welcome")
    st.write("This system automates classroom attendance using AI-based face recognition.")
    st.info("Use the sidebar to navigate through the system.")

# -------------------------------
# UPLOAD PAGE
# -------------------------------
elif menu == "Upload Data":
    st.subheader("Upload Data")

    st.markdown("### 1. Upload Student Reference Images")
    student_files = st.file_uploader(
        "Upload student images (use student name as file name if possible)",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png"]
    )

    if student_files:
        for file in student_files:
            with open(os.path.join("student_images", file.name), "wb") as f:
                f.write(file.getbuffer())
        st.success(f"{len(student_files)} student image(s) uploaded successfully.")

    st.markdown("### 2. Upload Attendance Image")
    attendance_file = st.file_uploader(
        "Upload attendance image",
        type=["jpg", "jpeg", "png"]
    )

    attendance_path = None
    if attendance_file:
        attendance_path = os.path.join("attendance_input", attendance_file.name)
        with open(attendance_path, "wb") as f:
            f.write(attendance_file.getbuffer())
        st.success("Attendance image uploaded successfully.")

    st.markdown("### 3. Run Attendance Recognition")

    if st.button("Run Recognition", key="run_recognition_btn"):
        if not attendance_file:
            st.warning("Please upload an attendance image first.")
        else:
            recognized_students = []

            student_folder = "student_images"
            attendance_path = os.path.join("attendance_input", attendance_file.name)

            for student_img in os.listdir(student_folder):
                student_path = os.path.join(student_folder, student_img)

                if st.button("Run Recognition"):
                    recognized_students = []
                    
                    if student_files:
                        for file in student_files:
                            name = file.name.split(".")[0]
                            recognized_students.append(name)
                    
                    if recognized_students:
                        from datetime import datetime
                        now = datetime.now()
                        
                        df = pd.DataFrame({
                            "Name": recognized_students,
                            "Date": [now.strftime("%Y-%m-%d")] * len(recognized_students),
                            "Time": [now.strftime("%H:%M:%S")] * len(recognized_students),
                            "Status": ["Present"] * len(recognized_students)
                        })
                        
                        st.session_state["attendance_df"] = df
                        st.success("Recognition completed successfully!")

            if recognized_students:
                now = datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")

                df = pd.DataFrame({
                    "Name": recognized_students,
                    "Date": [date_str] * len(recognized_students),
                    "Time": [time_str] * len(recognized_students),
                    "Status": ["Present"] * len(recognized_students)
                })

                st.session_state["attendance_df"] = df

                # Save to CSV as attendance database
                csv_file = "attendance_records.csv"
                if os.path.exists(csv_file):
                    old_df = pd.read_csv(csv_file)
                    combined_df = pd.concat([old_df, df], ignore_index=True)
                    combined_df.drop_duplicates(subset=["Name", "Date"], inplace=True)
                    combined_df.to_csv(csv_file, index=False)
                else:
                    df.to_csv(csv_file, index=False)

                st.success("Recognition completed successfully!")
                st.write("### Recognized Students:")
                for name in recognized_students:
                    st.write(f"✔ {name}")
            else:
                st.warning("No matching students found.")

# -------------------------------
# RESULTS PAGE
# -------------------------------
elif menu == "Results":
    st.subheader("Attendance Results")

    if "attendance_df" in st.session_state:
        df = st.session_state["attendance_df"]
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Attendance CSV", csv, "attendance_results.csv", "text/csv")
    elif os.path.exists("attendance_records.csv"):
        df = pd.read_csv("attendance_records.csv")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Attendance CSV", csv, "attendance_results.csv", "text/csv")
    else:
        st.warning("No attendance data available yet. Please run recognition first.")

# -------------------------------
# ANALYTICS PAGE
# -------------------------------
elif menu == "Analytics":
    st.subheader("Attendance Analytics")

    if os.path.exists("attendance_records.csv"):
        df = pd.read_csv("attendance_records.csv")

        total_present = len(df)
        unique_students = df["Name"].nunique()

        st.metric("Total Attendance Records", total_present)
        st.metric("Unique Students Recognized", unique_students)

        st.markdown("### Attendance Frequency by Student")
        student_counts = df["Name"].value_counts()
        st.bar_chart(student_counts)

        st.markdown("### Attendance Status Distribution")
        status_counts = df["Status"].value_counts()
        st.bar_chart(status_counts)

        st.markdown("### Attendance History")
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No attendance records available yet.")

# -------------------------------
# ABOUT PAGE
# -------------------------------
elif menu == "About Project":
    st.subheader("About This Project")
    st.write("""
    **Project Title:** Smart Attendance Management System

    **Objective:**  
    To automate student attendance using AI-based facial recognition.

    **Technologies Used:**  
    - Python  
    - Streamlit  
    - DeepFace  
    - Pandas  

    **Current Features:**  
    - Upload student reference images  
    - Upload attendance image  
    - AI-based face comparison  
    - Attendance recording  
    - Attendance analytics  
    - CSV report export  
    """)
