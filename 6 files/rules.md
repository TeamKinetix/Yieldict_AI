# Crop Yield Prediction — Project Rules

## 1. General Rules

1. Keep the project simple enough to understand and demonstrate.
2. Do not add unnecessary technologies.
3. Every major ML decision must have a reason.
4. Do not claim results that were not actually measured.
5. Use reproducible experiments whenever possible.

---

## 2. Dataset Rules

1. Document the dataset source.
2. Do not modify the original dataset unnecessarily.
3. Keep a clean copy of the raw dataset.
4. Check column names and data types.
5. Check missing values.
6. Check duplicate records.
7. Check invalid values.
8. Understand what each feature means before using it.

---

## 3. Target Variable Rules

The target variable should represent crop yield.

Example:

```text
Yield = tons/hectare
```

Do not accidentally include the target variable among the input features.

---

## 4. Data Leakage Rules

Data leakage is strictly prohibited.

Examples of potentially dangerous features include information that is only known after harvest when the goal is pre-harvest prediction.

Do not use future information to predict the past.

Preprocessing must be fitted on training data only.

---

## 5. Train/Test Rules

Use a clear validation strategy.

For a standard dataset:

```text
Training: 80%
Validation/Test: 20%
```

The exact split can change if the dataset structure requires another approach.

For small datasets, cross-validation should be considered.

---

## 6. Random State

Use a fixed random state where appropriate.

Example:

```python
random_state=42
```

This makes experiments more reproducible.

---

## 7. Model Rules

Always start with a baseline.

Required baseline:

```text
Linear Regression
```

Then compare with:

```text
Random Forest
Extra Trees
Gradient Boosting
```

XGBoost is optional.

Do not automatically assume that the most complicated model is the best model.

---

## 8. Evaluation Rules

Every model must be evaluated using:

```text
MAE
RMSE
R²
```

### MAE

Lower is better.

### RMSE

Lower is better.

### R²

Higher is better.

Do not report training metrics alone.

Validation/test performance must be reported.

---

## 9. Model Selection Rules

The final model should be selected based on validation performance and practical considerations.

Do not select a model simply because:

* It is more advanced.
* It has a popular name.
* AI suggested it.
* It performs well only on training data.

---

## 10. Feature Engineering Rules

Feature engineering must be based on meaningful domain logic.

Avoid creating hundreds of meaningless features.

Every engineered feature should have a reason.

---

## 11. Explainability Rules

At minimum, provide feature importance for tree-based models.

Example:

```text
Feature              Importance
Rainfall             0.31
Temperature          0.24
Fertilizer           0.19
Soil Type            0.13
Area                 0.08
```

If SHAP is implemented, clearly explain that it shows model contribution rather than proving real-world causation.

---

## 12. UI Rules

The interface should be:

* Simple
* Clean
* Easy to understand
* Mobile-friendly where practical
* Focused on the prediction

Avoid unnecessary animations and complicated pages.

---

## 13. Prediction Rules

Before prediction:

1. Validate user input.
2. Check ranges where meaningful.
3. Apply the same preprocessing as training.
4. Pass data to the trained model.
5. Display the prediction with units.

Example:

```text
Predicted Yield: 3.8 tons/hectare
```

---

## 14. Error Handling

The application should not crash because of normal invalid input.

Examples:

* Missing value
* Negative area
* Invalid crop
* Non-numeric rainfall
* Invalid temperature

Display a useful error message.

---

## 15. Code Rules

Use:

* Meaningful variable names.
* Functions for repeated logic.
* Comments for complex ML operations.
* Modular files.

Avoid:

* Huge single files.
* Hardcoded paths where possible.
* Repeated code.
* Unused libraries.

---

## 16. AI Usage Rules

AI may be used to:

* Explain ML concepts.
* Generate boilerplate code.
* Debug errors.
* Improve UI.
* Suggest feature engineering.
* Explain model results.

However, the team must understand the code enough to explain it during the hackathon.

Never submit AI-generated results without testing them.

---

## 17. Documentation Rules

Document:

* Dataset source.
* Features.
* Target.
* Preprocessing.
* Models.
* Evaluation metrics.
* Final model.
* Limitations.

---

## 18. Claim Rules

Do not say:

> "Our model guarantees crop yield."

Instead say:

> "Our model estimates crop yield based on patterns learned from historical data."

---

## 19. Security Rules

Do not store:

* Passwords
* API keys
* Personal user data

inside the repository.

Use environment variables for secrets if any are required.

---

## 20. Final Quality Rule

Before the final presentation, verify that:

```text
Dataset works
      ↓
Preprocessing works
      ↓
Training works
      ↓
Evaluation works
      ↓
Model saved
      ↓
Prediction works
      ↓
UI works
      ↓
Demo works from start to finish
```
