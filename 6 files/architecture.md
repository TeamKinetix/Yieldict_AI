# Crop Yield Prediction — System Architecture

## 1. Architecture Overview

The system follows a standard machine learning pipeline.

```text
                 ┌──────────────────┐
                 │     Dataset      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Data Validation   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Preprocessing     │
                 │ & Feature Eng.    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Train/Validation  │
                 │ Split             │
                 └────────┬─────────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        Linear Reg.   Random Forest  Extra Trees
              │           │           │
              └───────────┼───────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Model Evaluation │
                 │ MAE/RMSE/R²      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Best Model       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Saved Model      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Prediction API   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Web Application  │
                 └──────────────────┘
```

---

## 2. Project Components

### Component 1 — Dataset

Contains historical agricultural records.

Possible location:

```text
data/
└── crop_yield.csv
```

---

## 3. Data Processing Layer

Responsibilities:

* Load data.
* Validate columns.
* Handle missing values.
* Handle categorical variables.
* Process numerical variables.
* Detect invalid records.
* Prepare training data.

Example structure:

```text
src/
└── preprocessing.py
```

---

## 4. Exploratory Data Analysis

EDA should investigate:

* Dataset size.
* Feature distributions.
* Missing values.
* Correlations.
* Outliers.
* Crop-wise patterns.
* Regional patterns.

Possible notebook:

```text
notebooks/
└── 01_eda.ipynb
```

---

## 5. Feature Engineering

Feature engineering may include:

* Converting units.
* Creating derived variables.
* Encoding categorical variables.
* Normalization/scaling where required.
* Removing irrelevant columns.

Feature engineering must be performed consistently during training and prediction.

---

## 6. Model Training

Models:

```text
Linear Regression
Random Forest Regression
Extra Trees Regression
Gradient Boosting
XGBoost (optional)
```

Example:

```text
src/
└── train.py
```

The training process should:

1. Load processed data.
2. Separate X and y.
3. Split data.
4. Train models.
5. Evaluate models.
6. Compare results.
7. Select best model.
8. Save model.

---

## 7. Model Evaluation

Evaluation output should resemble:

```text
Model              MAE       RMSE      R²
------------------------------------------------
Linear Regression  0.82      1.21      0.71
Random Forest      0.54      0.81      0.87
Extra Trees        0.49      0.76      0.90
Gradient Boosting  0.51      0.79      0.89
```

These numbers are examples only.

Actual results must come from the dataset.

---

## 8. Model Persistence

The final trained model should be saved.

Possible format:

```text
models/
└── best_model.pkl
```

If preprocessing is required, it should ideally be stored together with the model using a pipeline.

---

## 9. Prediction Layer

The prediction component accepts user input.

Example:

```text
{
    "crop": "Rice",
    "rainfall": 1200,
    "temperature": 27,
    "area": 2,
    "fertilizer": 150
}
```

The input is passed through the same preprocessing pipeline used during training.

Output:

```text
{
    "predicted_yield": 3.8
}
```

---

## 10. Frontend

A simple web application can be implemented using:

### Recommended for beginner

**Streamlit**

Advantages:

* Easy Python integration.
* No complex frontend framework required.
* Fast to build.
* Suitable for ML hackathons.

Possible structure:

```text
app.py
```

---

## 11. Suggested Project Structure

```text
crop-yield-ml/
│
├── data/
│   └── crop_yield.csv
│
├── notebooks/
│   └── 01_eda.ipynb
│
├── models/
│   └── best_model.pkl
│
├── src/
│   ├── preprocessing.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
│
├── app.py
├── requirements.txt
│
├── PRD.md
├── architecture.md
├── rules.md
├── phases.md
├── design.md
└── memory.md
```

---

## 12. Technology Stack

### Programming

Python

### Machine Learning

* pandas
* NumPy
* scikit-learn
* XGBoost if required

### Visualization

* Matplotlib
* Seaborn

### UI

Streamlit

### Model Storage

Joblib or pickle

### Development

Jupyter Notebook + VS Code

---

## 13. Data Flow

```text
User Input
    ↓
Input Validation
    ↓
Preprocessing Pipeline
    ↓
ML Model
    ↓
Prediction
    ↓
Explainability
    ↓
Result Display
```

---

## 14. Architecture Principle

The same preprocessing logic must be used during training and prediction.

Avoid manually preprocessing training and prediction data differently.

Preferred:

```text
Pipeline(
    preprocessing,
    model
)
```

This reduces errors and data leakage.
