# Vehicle Insurance Prediction - MLOps Project

This project implements an end-to-end MLOps pipeline for predicting vehicle insurance interest using the **XGBoost Classifier**. It demonstrates a robust, modular architecture for training, evaluating, and deploying machine learning models, integrating modern technologies like FastAPI, Docker, MongoDB, and AWS S3.

## 📌 Project Overview

The goal of this project is to predict whether a customer is likely to be interested in vehicle insurance based on various demographic and vehicle-related features. The solution allows for:
- **Real-time predictions** via a Web UI and REST API.
- **Batch predictions** for processing multiple records at once.
- **Automated Training Pipeline** to retrain and update models.
- **Continuous Deployment** of model artifacts to the cloud.

## 🧠 Model Details

We use the **XGBoost (Extreme Gradient Boosting)** algorithm, known for its high performance and efficiency in classification tasks.

- **Algorithm**: `XGBoostClassifier`
- **Objective**: Binary Classification (`binary:logistic`)
- **Key Hyperparameters**:
  - `learning_rate`: 0.1
  - `n_estimators`: 100
  - `max_depth`: 6
  - `subsample`: 0.8
  - `colsample_bytree`: 0.8
- **Metrics**: The model is evaluated based on **Accuracy**, **F1 Score**, **Precision**, and **Recall**.

## 🚀 Pipeline Architecture

The project follows a modular pipeline structure defined in `src/pipline/`:

1.  **Data Ingestion**:
    -   Fetches raw data from a **MongoDB** database.
    -   Splits data into training and testing sets.
    -   Artifacts: `train.csv`, `test.csv`.

2.  **Data Validation**:
    -   Validates the schema of the incoming data against a defined schema.
    -   Checks for data drift and anomalies.

3.  **Data Transformation**:
    -   Handles missing values and performs feature engineering.
    -   Encodes categorical variables (e.g., `Gender`, `Vehicle_Damage`).
    -   Scales numerical features.
    -   Artifacts: `preprocessor.pkl` (serialized transformation object).

4.  **Model Trainer**:
    -   Trains the **XGBoost** model on the transformed data.
    -   Saves the trained model artifact.

5.  **Model Evaluation**:
    -   Compares the newly trained model against the currently deployed model (if exists) in AWS S3.
    -   Promotes the new model only if it achieves a better performance score.

6.  **Model Pusher**:
    -   Uploads the approved model artifact to **AWS S3** for deployment.

## 🛠 Tech Stack

-   **Language**: Python 3.8+
-   **Web Framework**: FastAPI, Jinja2 Templates
-   **Machine Learning**: XGBoost, Scikit-Learn, Pandas, NumPy
-   **Database**: MongoDB (Data Source)
-   **Cloud Storage**: AWS S3 (Model Registry)
-   **Containerization**: Docker
-   **Frontend**: HTML5, CSS3, JavaScript (Batch Processing)

## 📂 Project Structure

```bash
MLops-7-Project/
├── app.py                  # FastAPI Application entry point
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── src/                    # Source code
│   ├── components/         # Pipeline components (Ingestion, Trainer, etc.)
│   ├── entity/             # Configuration & Artifact dataclasses
│   ├── pipline/            # Training & Prediction pipelines
│   └── utils/              # Utility functions
├── static/                 # CSS, JS, Images
└── templates/              # HTML Templates
```

## 💻 How to Use

### Prerequisites
-   **MongoDB**: a running MongoDB instance with the dataset.
-   **AWS Credentials**: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` configured for S3 access.

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone <repo-url>
cd MLops-7-Project
pip install -r requirements.txt
```

### 2. Running Locally

Start the FastAPI server:

```bash
python app.py
```

Access the application at `http://localhost:8080`.

### 3. Using the Application

-   **Web Interface**: Navigate to the home page to enter vehicle details manually or upload a batch file.
-   **Train Model**: Trigger the training pipeline by visiting `/train` or using the "Admin Train Model" button.
-   **Prediction**:
    -   **Single Prediction**: Submit the form on the UI.
    -   **Batch Prediction**: Use the API endpoint `/predict_batch` with a JSON payload of rows.

### 4. Docker Usage

Build and run the container:

```bash
docker build -t mlops-project .
docker run -p 8080:8080 -e AWS_ACCESS_KEY_ID=... -e AWS_SECRET_ACCESS_KEY=... mlops-project
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Renders the HTML Web Interface. |
| `POST` | `/` | Handles form submission and returns predictions. |
| `GET` | `/train` | Triggers the full training pipeline. |
| `GET` | `/run-demo` | Streams training logs to the UI. |
| `POST` | `/predict` | API endpoint for single JSON prediction. |
| `POST` | `/predict_batch` | API endpoint for batch predictions. |

---
*Built within the MLops-7-Project ecosystem utilizing advanced Agentic Coding.*
