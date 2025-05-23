import streamlit as st
import pandas as pd
import time
import os
import plotly.express as px

# Create a folder called data in the main project folder
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")


def save_to_csv(data_dict, csv_file):
    # Convert dict to DataFrame with a single row
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        # If CSV doesn't exist, write with headers
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        # Else, we need to append without writing the header!
        df_new.to_csv(csv_file, mode='a', header=False, index=False)


def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()


def main():
    st.title("Usability Testing Tool")

    home, consent, demographics, tasks, exit_tab, report = st.tabs(
        ["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"])

    with home:
        st.header("Introduction")
        st.write("""
        Welcome to the Usability Testing Tool for HCI.

        In this app, you will:
        1. Provide consent for data collection.
        2. Fill out a short demographic questionnaire.
        3. Perform a specific task (or tasks).
        4. Answer an exit questionnaire about your experience.
        5. View a summary report (for demonstration purposes).
        """)

    with consent:
        st.header("Consent Form")
        st.write("""
        I understand that this usability testing session is being conducted for academic 
        and research purposes. I voluntarily agree to participate and understand that I 
        will be asked to complete specific tasks as a part of this study.

        The data collected during this session - including task performance, feedback, and 
        demographic information - will be used solely to evaluate and improve the usability 
        of apps.

        All data will be kept confidential nd will not be used for any purpose other than 
        academic research and product improvement.

        I understand that my participation is voluntary and that I amy withdraw at any 
        time without any consequences.
        """)
        consent_given = st.checkbox("I agree to the above terms and consent to participate.")
        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree to the consent terms before proceeding.")
            else:
                # Save the consent acceptance time
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_csv(data_dict, CONSENT_CSV)

    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):
            name = st.text_input("Name")
            age = st.radio("Age Range", ["Under 18", "18-24", "25-34", "35-44", "45-54", "55+"])
            gender = st.radio("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
            education = st.radio("Education Level", ["High School or equivalent", "Some College",
                                                     "Associate's Degree", "Bachelor's Degree",
                                                     "Graduate Degree"])
            occupation = st.text_input("Enter your occupation:")
            familiarity = st.radio("How familiar are you with technology?", ["Not familiar",
                                                                             "Somewhat familiar",
                                                                             "Very familiar"])
            accessibility = st.text_input("Are there any accessibility needs we should be aware of?")
            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "education": education,
                    "occupation": occupation,
                    "familiarity": familiarity,
                    "accessibility": accessibility
                }
                save_to_csv(data_dict, DEMOGRAPHIC_CSV)

    with tasks:
        st.header("Task Page")

        st.write("Please select a task and record your experience completing it.")

        # For this template, we assume there's only one task, in project 3, we will have to include the actual tasks
        selected_task = st.selectbox("Select Task", ["Task 1: Example Task"])
        st.write("Task Description: Perform the example task in our system...")

        # Track success, completion time, etc.
        start_button = st.button("Start Task Timer")
        if start_button:
            st.session_state["start_time"] = time.time()

        stop_button = st.button("Stop Task Timer")
        if stop_button and "start_time" in st.session_state:
            duration = time.time() - st.session_state["start_time"]
            st.session_state["task_duration"] = duration

        success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
        notes = st.text_area("Observer Notes")

        if st.button("Save Task Results"):
            duration_val = st.session_state.get("task_duration", None)

            data_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "task_name": selected_task,
                "success": success,
                "duration_seconds": duration_val if duration_val else "",
                "notes": notes
            }
            save_to_csv(data_dict, TASK_CSV)

            # Reset any stored time in session_state if you'd like
            if "start_time" in st.session_state:
                del st.session_state["start_time"]
            if "task_duration" in st.session_state:
                del st.session_state["task_duration"]

    with exit_tab:
        st.header("Exit Questionnaire")

        with st.form("exit_form"):
            satisfaction = st.slider("On a scale from 0 to 5, where 0 is very unsatisfied and 5 is"
                                     "very satisfied, how satisfied were you with "
                                     "the overall experience using the product? ", 0, 5)
            design = st.text_input("Was there anything about the design that you found confusing?")
            difficulty = st.slider("On a scale from 0 to 5, where 0 is very difficult and 5 is not difficult "
                                   "at all, how difficult was it to complete these tasks?", 0, 5)
            confidence = st.slider("On a scale from 0 to 5, where 0 is not confident at all and 5 is "
                                   "very confident, how confident were you in completing these tasks?", 0, 5)
            completion = st.text_input("Was there a task you could not complete? If so, "
                                       "what was the barrier?")
            improvements = st.text_input("Suggestions for improvement")
            open_feedback = st.text_input("Please provide any additional feedback")
            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "satisfaction": satisfaction,
                    "design": design,
                    "difficulty": difficulty,
                    "confidence": confidence,
                    "completion": completion,
                    "improvements": improvements,
                    "open_feedback": open_feedback
                }
                save_to_csv(data_dict, EXIT_CSV)
                st.success("Exit questionnaire data saved.")

    with report:
        st.header("Usability Report - Aggregated Results")

        st.write("**Consent Data**")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        st.write("**Demographic Data**")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
        else:
            st.info("No demographic data available yet.")

        st.write("**Task Performance Data**")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            st.dataframe(task_df)
        else:
            st.info("No task data available yet.")

        st.write("**Exit Questionnaire Data**")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)
        else:
            st.info("No exit questionnaire data available yet.")

        # Example of aggregated stats (for demonstration only)
        if not exit_df.empty:
            st.subheader("Exit Questionnaire Averages")

            avg_satisfaction = exit_df["satisfaction"].mean()
            avg_difficulty = exit_df["difficulty"].mean()
            avg_confidence = exit_df["confidence"].mean()
            avg_task_duration = task_df["duration_seconds"].mean()

            st.write(f"**Average Satisfaction**: {avg_satisfaction:.2f}")
            st.write(f"**Average Difficulty**: {avg_difficulty:.2f}")
            st.write(f"**Average Confidence**: {avg_confidence:.2f}")
            st.write(f"**Average Task Duration**: {avg_task_duration:.2f} Second(s)")

            # Ordering data
            education_order = [
                "High School or equivalent",
                "Some College",
                "Associate's Degree",
                "Bachelor's Degree",
                "Graduate Degree"
            ]

            age_order = [
                "Under 18",
                "18-24",
                "25-34",
                "35-44",
                "45-54",
                "55+"
            ]

            gender_counts = demographic_df["gender"].value_counts()
            age_counts = demographic_df["age"].value_counts().reindex(age_order)
            education_counts = demographic_df["education"].value_counts().reindex(education_order)
            task_success_counts = task_df["success"].value_counts()

            merge_demo_exit = pd.merge(exit_df, demographic_df, left_index=True, right_index=True)
            merge_demo_task = pd.merge(task_df, demographic_df, left_index=True, right_index=True)
            # st.write(merge_demo_exit) # DEBUG
            # st.write(merge_demo_task) # DEBUG
            avg_difficulty_by_age = merge_demo_exit.groupby("age")["difficulty"].mean()
            # st.write(avg_difficulty_by_age) # DEBUG
            avg_confidence_by_gender = merge_demo_exit.groupby("gender")["confidence"].mean()
            # st.write(avg_confidence_by_gender) # DEBUG
            success_by_education = merge_demo_task.groupby("education")["success"].value_counts().unstack(fill_value=0)
            # st.write(success_by_education) # DEBUG

            # Data Visuals in Reports page
            st.subheader("Demographic Distributions")
            st.write("""
            The following visualizations provide an overview of the demographic characteristics of the participants.

            - **Gender Distribution** displays the distribution of genders across participants.
            - **Age Distribution** displays the distribution of ages across participants.
            - **Education Level Distribution** displays the distribution of education levels across participants.
            """)
            # gender distribution pie chart
            fig_gender_counts = px.pie(gender_counts,
                                             names=gender_counts.index,
                                             values=gender_counts.values,
                                             title='Gender Distribution')
            st.plotly_chart(fig_gender_counts, use_container_width=True)

            # age distribution pie chart
            fig_age_counts = px.pie(age_counts,
                                             names=age_counts.index,
                                             values=age_counts.values,
                                             title='Age Distribution')
            st.plotly_chart(fig_age_counts, use_container_width=True)

            # education level pie chart
            fig_education_counts = px.pie(education_counts,
                                          names=education_counts.index,
                                          values=education_counts.values,
                                          title='Education Level Distribution')
            st.plotly_chart(fig_education_counts, use_container_width=True)

            st.subheader("Task Performance Distribution")
            st.write("""
            The following visualizations provide a breakdown of task completion outcomes and how these vary by education level.

            - **Task Success Distribution** displays the overall percentages of successful, partially successful, and unsuccessful task completions.
            - **Task Success by Education Level** shows how task completion rates differ across education levels.
            """)

            # task success pie chart
            fig_task_success_counts = px.pie(task_success_counts,
                                             names=task_success_counts.index,
                                             values=task_success_counts.values,
                                             title='Task Success Distribution')
            st.plotly_chart(fig_task_success_counts, use_container_width=True)

            success_by_education = success_by_education.reindex(education_order)
            # success by education level bar graph
            fig_success_by_education = px.bar(success_by_education,
                                              labels={'value':'Count', 'education': 'Education Level'},
                                              title = "Task Success by Education Level",
                                              barmode ="group")
            st.plotly_chart(fig_success_by_education, use_container_width=True)

            st.subheader("User Experience Metrics by Demographics")
            st.write("""
            The following visualizations break down usability testing feedback by user age and gender.
            They provide insights into how different demographic groups experienced the product:

            - **Average Difficulty by Age** shows how easy or difficult participants of different age ranges found the tasks.
            - **Average Confidence by Gender** indicates how confident each gender group felt while completing the tasks.
            """)

            avg_difficulty_by_age = avg_difficulty_by_age.reindex(age_order)
            # difficulty by age level bar graph
            fig_avg_difficulty_by_age = px.bar(avg_difficulty_by_age,
                                              labels={'value':'Average Difficulty (0 = Very Difficult, 5 = Not Difficult', 'age': 'Age Range'},
                                              title = "Average Difficulty by Age")
            fig_avg_difficulty_by_age.update_layout(showlegend=False)
            st.plotly_chart(fig_avg_difficulty_by_age, use_container_width=True)

            # confidence by gender bar graph
            fig_avg_confidence_by_gender = px.bar(avg_confidence_by_gender,
                                              labels={'value':'Average Confidence (0 = Not Confident, 5 = Very Confident', 'gender': 'Gender'},
                                              title = "Average Confidence by Gender")
            fig_avg_confidence_by_gender.update_layout(showlegend=False)
            st.plotly_chart(fig_avg_confidence_by_gender, use_container_width=True)

if __name__ == "__main__":
    main()
