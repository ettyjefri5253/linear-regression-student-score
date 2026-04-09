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

# ================== LOAD MODEL ( SLR - PICKLE) ==================
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
st.sidebar.title("⚙️ Navigation")
mode = st.sidebar.selectbox(
    "Go to",
    ["🏠 Home", "🎓 Student", "👨‍🏫 Teacher", "🔢 Calculator"]
)

st.sidebar.markdown("---")
st.sidebar.info("⚠️ Note: This is a model-based estimate and may not be exact.")

# ================== HEADER ==================
col1, col2 = st.columns([1, 8])

with col1:
    st.image("statistics.png", width=80)

with col2:
    st.markdown("## Student ScoreCast")
    st.caption("Better insights. Better outcomes.")

# =========================================================
# 🏠 HOME PAGE
# =========================================================
if mode == "🏠 Home":
    st.title("👋 Welcome")

    st.write("""
    This app helps students and teachers:
    
    - 📊 Predict academic performance  
    - 📈 Visualize study impact  
    - 🧑‍🏫 Analyze class data (Teacher Mode)  
    - 🔢 Perform quick calculations  
    
    👈 Use the sidebar to navigate between features.
    """)

    st.markdown(
    "<p style='color: #A3A32E; font-style: italic;'> 🚀 More features coming soon...</p>",
    unsafe_allow_html=True
)
# =========================================================
# 🎓 STUDENT PAGE
# =========================================================
elif mode == "🎓 Student":
    st.title("🎓 Student Dashboard")
# =========================================================

    col1, col2 = st.columns(2)

    with col1:
        hours = st.slider(
            "Hours Studied",
            1.0,
            10.0,
            5.0,
            step=0.5
        )

    with col2:
        st.write("")  # adds a bit of spacing
        show_graph = st.toggle("Show Graph")
# ------------------------------------------------------------------------------
    x = np.array([hours]).reshape(-1, 1)
    prediction = model.predict(x)[0]

    st.subheader("🎯 Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Estimated Score", f"{prediction:.1f}")

    with col2:
        if prediction >= 90:
            level = "🌟 Excellent"
        elif prediction >= 70:
            level = "👍 Good"
        elif prediction >= 50:
            level = "⚠️ Needs Improvement"
        else:
            level = "❗ At Risk"

        st.metric("Performance", level)

    # Data Tracking / session history
    st.subheader("📁 Session History")

    if "history" not in st.session_state:
        st.session_state.history = []

    if st.button("💾 Save Result"):
        st.session_state.history.append({
            "Hours": hours,
            "Predicted Score": round(prediction, 1)
        })

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)

    # Recommendations
    st.subheader("📚 Recommendations")

    if hours < 3:
        st.warning("Increase study time to improve performance.")
    elif hours < 6:
        st.info("You're on track. A bit more effort can help.")
    else:
        st.success("Great job! Keep it up.")

    # Graph
    if show_graph:
        x_vals = np.linspace(1, 10, 100).reshape(-1, 1)
        y_vals = model.predict(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)
        ax.scatter(hours, prediction)
        ax.set_xlabel("Hours")
        ax.set_ylabel("Score")

        st.pyplot(fig)

# ==================================================================================================================
# 👨‍🏫 TEACHER PAGE
# ==================================================================================================================
elif mode == "👨‍🏫 Teacher":
    st.title("👨‍🏫 Teacher Dashboard")

# ================== QUICK STUDENT CHECK ==================
    st.subheader("⚡ Quick Student Check")

    col1, col2 = st.columns(2)

    with col1:
        t_hours = st.slider("Hours Studied", 1.0, 10.0, 5.0, step=0.5, key="teacher_hours")

    with col2:
        pass_mark = st.number_input("Pass Mark", 0, 100, 50)

    t_x = np.array([t_hours]).reshape(-1, 1)
    t_prediction = model.predict(t_x)[0]

    st.subheader("🎯 Quick Result")

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Estimated Score", f"{t_prediction:.1f}")

    with col4:
        t_level = "Pass" if t_prediction >= pass_mark else "Fail"
        st.metric("Estimated Grade", t_level)

# ================== TEACHER INSIGHT ==================
    st.subheader("📚 Teacher Insight")

    if t_prediction >= pass_mark + 20:
        st.success("Student is performing excellently.")
    elif t_prediction >= pass_mark:
        st.info("Student is passing. Encourage consistency.")
    else:
        st.error("Student is below pass mark. Intervention needed.")

# ================== SAVE ==================
    if "teacher_history" not in st.session_state:
        st.session_state.teacher_history = []

    if st.button("💾 Save Quick Result"):
        st.session_state.teacher_history.append({
            "Hours": t_hours,
            "Predicted Score": round(t_prediction, 1)
        })

    if st.session_state.teacher_history:
        st.dataframe(pd.DataFrame(st.session_state.teacher_history))

# ================== DIVIDER ==================
    st.markdown("---")

# ================== UPLOAD ==================
    st.subheader("📂 Upload Student Data")

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.markdown("""
        **Required Column**
        - Hours
        """)

    with col_info2:
        st.markdown("""
        **Optional**
        - Student Name  
        - Actual Score
        """)

    colA, colB = st.columns([1, 2])

    with colA:
        sample_df = pd.DataFrame({
            "Student Name": ["Alice", "Bob"],
            "Hours": [4, 6],
            "Actual Score": [60, 80]
        })

        st.download_button("📥 Sample CSV", sample_df.to_csv(index=False), "sample.csv")

    with colB:
        uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx", "xls"])

# ================== PROCESS ==================
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df.columns = df.columns.str.strip()

        if "Hours" in df.columns:
            df = df.sort_values("Hours")

            X = df["Hours"].values.reshape(-1, 1)
            df["Predicted Score"] = model.predict(X).round(1)

# ================== LOGIC ==================
            # At Risk based on pass mark
            if "Actual Score" in df.columns:
                df["At Risk"] = df["Actual Score"] < pass_mark
                df["Error"] = (df["Actual Score"] - df["Predicted Score"]).round(1)
            else:
                df["At Risk"] = df["Predicted Score"] < pass_mark

# ================== SUMMARY ==================
            st.subheader("📊 Class Summary")

            # 🔹 Predicted Summary
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Pred Avg", f"{df['Predicted Score'].mean():.1f}")
            col2.metric("Pred Max", f"{df['Predicted Score'].max():.1f}")
            col3.metric("Pred Min", f"{df['Predicted Score'].min():.1f}")
            col4.metric("Pass Rate", f"{(df['Predicted Score'] >= pass_mark).mean()*100:.0f}%")

            # 🔹 If actual exists → show comparison
            if "Actual Score" in df.columns:
                st.markdown("### 📊 Actual Performance")

                col5, col6, col7 = st.columns(3)

                col5.metric("Actual Avg", f"{df['Actual Score'].mean():.1f}")
                col6.metric("Actual Max", f"{df['Actual Score'].max():.1f}")
                col7.metric("Actual Min", f"{df['Actual Score'].min():.1f}")
# ================== TABLE ==================
            st.subheader("📋 Predictions")
            st.dataframe(df, use_container_width=True)

            st.caption("🟠 Predicted = Model Output | 🔵 Actual = Real Scores")

# ================== ALERT ==================
            low_students = df[df["At Risk"]]

            if not low_students.empty:
                st.warning("⚠️ Students below pass mark:")
                st.dataframe(low_students)

# ================== GRAPH ==================
            st.subheader("📈 Regression Analysis")

            fig, ax = plt.subplots()

            if "Actual Score" in df.columns:
                ax.scatter(df["Hours"], df["Actual Score"], label="Actual")
                ax.scatter(df["Hours"], df["Predicted Score"], label="Predicted")
            else:
                ax.scatter(df["Hours"], df["Predicted Score"], label="Predicted")

            x_vals = np.linspace(df["Hours"].min(), df["Hours"].max(), 100).reshape(-1, 1)
            y_vals = model.predict(x_vals)

            ax.plot(x_vals, y_vals, label="Regression Line")

            ax.set_xlabel("Hours")
            ax.set_ylabel("Score")
            ax.legend()

            st.pyplot(fig)

# ================== DOWNLOAD ==================
            csv = df.to_csv(index=False).encode("utf-8")

            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)

            col1, col2 = st.columns(2)

            with col1:
                st.download_button("📄 CSV", csv, "predictions.csv")

            with col2:
                st.download_button("📊 Excel", output.getvalue(), "predictions.xlsx")

        else:
            st.error("File must contain 'Hours' column")

# =========================================================
# 🔢              SIMPLE CALCULATOR MENU
# =========================================================
elif mode == "🔢 Calculator":
    st.title("🔢 Quick Calculator")

    num1 = st.number_input("Enter first number")
    num2 = st.number_input("Enter second number")

    operation = st.selectbox("Operation", ["+", "-", "×", "÷"])

    if st.button("Calculate"):
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "×":
            result = num1 * num2
        elif operation == "÷":
            if num2 != 0:
                result = num1 / num2
            else:
                st.error("Cannot divide by zero")
                result = None

        if result is not None:
            st.success(f"Result: {result}")


# ================== FOOTER ==================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 0.9rem; color: gray;'>"
    "• Predict student performance and explore insights •"
    "</p>",
    unsafe_allow_html=True
)
