import streamlit as st
import pandas as pd
import altair as alt
import speech_recognition as sr
from st_audiorec import st_audiorec
import io

# Global DataFrame
df = pd.DataFrame()

# Page configuration
st.set_page_config(
    page_title="Voice-Controlled CSV Graph Renderer",
    page_icon="🎙️",
    layout="wide",
)

# Main Title of the App
st.title("🎙️ Voice-Controlled Graph Renderer")

# CSS for custom styles
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stAudio {
        display: none; /* Hide the extra audio widget */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for file upload
st.sidebar.header("📁 File Upload")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"])

# Function to process audio
def process_audio(wav_audio_data):
    recognizer = sr.Recognizer()
    # Wrap binary audio data in a BytesIO object
    audio_file = io.BytesIO(wav_audio_data)
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            command = recognizer.recognize_google(audio)
            st.success(f"🎙️ Recognized command: {command}")
            return command.lower()
        except sr.UnknownValueError:
            st.error("⚠️ Could not understand the audio. Please speak clearly.")
        except sr.RequestError as e:
            st.error(f"⚠️ Speech recognition service error: {e}")
        except Exception as ex:
            st.error(f"⚠️ An error occurred: {ex}")
    return None

# Function to create Line chart
def create_line_chart():
    x_axis = df.columns[0]
    y_axis = df.select_dtypes(include=["number"]).columns[0]
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(x_axis, title=x_axis),
            y=alt.Y(y_axis, title=y_axis),
            tooltip=[x_axis, y_axis],
        )
        .properties(width=700, height=400, title=f"📊 Line Chart of {y_axis} over {x_axis}")
    )
    return chart

# Function to create Bar chart
def create_bar_chart():
    x_axis = df.columns[0]
    y_axis = df.select_dtypes(include=["number"]).columns[0]
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(x_axis, title=x_axis),
            y=alt.Y(y_axis, title=y_axis),
            tooltip=[x_axis, y_axis],
        )
        .properties(width=700, height=400, title=f"📊 Bar Chart of {y_axis} over {x_axis}")
    )
    return chart

# Function to create Pie chart
def create_pie_chart():
    x_axis = df.columns[0]
    y_axis = df.select_dtypes(include=["number"]).columns[0]
    chart = (
        alt.Chart(df)
        .mark_arc()
        .encode(
            theta=alt.Theta(y_axis, title=y_axis),
            color=alt.Color(x_axis, title=x_axis),
            tooltip=[x_axis, y_axis],
        )
        .properties(width=400, height=400, title=f"📊 Pie Chart of {y_axis} by {x_axis}")
    )
    return chart

# Main app layout
if uploaded_file is not None:
    st.sidebar.success(f"📄 File uploaded: {uploaded_file.name}")
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        st.subheader("📂 Uploaded CSV Content")
        st.write(df)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        st.subheader("📂 Uploaded XLSX Content")
        st.write(df)

    # Initialize session state for graphs if not yet initialized
    if "graphs" not in st.session_state:
        st.session_state["graphs"] = []

    st.markdown("### 🎤 Voice Command Options")
    st.info("🔊 Record your voice and give commands like 'line chart', 'bar chart', or 'pie chart'.")

    # Audio Recorder Widget
    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        st.audio(wav_audio_data, format="audio/wav")  # Play the recorded audio
        command = process_audio(wav_audio_data)
        if command:
            if "line chart" in command:
                st.session_state["graphs"].append(create_line_chart())
            elif "bar chart" in command:
                st.session_state["graphs"].append(create_bar_chart())
            elif "pie chart" in command:
                st.session_state["graphs"].append(create_pie_chart())
            else:
                st.warning("⚠️ Command not recognized. Try saying 'line chart', 'bar chart', or 'pie chart'.")

    # Display all graphs from session state side by side
    if len(st.session_state["graphs"]) > 0:
        st.markdown("### 📊 Rendered Graphs")
        # Create columns based on the number of graphs
        columns = st.columns(len(st.session_state["graphs"]))
        for idx, graph in enumerate(st.session_state["graphs"]):
            columns[idx].altair_chart(graph, use_container_width=True)

else:
    st.sidebar.warning("⚠️ Please upload a CSV or Excel file to proceed.")

st.markdown("---")
st.markdown("🛠️ Developed by [Jaswin Singh Dang](https://yourwebsite.com) • Powered by [Streamlit](https://streamlit.io)")
