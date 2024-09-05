import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# Load the trained model for student performance analysis
with open('student_performance_model.pkl', 'rb') as file:
    model = pickle.load(file)

st.title("Student Performance Analysis")
st.sidebar.header("Student Data Input")

# Video resources dictionary with links
video_resources = {
    'Mathematics': 'https://www.youtube.com/playlist?list=PLB6MUoMXv9xcGOPDraWI707O7Zj5qVrDW',
    'Physics': 'https://www.youtube.com/playlist?list=PLTYLC3XcJGZ5D3ohTYfOIR39L-H69f9Ca',
    'Computer Science': 'https://www.youtube.com/c/ComputerScienceLessons/playlists',
    'Electronics': 'https://www.youtube.com/watch?v=CeD2L6KbtVM&list=PL803563859BF7ED8C',
    'Mechanical Engineering': 'https://www.youtube.com/playlist?list=PLyqSpQzTE6M_MEUdn1izTMB2yZgP1NLfs',
    'Electrical Engineering': 'https://www.youtube.com/playlist?list=PL425060D3C78350E1',
    'Chemistry': 'https://www.youtube.com/watch?v=XL2IqiImLO4&list=PLwdnzlV3ogoXpDif2e93GJKoojj0SgvV0',
}

def user_input_features():
    mathematics_quiz = st.sidebar.number_input('Mathematics Quiz Score', min_value=0, max_value=100)
    physics_quiz = st.sidebar.number_input('Physics Quiz Score', min_value=0, max_value=100)
    cs_quiz = st.sidebar.number_input('Computer Science Quiz Score', min_value=0, max_value=100)
    electronics_quiz = st.sidebar.number_input('Electronics Quiz Score', min_value=0, max_value=100)
    mech_eng_quiz = st.sidebar.number_input('Mechanical Engineering Quiz Score', min_value=0, max_value=100)
    elec_eng_quiz = st.sidebar.number_input('Electrical Engineering Quiz Score', min_value=0, max_value=100)
    chemistry_quiz = st.sidebar.number_input('Chemistry Quiz Score', min_value=0, max_value=100)

    mathematics_exam = st.sidebar.number_input('Mathematics Exam Score', min_value=0, max_value=100)
    physics_exam = st.sidebar.number_input('Physics Exam Score', min_value=0, max_value=100)
    cs_exam = st.sidebar.number_input('Computer Science Exam Score', min_value=0, max_value=100)
    electronics_exam = st.sidebar.number_input('Electronics Exam Score', min_value=0, max_value=100)
    mech_eng_exam = st.sidebar.number_input('Mechanical Engineering Exam Score', min_value=0, max_value=100)
    elec_eng_exam = st.sidebar.number_input('Electrical Engineering Exam Score', min_value=0, max_value=100)
    chemistry_exam = st.sidebar.number_input('Chemistry Exam Score', min_value=0, max_value=100)
    
    grade = st.sidebar.selectbox('Grade', [1, 2, 3, 4])

    data = {
        'Mathematics_QuizScore': mathematics_quiz,
        'Physics_QuizScore': physics_quiz,
        'Computer Science_QuizScore': cs_quiz,
        'Electronics_QuizScore': electronics_quiz,
        'Mechanical Engineering_QuizScore': mech_eng_quiz,
        'Electrical Engineering_QuizScore': elec_eng_quiz,
        'Chemistry_QuizScore': chemistry_quiz,
        'Mathematics_ExamScore': mathematics_exam,
        'Physics_ExamScore': physics_exam,
        'Computer Science_ExamScore': cs_exam,
        'Electronics_ExamScore': electronics_exam,
        'Mechanical Engineering_ExamScore': mech_eng_exam,
        'Electrical Engineering_ExamScore': elec_eng_exam,
        'Chemistry_ExamScore': chemistry_exam,
    }
    features = pd.DataFrame(data, index=[0])
    return features

def suggest_resources(prediction):
    weak_topics = []
    for subject, score in prediction.items():
        if score < 60:  # Threshold for weak topics
            weak_topics.append(subject.split('_')[0])

    if weak_topics:
        suggestion = "You need to focus on the following topics:\n"
        suggestion += ', '.join(weak_topics) + ".\n\nHere are some resources:\n"
        for topic in weak_topics:
            suggestion += f"- {topic}: {video_resources.get(topic, 'No resources available')}\n"
        return suggestion
    else:
        return "Keep up the good work! You're doing well in all areas."

def plot_scores(df):
    quiz_scores = df[[col for col in df.columns if 'QuizScore' in col]].melt(var_name='Subject', value_name='Score')
    exam_scores = df[[col for col in df.columns if 'ExamScore' in col]].melt(var_name='Subject', value_name='Score')

    fig1 = px.bar(quiz_scores, x='Subject', y='Score', title="Quiz Scores", labels={'Subject': 'Subjects', 'Score': 'Scores'})
    fig2 = px.bar(exam_scores, x='Subject', y='Score', title="Exam Scores", labels={'Subject': 'Subjects', 'Score': 'Scores'})

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

# Store the chart type in session state
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = 'Bar'

df = user_input_features()

st.subheader("Student Data")
st.write(df)

if st.button('Analyze'):
    prediction = df.iloc[0].to_dict()
    st.subheader("Analysis Result")
    st.write(suggest_resources(prediction))

    st.subheader("Performance Analysis Graphs")
    # Display the chart type selector after clicking "Analyze"
    st.session_state.chart_type = 'Bar'  # Only Bar chart is available
    plot_scores(df)
