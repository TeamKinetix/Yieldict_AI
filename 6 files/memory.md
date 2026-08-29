# CropYield AI — Project Memory

## Project Identity

### Project Name

CropYield AI

### Project Type

Machine Learning Regression

### Main Objective

Predict crop yield using agricultural and environmental information.

---

# Current Project Direction

The project will use supervised machine learning.

The prediction target is crop yield.

Preferred target representation:

```text
Yield = tons/hectare
```

The exact target definition depends on the selected dataset.

---

# Model Strategy

## Baseline

Linear Regression

Purpose:

Provide a simple reference model.

## Main Models

1. Random Forest Regression
2. Extra Trees Regression
3. Gradient Boosting

## Optional

XGBoost

Only implement if it improves the project and there is enough time to test and explain it properly.

---

# Evaluation

Required metrics:

```text
MAE
RMSE
R²
```

Interpretation:

```text
MAE  → Lower is better
RMSE → Lower is better
R²   → Higher is better
```

---

# Validation Strategy

Default:

```text
80% Training
20% Validation/Test
```

For smaller datasets, cross-validation may be used.

Use a fixed random seed where appropriate:

```text
random_state = 42
```

---

# Explainability Strategy

Minimum:

Feature importance.

Optional:

SHAP.

Important distinction:

Feature importance explains model behavior.

It does not automatically prove that a feature causes crop yield to increase or decrease.

---

# Application Strategy

Recommended framework:

```text
Streamlit
```

Reason:

* Easy for a beginner.
* Python-based.
* Fast to develop.
* Suitable for ML demonstrations.

---

# Recommended Project Structure

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

# Important Decisions

## Decision 1

Use regression because crop yield is a continuous numerical value.

## Decision 2

Always compare a simple baseline against more advanced models.

## Decision 3

Use MAE, RMSE and R² for model evaluation.

## Decision 4

Use feature importance for basic explainability.

## Decision 5

Use Streamlit for the first application version.

## Decision 6

Prevent data leakage throughout preprocessing and training.

---

# Dataset Memory

The exact dataset has not yet been permanently selected in this document.

Once selected, record:

```text
Dataset Name:
Dataset Source:
Number of Rows:
Number of Columns:
Target Column:
Target Units:
Important Features:
Categorical Features:
Numerical Features:
Missing Values:
```

---

# Model Results Memory

After training, update this section.

```text
Linear Regression:
MAE:
RMSE:
R²:

Random Forest:
MAE:
RMSE:
R²:

Extra Trees:
MAE:
RMSE:
R²:

Gradient Boosting:
MAE:
RMSE:
R²:

XGBoost:
MAE:
RMSE:
R²:
```

Do not fill these values with guessed numbers.

Only add actual experimental results.

---

# Final Model

Update after model evaluation.

```text
Selected Model:
Reason:
Validation MAE:
Validation RMSE:
Validation R²:
```

---

# Current Development Status

```text
[ ] Problem defined
[ ] Dataset selected
[ ] Dataset downloaded
[ ] Dataset understood
[ ] EDA completed
[ ] Preprocessing completed
[ ] Linear Regression trained
[ ] Random Forest trained
[ ] Extra Trees trained
[ ] Gradient Boosting trained
[ ] Models compared
[ ] Best model selected
[ ] Feature importance implemented
[ ] Model saved
[ ] Streamlit application built
[ ] Application tested
[ ] Final presentation prepared
```

---

# Known Limitations

The system's predictions depend on:

* Dataset quality.
* Dataset size.
* Geographic coverage.
* Historical patterns.
* Available agricultural features.
* Environmental variability.

The model should not be presented as a guaranteed prediction.

---

# Future Improvements

Possible future features:

1. Weather API integration.
2. Real-time weather data.
3. Satellite imagery.
4. Soil data integration.
5. More advanced models.
6. Time-series forecasting.
7. Regional models.
8. Uncertainty estimation.
9. Mobile application.
10. Multilingual interface.

---

# Important Reminder

The goal of the hackathon project is not simply to obtain the highest possible model score.

The team must be able to explain:

```text
What problem are we solving?
        ↓
What data are we using?
        ↓
What is the target?
        ↓
Why is this a regression problem?
        ↓
What preprocessing did we perform?
        ↓
Which models did we test?
        ↓
How did we evaluate them?
        ↓
Why did we select the final model?
        ↓
How does the application make predictions?
        ↓
What are the limitations?
```

This explanation is essential during the hackathon presentation.
