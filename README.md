# Mlops-intensive

A 60-day MLOps sprint repository. **Phase 1** focuses on building production-style APIs with FastAPI, validating data with Pydantic, containerizing them with Docker, and serving a trained machine learning model behind a REST endpoint.

[![Live API on AWS](https://img.shields.io/badge/AWS-Live%20API-FF9900?logo=amazonaws&logoColor=white)](http://3.25.131.90:8000/docs)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-programmerbishal%2Fimproved--ipm-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/programmerbishal/improved-ipm)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.150-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org)

---

## 🚀 Dockerized & Deployed on AWS

**The Insurance Premium Prediction API is containerized with Docker and running live on AWS.**

| What | Where |
| --- | --- |
| **Live API** | **http://3.25.131.90:8000** |
| **Swagger UI** | **http://3.25.131.90:8000/docs** |
| **Health check** | **http://3.25.131.90:8000/health** |
| **Docker image** | **`programmerbishal/improved-ipm:1.0.1`** (`latest` also published) |
| **Docker Hub** | **https://hub.docker.com/r/programmerbishal/improved-ipm** |
| **Docker Hub profile** | **https://hub.docker.com/u/programmerbishal** |
| **Hosting** | **AWS EC2 + Docker, served by Uvicorn on port 8000** |

```bash
# Pull the exact image running in production
docker pull programmerbishal/improved-ipm:1.0.1

# Run it anywhere
docker run -d --name improved-ipm -p 8000:8000 programmerbishal/improved-ipm:1.0.1
```

Full build, push, and AWS deployment steps: [Docker & AWS deployment](#4-docker--aws-deployment).

---

## Table of Contents

- [🚀 Dockerized & Deployed on AWS](#-dockerized--deployed-on-aws)
- [What's in this repo](#whats-in-this-repo)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [1. Patient Management System API](#1-patient-management-system-api)
- [2. Insurance Premium Prediction API](#2-insurance-premium-prediction-api)
- [3. Improved Insurance Premium API (`improved_IPM`)](#3-improved-insurance-premium-api-improved_ipm)
- [4. Docker & AWS deployment](#4-docker--aws-deployment)
- [5. DSA practice](#5-dsa-practice)
- [Known notes](#known-notes)
- [Author](#author)

---

## What's in this repo

| Area | Description |
| --- | --- |
| **Patient Management API** | CRUD REST API for patient records with Pydantic validation, computed BMI/verdict fields, sorting and filtering. |
| **Insurance Premium Prediction API** | Serves a scikit-learn `RandomForestClassifier` pipeline that predicts an insurance premium category (`Low` / `Medium` / `High`) from user input. |
| **Improved Insurance Premium API** | Production-style variant in `phase1/improved_IPM/` with layered `schema/` + `model/` modules, confidence scores and class probabilities. **This is the Docker image deployed to AWS.** |
| **Streamlit frontends** | Web UI that sends user input to the prediction API and renders the predicted category, confidence, and class probabilities. |
| **DSA practice** | Solutions to classic LeetCode problems (Two Sum, Valid Anagram, Group Anagrams). |

---

## Tech stack

- **Python** 3.13
- **FastAPI** + **Uvicorn** — API framework and ASGI server
- **Pydantic** — request validation, field constraints and computed fields
- **pandas / NumPy** — feature construction
- **scikit-learn** — `Pipeline`, `ColumnTransformer`, `OneHotEncoder`, `RandomForestClassifier`
- **joblib / pickle** — model persistence
- **Streamlit** — interactive frontend for the prediction API
- **Docker** — production image `programmerbishal/improved-ipm` (non-root user, healthcheck, slim Python base)
- **Docker Hub** — image registry ([programmerbishal](https://hub.docker.com/u/programmerbishal))
- **AWS EC2** — hosts the container and exposes it on port 8000

---

## Project structure

```
.
├── flask-app/                         # Small Dockerized Flask demo
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── phase1/
    ├── improved_IPM/                  # Dockerized + AWS-deployed API
    │   ├── Dockerfile
    │   ├── .dockerignore
    │   ├── main.py                    # FastAPI app
    │   ├── requirements.txt
    │   ├── config/
    │   │   └── city_teir.py           # Tier-1 / tier-2 city lists
    │   ├── model/
    │   │   ├── model.pkl              # Trained sklearn pipeline
    │   │   └── predict.py             # Inference + probabilities
    │   └── schema/
    │       ├── user_input.py          # Request model + computed fields
    │       └── prediction_response.py # Response model
    └── learnfastapi/
        ├── .gitignore
        ├── src/
        │   ├── main.py                # Patient Management System API
        │   ├── pydantic_test.py       # Pydantic validation experiments
        │   ├── patients.json          # Local data store (gitignored)
        │   ├── two_sum_solution.py    # LeetCode 1 - Two Sum
        │   ├── valid_anagram_solution.py# LeetCode 242 - Valid Anagram
        │   └── group_anagram.py       # LeetCode 49 - Group Anagrams
        └── insurence_premium_model/
            ├── fastapi_ml_model.ipynb # Training / EDA notebook
            ├── insurance.csv          # 100-row training dataset
            ├── model.pkl              # Pickled sklearn pipeline
            ├── main.py                # Insurance Premium Prediction API
            ├── frontend.py            # Streamlit UI (defaults to the AWS API)
            └── requirements.txt
```

> Virtual environments (`myenv/`, `.venv/`, `bin/`, `lib/`, ...) are **not** committed — see [Getting started](#getting-started).

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
pip install fastapi uvicorn pydantic[email] pandas numpy scikit-learn streamlit requests
```

Or install a project's pinned set:

```bash
pip install -r phase1/improved_IPM/requirements.txt
pip install -r phase1/learnfastapi/insurence_premium_model/requirements.txt
```

### 3. Run an app

```bash
# Patient Management API
uvicorn main:app --reload
```

```bash
# Insurance Premium Prediction API (local, from learnfastapi)
cd insurence_premium_model
uvicorn main:app --reload
```

```bash
# Improved API (the one that is Dockerized and deployed)
cd phase1/improved_IPM
uvicorn main:app --reload
```

```bash
# Streamlit frontend — points at the AWS API by default
cd phase1/learnfastapi/insurence_premium_model
streamlit run frontend.py

# ...or target a local backend instead
API_BASE_URL=http://localhost:8000 streamlit run frontend.py
```

Interactive docs are available at **http://127.0.0.1:8000/docs** when running locally.

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

## 3. Improved Insurance Premium API (`improved_IPM`)

Directory: `phase1/improved_IPM/` — **this is the service that is containerized and deployed on AWS.**

It is a refactored version of the API above, split into `schema/`, `model/`, and `config/` packages, and it returns richer output (confidence + per-class probabilities) using the response model in `schema/prediction_response.py`.

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Liveness probe: status, model version, model-loaded flag |
| `POST` | `/predict` | Predict the insurance premium category and return probabilities |

The request field is **`income_lpa`** (not `income_in_lpa`). City input is normalized to title case (`"mumbai"` → `"Mumbai"`) before tier lookup.

### Example — predict against the AWS deployment

```bash
curl -X POST http://3.25.131.90:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
        "age": 30,
        "weight": 65.0,
        "height": 1.75,
        "income_lpa": 10.0,
        "smoker": false,
        "city": "Mumbai",
        "occupation": "private_job"
      }'
```

Response (`200`):

```json
{
  "response": {
    "predicted_category": "Low",
    "confidence": 0.73,
    "class_probabilities": { "High": 0.01, "Low": 0.73, "Medium": 0.26 }
  }
}
```

> The deployed API wraps the prediction in a top-level `response` object. The Streamlit frontend in `learnfastapi/insurence_premium_model/frontend.py` handles this shape automatically and defaults to the AWS URL (override with `API_BASE_URL`).

### Input schema

| Field | Type | Constraints |
| --- | --- | --- |
| `age` | int | `0 < age < 120` |
| `weight` | float | `> 0` (kg) |
| `height` | float | `0 < height < 2.5` (m) |
| `income_lpa` | float | `> 0` |
| `smoker` | bool | — |
| `city` | str | Any city; stripped, title-cased, unknown cities fall to tier 3 |
| `occupation` | enum | `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job` |

---

## 4. Docker & AWS deployment

The API is shipped as a Docker image and runs in a container on an AWS EC2 instance.

**Docker Hub:** **https://hub.docker.com/r/programmerbishal/improved-ipm** · **Profile:** https://hub.docker.com/u/programmerbishal

| Tag | Notes |
| --- | --- |
| `1.0.1` | Current production tag |
| `latest` | Points at the latest build |

### Image design (`phase1/improved_IPM/Dockerfile`)

- `python:3.13-slim` base, unbuffered logs, no `.pyc` files, pip cache disabled
- Dependencies installed in their own layer before source is copied, so rebuilds are fast
- Runs as a **non-root user** (`appuser`, UID 10001)
- Built-in `HEALTHCHECK` that polls `/health`
- `EXPOSE 8000`, started with `uvicorn main:app --host 0.0.0.0 --port 8000`
- `.dockerignore` keeps `myenv/`, `__pycache__/`, `.env`, and docs out of the image

### Build and push

```bash
cd phase1/improved_IPM

docker build -t programmerbishal/improved-ipm:1.0.1 .
docker tag programmerbishal/improved-ipm:1.0.1 programmerbishal/improved-ipm:latest

docker push programmerbishal/improved-ipm:1.0.1
docker push programmerbishal/improved-ipm:latest
```

> Build from `phase1/improved_IPM/` — the app loads the model from the relative path `model/model.pkl`.

### Run locally

```bash
docker run -d --name improved-ipm -p 8000:8000 programmerbishal/improved-ipm:1.0.1
curl http://localhost:8000/health
```

### Deploy on AWS EC2

1. Launch an EC2 instance with Docker installed.
2. Allow inbound **TCP 8000** in the instance's security group (plus SSH from your IP).
3. Pull and run the published image:

   ```bash
   docker pull programmerbishal/improved-ipm:1.0.1
   docker run -d --restart unless-stopped \
     --name improved-ipm \
     -p 8000:8000 \
     programmerbishal/improved-ipm:1.0.1
   ```

4. Verify from anywhere:

   ```bash
   curl http://3.25.131.90:8000/health
   # {"status":"OK","version":"1.0.0","model_loaded":true}
   ```

The service is now live at **http://3.25.131.90:8000** (docs at **/docs**, health at **/health**).

### Updating the deployment

```bash
# Build and push a new tag from your machine
docker build -t programmerbishal/improved-ipm:1.0.2 .
docker push programmerbishal/improved-ipm:1.0.2

# On the EC2 instance
docker pull programmerbishal/improved-ipm:1.0.2
docker rm -f improved-ipm
docker run -d --restart unless-stopped --name improved-ipm -p 8000:8000 programmerbishal/improved-ipm:1.0.2
```

---

## 5. DSA practice

LeetCode solutions kept alongside the API work:

| File | Problem | Approach |
| --- | --- | --- |
| `src/two_sum_solution.py` | Two Sum | Hash map of `target - num` |
| `src/valid_anagram_solution.py` | Valid Anagram | `collections.Counter` comparison |
| `src/group_anagram.py` | Group Anagrams | Frequency-count tuple as hash key |

---

## Known notes

- **scikit-learn version.** `model.pkl` was serialized with scikit-learn **1.8.0**, which is why `phase1/improved_IPM/requirements.txt` pins `scikit-learn==1.8.0`. Loading it with a different version prints `InconsistentVersionWarning` and can shift predictions; re-train and re-pickle if you upgrade:

  ```python
  import pickle
  with open("model/model.pkl", "wb") as f:
      pickle.dump(pipeline, f)
  ```

- **Column name contract.** The trained pipeline expects the column `income_lpa` (not `income_in_lpa`). The deployed `improved_IPM` API uses `income_lpa` in both the request and the inference DataFrame; the older `learnfastapi` API maps `income_in_lpa` to it internally.
- **Docker build context.** Always build from `phase1/improved_IPM/`, since the app loads `model/model.pkl` via a relative path and `uvicorn` must run with that directory as the working directory.
- **`insurence_premium_model`** is intentionally kept with its original spelling to match the notebook and model artifacts.
- **`patients.json`** is gitignored; the Patient API will fail on first run until you create it.

---

## Author

**Bishal Shrestha** — [github.com/Bishal-Stha](https://github.com/Bishal-Stha)

- **Docker Hub:** [hub.docker.com/u/programmerbishal](https://hub.docker.com/u/programmerbishal)
- **Deployed API:** [http://3.25.131.90:8000/docs](http://3.25.131.90:8000/docs)
