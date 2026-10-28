import os

import requests
import streamlit as st

# Base URL of the FastAPI backend.
# Override without touching code, e.g.: export API_BASE_URL="http://localhost:8000"
DEFAULT_API_BASE_URL = "http://3.25.131.90:8000"
API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")
PREDICT_URL = f"{API_BASE_URL}/predict"


def extract_prediction(body: dict) -> dict:
    """The deployed API wraps the result in {"response": {...}}; accept both shapes."""
    if isinstance(body, dict) and isinstance(body.get("response"), dict):
        return body["response"]
    return body


def format_error(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text
    return f"API Error {response.status_code} from {PREDICT_URL}: {detail}"


st.title("Insurance Premium Category Predictor")

with st.sidebar:
    st.subheader("Backend")
    st.code(PREDICT_URL, language=None)
    if st.button("Test connection"):
        try:
            health = requests.get(f"{API_BASE_URL}/health", timeout=10)
            if health.status_code == 200:
                st.success("API is reachable")
            else:
                st.warning(f"API returned {health.status_code}")
        except requests.exceptions.RequestException as exc:
            st.error(f"Could not reach the API: {exc}")

st.markdown("Enter your details below: ")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0, step=1.0)
height = st.number_input("Height (m)", min_value=1.0, max_value=2.49, value=1.75, step=0.01)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0, step=0.5)
smoker = st.selectbox(
    "Are you a smoker?",
    options=[False, True],
    format_func=lambda value: "Yes" if value else "No",
)
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    options=[
        "retired",
        "student",
        "unemployed",
        "freelancer",
        "private_job",
        "government_job",
        "business_owner",
    ],
)

if st.button("Predict Premium Category", type="primary", use_container_width=True):
    # Field names must match the deployed Pydantic model (income_lpa, not income_in_lpa).
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city.strip(),
        "occupation": occupation,
    }

    try:
        response = requests.post(PREDICT_URL, json=input_data, timeout=30)
    except requests.exceptions.Timeout:
        st.error(f"The API at {PREDICT_URL} did not respond in time. Please try again.")
    except requests.exceptions.RequestException as exc:
        st.error(
            f"Could not connect to the FastAPI server at {PREDICT_URL}. "
            "Make sure the server is running and reachable from this machine."
        )
        st.caption(f"Details: {exc}")
    else:
        if response.status_code != 200:
            st.error(format_error(response))
        else:
            result = extract_prediction(response.json())
            category = result.get("predicted_category", "Unknown")
            confidence = result.get("confidence")
            probabilities = result.get("class_probabilities") or {}

            st.success(f"Predicted Insurance Premium Category: **{category}**")

            if confidence is not None:
                st.metric("Model confidence", f"{confidence:.0%}")

            if probabilities:
                with st.expander("Class probabilities"):
                    st.dataframe(
                        {
                            "Category": list(probabilities.keys()),
                            "Probability": [f"{value:.0%}" for value in probabilities.values()],
                        },
                        hide_index=True,
                        use_container_width=True,
                    )
