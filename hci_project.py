import streamlit as st
import pandas as pd
import time
import os
import csv
import plotly.express as px

# Create a folder called data in the main project folder
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASKS_CSV = os.path.join(DATA_FOLDER, "tasks_data.csv")
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
            Before continuing, please confirm that you meet **all** the following criteria and agree to participate:
            
            - I am 18 years of age or older.  
            - I am not currently studying or working in Computer Science, IT, or any related field.  
            - I have no prior knowledge or experience with this web application.  
            
            I understand that this usability testing session is being conducted for academic and research purposes.  
            I voluntarily agree to participate and understand that I will be asked to complete specific tasks as part of this study.
            
            The data collected during this session—including task performance, feedback, and demographic information—will be used solely to evaluate and improve the usability of apps.
            
            All data will be kept confidential and will not be used for any purpose other than academic research and product improvement.
            
            I understand that my participation is voluntary and that I may withdraw at any time without any consequences.
            """)
        consent_given = st.checkbox("I agree to the above terms and consent to participate.")
        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree to the consent terms before proceeding.")
            else:
                st.success("Consent Submitted.")
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
                st.success("Demographics Submitted.")
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

        st.write("Please enter your name and select a task and record your experience completing it.")
        name = st.text_input(
            "Name",
            placeholder="Enter your name"
        )
        # For this template, we assume there's only one task, in project 3, we will have to include the actual tasks
        selected_task = st.selectbox("Select Task", ["Task 1: Astronomy Picture of the Day", "Task 2: Kepler Space Telescope", "Task 3: Space Quiz"])
        
        if selected_task == "Task 1: Astronomy Picture of the Day":
            st.write("""
                ### Task Description: Astronomy Picture of the Day (APOD)
                
                Navigate through the app to find the **Astronomy Picture of the Day** section.
                
                Please complete the following steps:
                
                1. View yesterday’s APOD.
                2. Use the date selection feature to find and view the APOD from your birthday last year.
                3. Examine the image and description shown for that date.
                """)

            # Track success, completion time, etc.
            st.write("### Start the task timer now.\nWhen you have completed the task, stop the timer and answer the questions below.")
            # Start/stop task timer
            start_button = st.button("Start Task Timer")
            if start_button:
                st.success("Timer Started.")
                st.session_state["start_time"] = time.time()

            stop_button = st.button("Stop Task Timer")
            if stop_button and "start_time" in st.session_state:
                duration = time.time() - st.session_state["start_time"]
                st.session_state["task_duration"] = duration
                st.success(f"Task completed in {duration:.2f} seconds.")

            success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partially"])

            step_one = st.text_area(
                "What was the title or content of yesterday’s APOD?",
                placeholder="e.g., 'Star Trails over Mauna Kea'"
            )

            step_two = st.text_area(
                "What did you see for the APOD from your birthday last year?",
                placeholder="e.g., 'A nebula image with a detailed description of its formation'"
            )

            step_three = st.text_area(
                "Did the image and description display correctly and make sense?",
                placeholder="e.g., 'Yes, everything loaded properly and the explanation was clear."
            )

            feedback = st.text_area(
                "Was the APOD section easy to find? Was the date selector intuitive? Did anything "
                "cause confusion or seem difficult to use? Please share any suggestions for improvement.",
                placeholder="e.g., 'It took a while to find the section, and the date picker was not obvious on mobile.'"
            )

            if st.button("Save Task Results"):

                st.success("Task Results Saved.")
                duration_val = st.session_state.get("task_duration", None)

                data_dict = {
                    "name": name,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "task_name": selected_task,
                    "success": success,
                    "duration_seconds": duration_val if duration_val else "",
                    "step_one": step_one,
                    "step_two": step_two,
                    "step_three": step_three,
                    "feedback": feedback,
                }

                save_to_csv(data_dict, TASKS_CSV)

                # Reset any stored time in session_state if you'd like
                if "start_time" in st.session_state:
                    del st.session_state["start_time"]
                if "task_duration" in st.session_state:
                    del st.session_state["task_duration"]
        elif selected_task == "Task 2: Kepler Space Telescope":
            st.write("""
                ### Task Description: Kepler Space Telescope Exploration
                
                Navigate to the **Exoplanet Discovery** section and explore the interactive charts showing planet discoveries.
                
                Please complete the following tasks:
                
                1. Use the dropdown menu to select Kepler from the telescope list and examine the interactive table.
                2. Review the Kepler discovery chart and compare it with the total planet discovery chart.
                3. Reflect on the data shown and Kepler's contribution to exoplanet science.
                """)

            st.write("### Start the task timer now.\nWhen you have completed the task, stop the timer and answer the questions below.")
            # Start/stop task timer
            start_button = st.button("Start Task Timer")
            if start_button:
                st.success("Timer Started.")
                st.session_state["start_time"] = time.time()

            stop_button = st.button("Stop Task Timer")
            if stop_button and "start_time" in st.session_state:
                duration = time.time() - st.session_state["start_time"]
                st.session_state["task_duration"] = duration
                st.success(f"Task completed in {duration:.2f} seconds.")

            # User response fields
            success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partially"])
            step_one = st.text_area(
                "Approximately how many planets did Kepler discover in 2025?",
                placeholder="e.g., 130 planets"
            )

            step_two = st.text_area(
                "Did you observe any similarities between Kepler’s chart and the overall discovery chart?",
                placeholder="e.g., Did both charts have similar peaks? Did they have any trending data between years?"
            )

            step_three = st.text_area(
                "Did the charts help you understand Kepler’s impact on planet discovery? Why or why not?",
                placeholder="e.g., Yes — it was clear that Kepler discovered a large portion of planets."
            )

            feedback = st.text_area(
                "Was the dropdown easy to use? Were the charts and table intuitive and understandable? Please "
                "share any confusion or suggestions for improvement.",
                placeholder="e.g., I found the dropdown a bit small on mobile and the chart labels were hard to read."
            )

            if st.button("Save Task Results"):
                st.success("Task Results Saved.")
                duration_val = st.session_state.get("task_duration", None)

                data_dict = {
                    "name": name,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "task_name": selected_task,
                    "success": success,
                    "duration_seconds": duration_val if duration_val else "",
                    "step_one": step_one,
                    "step_two": step_two,
                    "step_three": step_three,
                    "feedback": feedback,
                }

                save_to_csv(data_dict, TASKS_CSV)

                # Reset any stored time in session_state if you'd like
                if "start_time" in st.session_state:
                    del st.session_state["start_time"]
                if "task_duration" in st.session_state:
                    del st.session_state["task_duration"]
        else:
            st.write("""
                ### Task Description: Space Quiz

                Navigate to the **Space Quiz** section of the app.
                
                Please complete the following steps:
                
                1. Enter your name.
                2. Answer all quiz questions.
                3. View your final score.
                """)
            # Track success, completion time, etc.
            st.write("### Start the task timer now.\nWhen you have completed the task, stop the timer and answer the questions below.")
            # Start/stop task timer
            start_button = st.button("Start Task Timer")
            if start_button:
                st.success("Timer Started.")
                st.session_state["start_time"] = time.time()

            stop_button = st.button("Stop Task Timer")
            if stop_button and "start_time" in st.session_state:
                duration = time.time() - st.session_state["start_time"]
                st.session_state["task_duration"] = duration
                st.success(f"Task completed in {duration:.2f} seconds.")

            success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partially"])

            step_one = st.text_area(
                "What name did you enter?",
                placeholder="e.g., John Smith"
            )

            step_two = st.text_area(
                "Describe your experience answering the quiz questions.",
                placeholder="e.g., Most of the questions were too difficult to understand."
            )

            step_three = st.text_area(
                "What was your final score?",
                placeholder="e.g., 1 out of 3"
            )

            feedback = st.text_area(
                "Was it clear how to start and complete the quiz? Did you understand when the quiz ended and how your "
                "score was presented? Were there any confusing elements or areas for improvement?",
                placeholder="e.g., It was easy to start the quiz, but the questions were confusing."
            )

            if st.button("Save Task Results"):

                st.success("Task Results Saved.")
                duration_val = st.session_state.get("task_duration", None)

                data_dict = {
                    "name": name,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "task_name": selected_task,
                    "success": success,
                    "duration_seconds": duration_val if duration_val else "",
                    "step_one": step_one,
                    "step_two": step_two,
                    "step_three": step_three,
                    "feedback": feedback,
                }

                save_to_csv(data_dict, TASKS_CSV)

                # Reset any stored time in session_state if you'd like
                if "start_time" in st.session_state:
                    del st.session_state["start_time"]
                if "task_duration" in st.session_state:
                    del st.session_state["task_duration"]

    with exit_tab:
        st.header("Exit Questionnaire")

        with st.form("exit_form"):
            satisfaction = st.slider("On a scale from 0 to 5, where 0 is very unsatisfied and 5 is"
                                     " very satisfied, how satisfied were you with "
                                     "the overall experience using the product? ", 0, 5)
            design = st.text_input("Was there anything about the design that you found confusing?")
            difficulty = st.slider("On a scale from 0 to 5, where 0 is easy and 5 is difficult "
                                   ", how complex was it to complete these tasks?", 0, 5)
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
        task_df = load_from_csv(TASKS_CSV)
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
            filtered_task_one = task_df[task_df["task_name"] == "Task 1: Astronomy Picture of the Day"]
            avg_task_one_duration = filtered_task_one["duration_seconds"].mean()
            filtered_task_two = task_df[task_df["task_name"] == "Task 2: Kepler Space Telescope"]
            avg_task_two_duration = filtered_task_two["duration_seconds"].mean()
            filtered_task_three = task_df[task_df["task_name"] == "Task 3: Space Quiz"]
            avg_task_three_duration = filtered_task_three["duration_seconds"].mean()

            st.write(f"**Average Satisfaction**: {avg_satisfaction:.2f}")
            st.write(f"**Average Difficulty**: {avg_difficulty:.2f}")
            st.write(f"**Average Confidence**: {avg_confidence:.2f}")
            st.write(f"**Average Task Duration - Task One**: {avg_task_one_duration:.2f} Second(s)")
            st.write(f"**Average Task Duration - Task Two**: {avg_task_two_duration:.2f} Second(s)")
            st.write(f"**Average Task Duration - Task Three**: {avg_task_three_duration:.2f} Second(s)")

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
            familiarity_counts = demographic_df["familiarity"].value_counts()
            task_success_counts = task_df["success"].value_counts()

            task_df["success_numeric"] = task_df["success"].map({"Yes": 1, "Partially": 0.5, "No": 0})

            summary_df = task_df.groupby("task_name").agg(
                success_rate=("success_numeric", lambda x: round((x.sum() / len(x)) * 100, 1)),
                avg_time_sec=("duration_seconds", "mean"),
                num_participants=("success", "count")
            ).reset_index()

            # Format nicely
            summary_df.columns = ["Task", "Success Rate (%)", "Avg. Completion Time (sec)", "Participants"]
            st.write("### Task Success Rates and Average Completion Times")
            st.dataframe(
                summary_df.style.format({"Success Rate (%)": "{:.1f}", "Avg. Completion Time (sec)": "{:.1f}"}))


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
            - **Familiarity Distribution** displays the distribution of familiarity across participants.
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

            #familiarity pie chart
            fig_familiarity_counts = px.pie(familiarity_counts,
                                          names=familiarity_counts.index,
                                          values=familiarity_counts.values,
                                          title='Familiarity Distribution')
            st.plotly_chart(fig_familiarity_counts, use_container_width=True)



            st.subheader("Task Performance Distribution")
            st.write("""
            The following visualizations provide a breakdown of task completion outcomes and how these vary by education level.

            - **Task Success Distribution** displays the overall percentages of successful, partially successful, and unsuccessful task completions.
            - **Task Success by Education Level** shows how task completion rates differ across education levels.
            """)

            # task success pie chart total
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
                                              labels={'value':'Average Difficulty (0 = Not Difficult, 5 = Very Difficult', 'age': 'Age Range'},
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
