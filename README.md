# Mlops-intensive

A 60-day MLOps sprint repository. **Phase 1** focuses on building production-style APIs with FastAPI, validating data with Pydantic, and serving a trained machine learning model behind a REST endpoint.

---

## Table of Contents

- [What's in this repo](#whats-in-this-repo)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [1. Patient Management System API](#1-patient-management-system-api)
- [2. Insurance Premium Prediction API](#2-insurance-premium-prediction-api)
- [3. DSA practice](#3-dsa-practice)
- [Known notes](#known-notes)
- [Author](#author)

---

## What's in this repo

| Area | Description |
| --- | --- |
| **Patient Management API** | CRUD REST API for patient records with Pydantic validation, computed BMI/verdict fields, sorting and filtering. |
| **Insurance Premium Prediction API** | Serves a scikit-learn `RandomForestClassifier` pipeline that predicts an insurance premium category (`Low` / `Medium` / `High`) from user input. |
| **DSA practice** | Solutions to classic LeetCode problems (Two Sum, Valid Anagram, Group Anagrams). |

---

## Tech stack

- **Python** 3.13
- **FastAPI** + **Uvicorn** — API framework and ASGI server
- **Pydantic** — request validation, field constraints and computed fields
- **pandas / NumPy** — feature construction
- **scikit-learn** — `Pipeline`, `ColumnTransformer`, `OneHotEncoder`, `RandomForestClassifier`
- **joblib / pickle** — model persistence

---

## Project structure

```
.
└── phase1/
    └── learnfastapi/
        ├── .gitignore
        ├── src/
        │   ├── main.py                  # Patient Management System API
        │   ├── pydantic_test.py         # Pydantic validation experiments
        │   ├── patients.json            # Local data store (gitignored)
        │   ├── two_sum_solution.py      # LeetCode 1 - Two Sum
        │   ├── valid_anagram_solution.py# LeetCode 242 - Valid Anagram
        │   └── group_anagram.py         # LeetCode 49 - Group Anagrams
        └── insurence_premium_model/
            ├── fastapi_ml_model.ipynb   # Training / EDA notebook
            ├── insurance.csv            # 100-row training dataset
            ├── model.pkl                # Pickled sklearn pipeline
            └── main.py                  # Insurance Premium Prediction API
```

> The virtual environment (`bin/`, `lib/`, ...) is **not** committed — see [Getting started](#getting-started).

---

## Getting started

### 1. Create and activate a virtual environment

```bash
cd phase1/learnfastapi
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install fastapi uvicorn pydantic[email] pandas numpy scikit-learn
```

Or, if you add a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Run an app

```bash
# Patient Management API
uvicorn main:app --reload
```

```bash
# Insurance Premium Prediction API
cd insurence_premium_model
uvicorn main:app --reload
```

Interactive docs are available at **http://127.0.0.1:8000/docs**.

---

## 1. Patient Management System API

File: `phase1/learnfastapi/src/main.py`

A file-backed CRUD API. Data is read from and written to `patients.json`, which is intentionally **gitignored** — create it with at least an empty object before first use:

```json
{}
```

Run it from inside `src/` (the data path is relative):

```bash
cd phase1/learnfastapi/src
uvicorn main:app --reload
```

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Health / welcome message |
| `GET` | `/about` | API description |
| `GET` | `/view` | List all patients |
| `GET` | `/patient/{patient_id}` | Get a single patient (`404` if missing) |
| `GET` | `/sort?sortby=height&order=asc` | Sort by `height`, `weight`, or `bmi` |
| `GET` | `/wordcount/{word}` | Count words in a text segment |
| `POST` | `/create` | Create a patient (`400` if the ID exists) |
| `PUT` | `/edit?patient_id=P001` | Partially update a patient |
| `DELETE` | `/delete/{patient_id}` | Delete a patient |

### Example — create a patient

```bash
curl -X POST http://127.0.0.1:8000/create \
  -H "Content-Type: application/json" \
  -d '{
        "id": "P001",
        "name": "Ananya Sharma",
        "city": "Guwahati",
        "age": 28,
        "gender": "female",
        "height": 1.65,
        "weight": 90.0
      }'
```

Response (`201`):

```json
{ "message": "Patient created successfully." }
```

The `Patient` model computes `bmi` and a `verdict` (`Underweight` / `Normal` / `Overweight` / `Obese`) automatically from `height` and `weight`.

---

## 2. Insurance Premium Prediction API

File: `phase1/learnfastapi/insurence_premium_model/main.py`

Serves the pipeline trained in `fastapi_ml_model.ipynb`.

### Model pipeline

1. **Feature engineering**
   - `bmi = weight / height²`
   - `age_group` → `young` / `adult` / `middle_aged` / `senior`
   - `lifestyle_risk` → `low` / `medium` / `high` (based on smoker + BMI)
   - `city_tier` → `1` / `2` / `3`
2. **Preprocessing** — `OneHotEncoder` for categorical features, passthrough for numeric features.
3. **Classifier** — `RandomForestClassifier(random_state=42)`.

Final model inputs: `bmi`, `age_group`, `lifestyle_risk`, `city_tier`, `income_lpa`, `occupation`.

### Endpoint

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/predict` | Predict the insurance premium category |

The API accepts `income_in_lpa` as the request field and maps it to the model's expected `income_lpa` column internally.

### Example — predict

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
        "age": 30,
        "weight": 85.0,
        "height": 1.75,
        "income_in_lpa": 12.5,
        "smoker": true,
        "city": "Mumbai",
        "occupation": "private_job"
      }'
```

Response (`200`):

```json
{ "predicted_category": "High" }
```

### Input schema

| Field | Type | Constraints |
| --- | --- | --- |
| `age` | int | `0 < age < 120` |
| `weight` | float | `> 0` (kg) |
| `height` | float | `0 < height < 2.5` (m) |
| `income_in_lpa` | float | `> 0` |
| `smoker` | bool | — |
| `city` | str | Any city; unknown cities fall to tier 3 |
| `occupation` | enum | `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job` |

---

## 3. DSA practice

LeetCode solutions kept alongside the API work:

| File | Problem | Approach |
| --- | --- | --- |
| `src/two_sum_solution.py` | Two Sum | Hash map of `target - num` |
| `src/valid_anagram_solution.py` | Valid Anagram | `collections.Counter` comparison |
| `src/group_anagram.py` | Group Anagrams | Frequency-count tuple as hash key |

---

## Known notes

- **scikit-learn version warning.** `model.pkl` was serialized with scikit-learn **1.8.0**, while the current environment uses **1.9.1**. Loading it prints `InconsistentVersionWarning`. Re-train and re-pickle the model with the installed version to remove the warning:

  ```python
  import pickle
  with open("model.pkl", "wb") as f:
      pickle.dump(pipeline, f)
  ```

- **Column name contract.** The trained pipeline expects the column `income_lpa` (not `income_in_lpa`). Keep inference DataFrames aligned with the training feature names.
- **`insurence_premium_model`** is intentionally kept with its original spelling to match the notebook and model artifacts.
- **`patients.json`** is gitignored; the Patient API will fail on first run until you create it.

---

## Author

**Bishal Shrestha** — [github.com/Bishal-Stha](https://github.com/Bishal-Stha)
