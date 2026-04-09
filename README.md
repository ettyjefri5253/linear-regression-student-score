# Student Performance Dashboard

An interactive Streamlit application that uses machine learning to predict and analyze student academic performance based on study hours.

## 🌐 Live Demo

👉 [Open Live App](https://student-scorecast.streamlit.app/)
---
## Features

### Student Dashboard
- Predict scores based on study hours
- Performance feedback and recommendations
- Visualization of prediction trends

### Teacher Dashboard
- Quick single-student prediction
- Upload CSV/Excel for batch analysis
- Regression analysis (actual vs predicted)
- Class summary (average, max, min, pass rate)
- Identify at-risk students
- Download results (CSV / Excel)

### Calculator
- Perform quick calculations
- Basic calculation (e.g. `+ / - *`)

---

## Input Format
Required:
- `Hours`
Optional:
- `Student Name`
- `Actual Score`

## Example

| Student Name | Hours | Actual Score |
|-------------|------|--------------|
| Alice       | 4    | 60           |
| Bob         | 6    | 80           |

---

## Model
- Linear Regression model
- Input: Study hours
- Output: Predicted score

⚠️ Note
- Predictions are estimates based on trained data
- Pass rate threshold is configurable by the user
- Results may vary depending on real-world factors

## Tech Stack
- Python
- Streamlit
- Scikit-learn
- Pandas
- Matplotlib

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run ml2.py
