import streamlit as st
import numpy as np
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

# ================== PAGE CONFIG ==================
icon = Image.open("rating.png")
st.set_page_config(page_title="ScoreCast", page_icon=icon, layout="centered")

# ================== LOAD MODEL ==================
@st.cache_resource
def load_model():
    with open("slr.pkl", "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
except:
    st.error("❌ Model file not found")
    st.stop()

# ================== SIDEBAR ==================
st.sidebar.title("⚙️ Settings")
mode = st.sidebar.selectbox("Select Mode", ["Student", "Teacher"])

st.sidebar.markdown("---")
st.sidebar.info("This app predicts student performance based on study habits.")

# ================== MAIN TITLE ==================
st.title("📊 Student Performance Predictor")

if mode == "Student":
    st.markdown("### 🎓 Student Dashboard")
    st.caption("Enter your study details to estimate your performance.")
else:
    st.markdown("### 👨‍🏫 Teacher Dashboard")
    st.caption("Analyze and predict student performance.")

# ================== INPUT SECTION ==================
st.subheader("📘 Input Details")

col1, col2 = st.columns(2)

with col1:
    hours = st.slider("Hours Studied", 1.0, 10.0, 4.0)

with col2:
    show_graph = st.toggle("Show Prediction Graph", value=True)

# ================== PREDICTION ==================
x = np.array([hours]).reshape(-1, 1)
prediction = model.predict(x)[0]

# ================== RESULT DISPLAY ==================
st.subheader("🎯 Prediction Result")

col3, col4 = st.columns(2)

with col3:
    st.metric("Estimated Score", f"{prediction:.1f}")

with col4:
    if prediction >= 90:
        feedback = "🌟 Excellent"
    elif prediction >= 70:
        feedback = "👍 Good"
    elif prediction >= 50:
        feedback = "⚠️ Needs Improvement"
    else:
        feedback = "❗ At Risk"

    st.metric("Performance Level", feedback)

# ================== STUDY RECOMMENDATIONS ==================
st.subheader("📚 Recommendations")

if mode == "Student":
    if hours < 3:
        st.warning("Increase study time to at least 5–6 hours for better results.")
    elif hours < 6:
        st.info("You're doing okay, but a bit more effort can boost your score.")
    else:
        st.success("Great effort! Keep maintaining your study routine.")

elif mode == "Teacher":
    if prediction >= 90:
        st.success("Student is performing excellently. Consider advanced material.")
    elif prediction >= 70:
        st.info("Student is doing well. Encourage consistency.")
    elif prediction >= 50:
        st.warning("Student needs improvement. Provide additional support.")
    else:
        st.error("Student is at risk. Immediate intervention recommended.")

# ================== GRAPH ==================
if show_graph:
    st.subheader("📈 Prediction Trend")

    x_vals = np.linspace(1, 10, 100).reshape(-1, 1)
    y_vals = model.predict(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.scatter(hours, prediction)
    ax.set_xlabel("Hours Studied")
    ax.set_ylabel("Predicted Score")

    st.pyplot(fig)

# ================== DATA TRACKING ==================
st.subheader("📁 Session History")

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Save Result"):
    st.session_state.history.append({
        "Hours": hours,
        "Predicted Score": round(prediction, 1)
    })

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    # ✅ DOWNLOAD BUTTON (PASTE HERE)
    from io import BytesIO

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='History')

    st.download_button(
        label="📥 Download History as Excel",
        data=output.getvalue(),
        file_name="student_history.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ================== TEACHER MODE ==================
# ================== TEACHER MODE ==================
if mode == "Teacher":
    st.subheader("👨‍🏫 Teacher Dashboard")

    uploaded_file = st.file_uploader(
        "Upload File (CSV or Excel)",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file:
        # ✅ Detect file type
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.caption(f"📄 Loaded file: {uploaded_file.name}")

        # ✅ Validate column
        if "Hours" in df.columns:
            X = df["Hours"].values.reshape(-1, 1)
            df["Predicted Score"] = model.predict(X).round(1)

            st.write("### 📊 Predictions")
            st.dataframe(df, use_container_width=True)

        else:
            st.error("File must contain a 'Hours' column")

# ================== FOOTER ==================
st.markdown("---")
st.caption("⚠️ Predictions are estimates based on trained data and may not be exact.")